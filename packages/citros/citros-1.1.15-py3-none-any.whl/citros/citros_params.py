import yaml
import json
import os
import numpy as np
from pathlib import Path


class citros_params():
    def __init__(self, citros):
        self.citros = citros
        self.log = citros.log
        self.CONFIG_FOLDER = None
   

    def _coercion(self, value, type):
        if value is None:
            return None

        if type == "FLOAT":
            return float(value)
        if type == "INT":
            return int(float(value))
        return value
        
    
    def _eval_distribution(self, parameter_setting):
        """
        Evaluates a distribution based on the given parameter settings.

        Args:
            parameter_setting (dict): A dictionary containing the parameter settings for the 
                distribution. It should contain 'distribution_type' and corresponding parameters.

        Returns:
            The generated value from the specified distribution.

        Raises:
            ValueError: If 'distribution_param1' is None.
            KeyError: If the distribution_type is not supported.
        """
        distribution_type = parameter_setting["distribution_type"]

        if distribution_type == "STRING":
            return parameter_setting["distribution_param1"]
        
        # sanity check:
        if parameter_setting.get("distribution_param1", None) is None:
            raise ValueError("distribution_param1 is None")

        if distribution_type == "FLOAT":
            return self._coercion(parameter_setting["distribution_param1"], "FLOAT")

        param1 = self._coercion(parameter_setting.get("distribution_param1", None), 
                                parameter_setting.get("param1_type", None))
        param2 = self._coercion(parameter_setting.get("distribution_param2", None), 
                                parameter_setting.get("param2_type", None))
        
        distribution_mapping = {
            "NORMAL": lambda: np.random.normal(param1, param2),
            "EXPONENTIAL": lambda: np.random.exponential(param1),
            "LAPLACE": lambda: np.random.laplace(param1, param2),
            "POISSON": lambda: np.random.poisson(param1),
            "POWER": lambda: np.random.power(param1),
            "UNIFORM": lambda: np.random.uniform(param1, param2),
            "ZIPF": lambda: np.random.zipf(param1),
            "VONMISES": lambda: np.random.vonmises(param1, param2),
            "RAYLEIGH": lambda: np.random.rayleigh(param1)
        }
        try:
            return distribution_mapping[distribution_type]()
        except KeyError:
            self.log.error(f"Error: {distribution_type} is not supported.")
    

    def save_config(self, config):  
        # callback running inside ROS workspace context.   
        from ament_index_python.packages import get_package_share_directory
                
        for package_name, citros_config in config['packages'].items():
            self.log.debug(f"Saving config for [{package_name}]")

            # TODO: add other method to get the package path
            path_to_package = None
            try:
                # get the path to the package install directory - the project must be sourced for it to work 
                path_to_package = get_package_share_directory(package_name)            
            except Exception as e:
                self.log.exception(e)
                continue                

            if not path_to_package:
                continue
                
            path = Path(path_to_package, "config")    
            
            # check if folder exists
            if not path.exists():
                self.log.debug(f"No config file {path} exits for pack:{package_name}. passing.") 
                continue
                                                
            path = Path(path, "params.yaml")
            
            # check if file exists
            if not Path(path).exists():
                self.log.debug(f"No config file {path} exits for package: {package_name}. passing.") 
                continue
            
            with open(path, "r") as stream:
                try:    
                    default_config = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    self.log.exception(exc)
            
            # citros_config will overwrite default_config if the same key appears in both. 
            merged_config = {**default_config, **citros_config}
            self.log.debug(json.dumps(merged_config, indent=4))
            
            # override default values
            with open(path, 'w') as file:
                yaml.dump(merged_config, file)  

            # sanity check
            if self.CONFIG_FOLDER is None:
                raise ValueError(f"citros_params.save_config: CONFIG_FOLDER is None.")

            # save for metadata
            Path(self.CONFIG_FOLDER).mkdir(exist_ok=True)
            with open(Path(self.CONFIG_FOLDER, f"{package_name}.yaml"), 'w') as file:                                     
                yaml.dump(merged_config, file)         
    

    def evaluate_distributions_recursive(self, data):
        if isinstance(data, dict):
            if "distribution_type" in data:
                # This is a distribution object, evaluate it
                return self._eval_distribution(data)
            else:
                # This is a normal dictionary, recursively evaluate its values
                return {k: self.evaluate_distributions_recursive(v) for k, v in data.items()}
        elif isinstance(data, list):
            # This is a list, recursively evaluate its items
            return [self.evaluate_distributions_recursive(item) for item in data]
        else:
            # This is a primitive data type, return it as is
            return data
        

    def init_params(self, simulation_name : str, sim_run_dir : str):
        """
        Fetches parameters from CITROS, saves them to files, and returns the config.
        """          
        self.CONFIG_FOLDER = os.path.join(sim_run_dir, 'config')

        if not simulation_name.endswith('.json'):
            simulation_name = simulation_name + '.json'

        with open(Path(self.citros.SIMS_DIR, simulation_name), 'r') as file:
            sim_data = json.load(file)

        param_setup = sim_data['parameter_setup']

        with open(Path(self.citros.PARAMS_DIR, param_setup), 'r') as file:
            param_setup_data = json.load(file)

        processed_data = self.evaluate_distributions_recursive(param_setup_data)

        self.log.debug("Saving parameters to files. ")        
        self.save_config(processed_data)
        self.log.debug("Done saving config files.")      

        return processed_data