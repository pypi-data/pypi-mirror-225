import traceback
import jwt
import json
import traceback
import os
import git
import time
import shutil
import jsonschema
import subprocess
from python_on_whales import docker
import importlib.resources
from datetime import datetime
from pathlib import Path
from decouple import config
from os import linesep

## graphQL
from gql import Client, gql
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport

import requests 

from .citros_events import citros_events
from .citros_utils import citros_utils
from .citros_batch import citros_batch
from .parsers import parser_ros2
from .citros_params import citros_params
from .logger import get_logger, shutdown
import citros_meta


class Citros:
    """
    The Citros class implements the frontend of the Citros CLI.
    It must be instantiated within a `with` block in order to prevent 
    resource leaks and unexpected behavior.
    """

    # for colored console output 
    COLORS = {
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow' : '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'default': '\033[0m'
    }

    def __init__(self, user_proj_dir=".", verbose=False, debug=False, on_init=False):    
        """
        Initialize Citros instance.

        Args:
        user_proj_dir:  optional user project directory, defaults to current 
                        working directory.
        verbose:        optionally turn on verbose console output.
        debug:          If True, sets log level to debug and turns on debug
                        output for the ROS simulation. Else, log level will 
                        be info, and debug output for the ROS simulation will 
                        not be given. Defaults to False.
        """
        self.VERBOSE = verbose
        self.STATS_INTERVAL = 1     # seconds
        self.BAG_NAME = 'bag_0.db3' # default to sqlite3

        if on_init:
            self.USER_PROJ_DIR = Path(user_proj_dir).expanduser().resolve()
            self.CITROS_REPO_DIR = Path(self.USER_PROJ_DIR, ".citros")
        else:
            self.CITROS_REPO_DIR = self.find_citros_in_ancestors(user_proj_dir)
            self.is_initialized = (self.CITROS_REPO_DIR is not None)
            if self.is_initialized:
                self.USER_PROJ_DIR = self.CITROS_REPO_DIR.parent
            else:
                self.CITROS_REPO_DIR = Path("INVALID_PATH")
                self.USER_PROJ_DIR = Path("INVALID_PATH")

        self.CITROS_HOME_DIR = Path.home() / ".citros"

        self.alternate_auth_paths = [self.CITROS_HOME_DIR / "auth", 
                                     Path("/var/lib/citros/auth")]

        self.PROJECT_FILE = Path(self.CITROS_REPO_DIR, "project.json")
        self.SETTINGS_FILE = Path(self.CITROS_REPO_DIR, "settings.json")
        self.REPO_ID_FILE = Path(self.CITROS_REPO_DIR, 'citros_repo_id')

        # subdirs
        self.SIMS_DIR = Path(self.CITROS_REPO_DIR, "simulations")
        self.PARAMS_DIR = Path(self.CITROS_REPO_DIR, "parameter_setups")
        self.NOTEBOOKS_DIR = Path(self.CITROS_REPO_DIR, "notebooks")
        self.WORKFLOWS_DIR = Path(self.CITROS_REPO_DIR, "workflows")
        self.REPORTS_DIR = Path(self.CITROS_REPO_DIR, "reports")
        self.RUNS_DIR = Path(self.CITROS_REPO_DIR, "runs")

        self.CLI_LOGS_DIR = Path(self.CITROS_HOME_DIR, "logs")

        self._user = None
        # do not access directly, only via get/set token.
        self._jwt_token = None
        
        # GQL
        self._gql_client = None
        self._token_changed = False
        
        # for logger. do not set directly, only via set_logger
        self._batch_id = None
        self._run_id = None

        # set via create_sim_run_dir, do not set directly
        self.SIM_RUN_DIR = None
        self.BAG_DIR = None
        self.MSGS_DIR = None

        # set via set_batch_name_and_message, do not set directly
        self._batch_name = ""
        self._batch_message = ""

        self._sim_name = None

        self.CITROS_ENVIRONMENT = config("CITROS_ENVIRONMENT", "LOCAL")
        self.DOCKER_REGISTRY = config("DOCKER_REGISTRY", "us-central1-docker.pkg.dev/citros")
        
        # internal communication is via http
        url_prefix = "http" if self.CITROS_ENVIRONMENT == "CLUSTER" else "https"

        self.CITROS_DOMAIN = config("CITROS_DOMAIN", "citros.io")
        self.CITROS_URL = f"{url_prefix}://{self.CITROS_DOMAIN}"
        self.CITROS_GIT_USER = config("CITROS_GIT_USER", "git")
        self.CITROS_GIT_DOMAIN = config("CITROS_GIT_DOMAIN", self.CITROS_DOMAIN)
        self.CITROS_GIT_URL = f"{self.CITROS_GIT_USER}@{self.CITROS_GIT_DOMAIN}"
        
        self.print(f"--- using CITROS_URL = {self.CITROS_URL}", only_verbose=True)
        self.print(f"--- using CITROS_GIT_URL = {self.CITROS_GIT_URL}", only_verbose=True)
        
        self.CITROS_ENTRYPOINT = f"{self.CITROS_URL}/api/graphql"
        self.CITROS_LOGS = f"{self.CITROS_URL}/api/logs"        
        self.CITROS_GTOKEN = f"{self.CITROS_URL}/api/gtoken" 
        self.CITROS_HEALTH_CHECK = f"{self.CITROS_URL}/api/check" 
        
        self.OPEN_TELEMETRY_URL = config("OPEN_TELEMETRY_URL", "localhost:3417")

        self.log = None

        self.log_level = 'debug' if debug else 'info'
        self.set_logger(self.CLI_LOGS_DIR)
        
        self._init_components()

        self.repo_id = None
        if self.REPO_ID_FILE.exists():
            with open(self.REPO_ID_FILE, 'r') as file:
                self.repo_id = file.read()
    

    def _init_components(self):
        self.events = citros_events(self)        
        self.parser_ros2 = parser_ros2(self)       
        self.params = citros_params(self)
        self.utils = citros_utils(self)
        self.batch = citros_batch(self)


    def print(self, message, only_debug=False, only_verbose=False, color='default'):
        if (only_debug and self.log_level != 'debug') or \
           (only_verbose and not self.VERBOSE):
            return
        
        default = Citros.COLORS['default']
        color = Citros.COLORS[color]
        if color is None:
            color = default
        
        print(f"{color}{message}{default}")


    def find_citros_in_ancestors(self, proj_dir=""):
        current_dir = Path.cwd() if not proj_dir else Path(proj_dir).expanduser().resolve()

        # Ensure we don't go into an infinite loop at the root directory
        while current_dir != current_dir.parent:
            citros_dir = current_dir / ".citros"
            if citros_dir.exists():
                return citros_dir.expanduser().resolve()
            current_dir = current_dir.parent

        return None


    def find_auth_key(self, proj_dir=""):
        # option 1: Start from current directory and traverse upwards
        citros_dir = self.find_citros_in_ancestors(proj_dir)
        if citros_dir is not None and Path(citros_dir, "auth").exists():
            return Path(citros_dir, "auth")

        # option 2: Look in alternate locations, e.g. the user's home folder.
        for auth_path in self.alternate_auth_paths:
            if auth_path.exists():
                return auth_path.expanduser().resolve()
        
        return None
    

    def set_auth_key(self, key, proj_dir=""):
        citros_dir = self.find_citros_in_ancestors(proj_dir)
        if citros_dir is not None:
            auth_path = Path(citros_dir, "auth")
        else:
            Path(self.CITROS_HOME_DIR).mkdir(exist_ok=True)
            auth_path = Path(self.CITROS_HOME_DIR, "auth") 
        
        with open(auth_path, 'w') as file:
            file.write(key)


    def set_batch_name_and_message(self, batch_name, batch_message):
        with open(self.SETTINGS_FILE, 'r') as file:
            settings = json.load(file)

        if not batch_message and self.utils.str_to_bool(settings['force_message']):
            self.print("Please supply a batch message (-m <message>).", color='yellow')
            self.print("You may turn off mandating of batch message in settings.json")
            return False
        
        if not batch_name and self.utils.str_to_bool(settings['force_batch_name']):
            self.print("Please supply a batch name (-n <name>).", color='yellow')
            self.print("You may turn off mandating of batch name in settings.json")
            return False

        self._batch_name = batch_name
        self._batch_message = batch_message
        return True
    

    def check_batch_name(self):
        batch_name_idx = 1

        if not self._batch_name or not self.utils.is_valid_file_name(self._batch_name):
            self._batch_name = self.utils.get_foramtted_datetime()
            
        # avoid duplicate batch dir names
        elif Path(self.RUNS_DIR, self._sim_name, self._batch_name).exists():
            while Path(self.RUNS_DIR, self._sim_name, f"{self._batch_name}_{str(batch_name_idx)}").exists():
                batch_name_idx = batch_name_idx + 1
            self._batch_name = f"{self._batch_name}_{str(batch_name_idx)}"


    def set_logger(self, log_dir : Path, batch_id=None, run_id=None):
        self._batch_id = batch_id
        self._run_id = run_id

        # log directory might not exist yet when calling from constructor
        if not Path(log_dir).exists():
            log_dir.mkdir(parents=True)

        log_file = f"{Path(log_dir, 'citros.log')}"
        self.log = get_logger(f"{citros_meta.__title__}:{citros_meta.__version__}", 
                              self._batch_id, self._run_id, self.log_level, log_file)


    def handle_exceptions(self, e, exit=False):
        """
        Handles exceptions and logs them.

        Args:
        e: Exception to handle.
        """
        self.print(f"An exception was raised. See log file under {self.CLI_LOGS_DIR} for details" + \
                   f" (or use the -d flag to log to the terminal).", color='red')
        stack_trace = traceback.format_exception(type(e), e, e.__traceback__)
        stack_trace_str = "".join(stack_trace)
        self.log.error(f"Exception details:{linesep}{stack_trace_str}")
        
        if exit:
            shutdown() # flush logger
            exit(3)

    def __enter__(self):
        """
        Returns the Citros instance. This allows the class to be used in a `with` statement.
        """
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Makes sure the stats collecting thread is stopped and handles exceptions.

        Args:
        exc_type: The type of exception.
        exc_val: The exception instance.
        exc_tb: A traceback object encapsulating the call stack at the point 
                where the exception originally occurred.
        """
        self.utils.stop_collecting_stats()
        if exc_type is not None:
            self.handle_exceptions(exc_val, exit=True)


    def _remove_token(self):
        """
        Removes the JWT token.
        """
        self._set_token(None)


    def _validate_token(self, token : str):
        """
        Validates the JWT token.

        Args:
        token: JWT token to validate.

        Returns:
        Boolean indicating if the token is valid.
        """
        try:
            dictionary = jwt.decode(token, options={"verify_signature": False})

            expiration_timestamp = dictionary.get('exp', None)
            if not expiration_timestamp:
                return False
            
            date = datetime.fromtimestamp(expiration_timestamp)
            current_timestamp = datetime.now().timestamp()

            if expiration_timestamp < current_timestamp:
                self.print(f"your login token has expired on {date}", color='yellow', only_verbose=True)
                return False

            return True
        
        except Exception as ex:
            self.handle_exceptions(ex)
            return False


    def _set_token(self, jwt_token):
        """
        Sets the JWT token.

        Args:
        jwt_token: JWT token to set.
        """
        if not jwt_token or jwt_token.strip() == '':
            self._jwt_token = None
            self._token_changed = True
            try:
                auth_path = self.find_auth_key()
                if auth_path is None:
                    raise FileNotFoundError
                os.remove(auth_path)
            except FileNotFoundError as e:
                pass # its ok that there is no file.                
            except Exception as e:
                self.handle_exceptions(e, exit=True)
            return    
        
        if not self._validate_token(jwt_token):
            self.log.error("Invalid JWT token.")
            return
            
        if not self.CITROS_HOME_DIR.is_dir():
            self.CITROS_HOME_DIR.mkdir()

        auth_dir = self.CITROS_REPO_DIR if self.is_initialized else self.CITROS_HOME_DIR
            
        try:
            with open(f"{auth_dir}/auth", mode='w') as file:            
                file.write(jwt_token)      
        except Exception as e:
            self.handle_exceptions(e, exit=True)
        finally:
            self._jwt_token = jwt_token
            self._token_changed = True                        
        
        return self._jwt_token


    def _get_token(self):
        """
        Gets the JWT token.
        """
        try:
            if self._jwt_token:
                # assuming token is valid
                return self._jwt_token
            
            auth_path = self.find_auth_key()
            if auth_path is None:
                raise FileNotFoundError
            
            if auth_path not in self.alternate_auth_paths:
                auth_paths = [auth_path] + self.alternate_auth_paths
            else:
                idx = self.alternate_auth_paths.index(auth_path)
                auth_paths = self.alternate_auth_paths[idx:]

            for path in auth_paths:
                with open(path, mode='r') as file:            
                    self._jwt_token = file.read()
                    self._token_changed = True
                    if not self._validate_token(self._jwt_token):
                        self.log.info(f"JWT token stored at {path} is invalid, removing.")
                        self._remove_token()
                    else:
                        break # valid token found
                    
        except FileNotFoundError as e:
            # Key file wasn't found. assuming the user is not logged in...
            self._jwt_token = None
            return None
        except Exception as e:
            self.handle_exceptions(e, exit=True)

        return self._jwt_token
    
    ############################### login/logout ##############################
    
    def logout(self):
        """
        Logs out of CiTROS
        """
        self._remove_token()
        self._user = None
        
    
    def isAuthenticated(self):
        """
        returns the authentication status

        Returns:
            boolean: True if the user is logged in. 
        """        
        return self._get_token() is not None


    def login(self, email, password):
        """
        Login to CiTROS using an email and password

        Args:
            email (str): the user email 
            password (str): the user's password

        Returns:
            bool: True if the login attempt was successful, False otherwise.
        """                  
        if self.isAuthenticated():
            return True
        
        query = """
            mutation AuthenticateUser($email: Emailtype!, $password: String!) {
                authenticate(input: {
                    email: $email, 
                    password: $password
                }) {
                    jwt
                }
            }
            """        
        result = self.gql_execute(query, variable_values={
            "email": email,
            "password": password
        })

        if result is None or 'authenticate' not in result or 'jwt' not in result['authenticate']:
            self.log.error("Failed to log in. Response: " + str(result))
            return False

        token = result["authenticate"]["jwt"]
        
        try:
            # bug fix. added audience as it didn't work in some cases. 
            decoded = jwt.decode(token, options={"verify_signature": False}, audience="postgraphile")
        except jwt.exceptions.DecodeError as err:
            self.log.error("Failed to log in. token: " + token) 
            self.handle_exceptions(err)
            return False
        
        if token and decoded["role"] != "citros_anonymous":
            self._set_token(token)
            self.log.info("User authenticated.")
            return True
        else:
            msg = f"Authentication attempt failed: wrong username or password for [{email}]"
            self.print(msg, color='red')
            self.log.error(msg)
            return False


    def getUser(self):
        """
        Returns the currently logged in user with all their data from CiTROS.

        This includes their ID, username, role ID and name, and their
        organization's ID, name, and domain prefix.

        Returns:
            dict: The user data, or None if the user is not logged in or an
                  error occurred.
        """           
        if self._user:
            return self._user
        
        query = """
            query getCurrentUser {
                currentUser {  
                    id        
                    email        
                    role{
                        id
                        role
                    }           
                    organization{
                        id 
                        name
                        slug
                    }                    
                }
            }  
            """
        
        try:
            result = self.gql_execute(query)
            if result is None or 'currentUser' not in result:
                self.log.error("Error during getUser: No response or unexpected response format from server.")
                self._user = None
            else:
                self._user = result["currentUser"]
        except Exception as e:
            self.handle_exceptions(e)
            self.logout()

        return self._user
    

    def get_organization_slug(self):
        try:
            user_info = self.getUser()
            prefix = user_info["organization"]["slug"]
        except Exception as ex:
            self.handle_exceptions(ex)
            return None

        return prefix
    
    ################################# Docker #################################
    
    def get_access_token(self, token_url=None):
        """
        Fetches an access token if the user is authenticated.

        Returns:
            str: The access token, or None if the user is not authenticated or an error occurred.
        """
        if not self.isAuthenticated():
            self.print("User is not logged in. Please log in first.", color='yellow')
            return None
        
        if not token_url:
            token_url = self.CITROS_GTOKEN
        
        rest_data = None
             
        try:
            resp = requests.post(token_url, headers={
                "Authorization": f"Bearer {self._get_token()}"
            })
            resp.raise_for_status()     
            rest_data = resp.json()
        except requests.HTTPError as ex:
            self.log.error(f"HTTP error occurred during get_access_token: {token_url}")
            self.handle_exceptions(ex)
            return None
        except requests.RequestException as ex:
            self.log.error(f"A network error occurred during get_access_token: {token_url}")
            self.handle_exceptions(ex)
            return None
        except json.JSONDecodeError as ex:
            self.log.error(f"Failed to decode JSON response during get_access_token: {token_url}")
            self.handle_exceptions(ex)
            return None
        
        try:
            token = rest_data["access_token"]            
            expires_in = rest_data["expires_in"]
            token_type = rest_data["token_type"]
        except KeyError as ex:
            self.log.error("Failed to fetch access token, expected key not found in response.")
            self.handle_exceptions(ex)
            return None
        
        return token
            

    def is_logged_in_to_docker(self):
        # conf_file = Path("~/.docker/config.json").expanduser()
        # if not conf_file.exists():
        #     return False

        # with open(conf_file, 'r') as file:
        #     data = json.load(file)

        # try:
        #     regis = self.DOCKER_REGISTRY.split('/')[0]
        #     token = data['auths'][regis]['auth']
        #     if token:
        #         return True
        #     else:
        #         return False
        # except Exception as ex:
        #     self.log.debug(f"is_logged_in_to_docker: {ex}")
        #     return False
        return False


    def docker_login(self):
        google_access_token = self.get_access_token()
        if google_access_token is None:
            self.print(f"failed to authenticate to SA.", color='red')
            return 
        
        docker.login(server="https://us-central1-docker.pkg.dev", 
                     username="oauth2accesstoken", 
                     password=google_access_token)


    def build_docker_image(self, tags):
        self.print("Building Docker image...")

        assert len(tags) > 0, "tags list cannot be empty"

        target_platform = 'linux/amd64'

        def trim_string(s):
            s = s.strip()

            tokens = s.split()
            
            if tokens:
                tokens.pop(0)

            if tokens and (tokens[0].replace('.', '', 1).isdigit()):
                tokens.pop(0)

            return "=> " + ' '.join(tokens)

        build_logs_iterator = docker.buildx.build(
            context_path=self.USER_PROJ_DIR, 
            tags=tags,
            platforms=[target_platform],
            stream_logs=True
        )
        for log_line in build_logs_iterator:
            self.print(trim_string(log_line), color='blue')

        image = docker.image.inspect(tags[0])
        if not image:
            raise Exception("No image was loaded in the daemon after the build.")
        
        self.print("Done.")


    def image_with_tag_exists(self, image_url, target_tag):
        images = docker.image.list(repository_or_tag=f"{Path(image_url).parent}/*")

        if f"{image_url}:{target_tag}" in str(images):
            return True
        
        return False


    def build_and_push_docker_image(self, image_name):
        if self.try_commit(f"docker-build-push for image {image_name}"):
            self.git_push()
        else:
            return

        slug = self.get_organization_slug()

        if not slug:
            self.log.error("Failed to get organization slug. Cannot push to Docker registry.")
            return False

        try:
            image_url = str(Path(self.DOCKER_REGISTRY, slug, image_name))
            user_commit, _ = self.get_git_info(self.USER_PROJ_DIR)
            tags=[f"{image_url}:{user_commit}", f"{image_url}:latest"]

            self.build_docker_image(tags)

            # if self.image_with_tag_exists(image_url, user_commit):
            #     self.print(f"Image for user commit {user_commit} already exists in registry, no need to push.")
            # else:
            self.print("Pushing Docker image...")
            docker.image.push(f"{image_url}:latest")
            docker.image.push(f"{image_url}:{user_commit}")

            self.print("Done.")
            return True

        except Exception as e:
            self.handle_exceptions(e)
            return False

    ################################# GraphQL #################################
       
    def _get_transport(self):
        """
        Obtain transport with authorization if user is authenticated.
        """                      
        transport = RequestsHTTPTransport(
            url=self.CITROS_ENTRYPOINT,
            verify=True,
            retries=3            
        )     
        # create GQL client for user or for anonymous user. 
        if self.isAuthenticated():
            transport.headers = {
                "Authorization": f"Bearer {self._get_token()}",
                "app" : "citros_cli",
                "version" : citros_meta.__version__
            }
        return transport


    def _get_gql_client(self):
        """
        Obtain GraphQL client.
        """
        if self._gql_client and not self._token_changed:
            return self._gql_client
        # https://gql.readthedocs.io/en/v3.0.0a6/intro.html
        transport = self._get_transport()
        self._gql_client = Client(transport=transport, fetch_schema_from_transport=False)
        self._token_changed = False
        return self._gql_client


    def gql_execute(self, query, variable_values=None):
        """
        Execute a GraphQL query.

        Args:
            query (gql): gql query
            variable_values (dict, optional): variables for the gql query. Defaults to None.

        Returns:
            dict: Result of the executed query.
        """
        
        gql_query = gql(query)
        try:
            return self._get_gql_client().execute(gql_query, variable_values=variable_values)
        except TransportQueryError as ex:
            safe_variable_values = dict(variable_values)
            if "password" in safe_variable_values:
                safe_variable_values["password"] = "REDACTED"
            self.log.error(f"Error while querying: query={query} variable_values={safe_variable_values}")

            self.handle_exceptions(ex)

            if ex.errors[0].get('errcode', '') == "23514":
                self.print("The email you provided is not valid.", color='red')
            if ex.errors[0].get('errcode', '') == "23503":
                self.logout()
        except Exception as ex:    
            self.log.error(f"Error while querying: query={query} variable_values={variable_values}")
            self.handle_exceptions(ex)
                           
        return None
    
    ####################### simulation attributes getters #####################

    def get_simulation_info(self, simulation_name : str):
        if not simulation_name.endswith('.json'):
            simulation_name = simulation_name + '.json'
            
        try:
            with open(Path(self.SIMS_DIR, simulation_name), 'r') as f:
                data = json.load(f)
        except FileNotFoundError as ex:
            self.log.error(f"simulation file {simulation_name} does not exist.")
            raise ex

        return data


    def get_package_name(self, launch_name : str):
        with open(self.PROJECT_FILE, 'r') as f:
            data = json.load(f)
            
        for package in data['packages']:
            for launch in package['launches']:
                if launch['name'] == launch_name:
                    package_path = package['path']
                    if Path(package_path, 'package.xml').exists():
                        return Path(package_path).name  
                    
        # If no matching launch or package is found
        return None

    ############################### CITROS list ###############################
    
    def get_simulations(self):
        path = self.SIMS_DIR
        sims = []
        if path.is_dir():
            if self._has_files(path):
                for file in path.iterdir():
                    if not str(file).endswith('.json'):
                        continue
                    sim = file.name.split('.')[0]
                    sims.append(sim)    
        return sims
    
    #################### initialization and validation ########################

    def _has_files(self, dir : Path):
        return any(p.is_file() for p in dir.iterdir()) 
    

    def _validate_json_file(self, json_filepath, schema_filepath):
        with open(json_filepath, 'r') as file:
            data = json.load(file)

        with open(schema_filepath, 'r') as file:
            schema = json.load(file)

        try:
            jsonschema.validate(instance=data, schema=schema)
            self.print(f"{json_filepath} is valid.", only_verbose=True)
            return True
        except jsonschema.exceptions.ValidationError as ve:
            self.log.error(f"{json_filepath} is not valid:{linesep}{ve}")
            return False


    def _get_schema_path(self, schema_file):
        return importlib.resources.path(f'data.schemas', schema_file)


    def _get_default_file_path(self, default):
        return importlib.resources.path(f'data.defaults', default)


    def _copy_default_file(self, default_file_path, destination):
        shutil.copy2(Path(default_file_path), destination)


    def _validate_file(self, file_path : Path, schema_file, default):
        if file_path.is_file():
            with self._get_schema_path(schema_file) as schema_path:
                return self._validate_json_file(str(file_path), schema_path)
        elif default:
            with self._get_default_file_path(default) as default_file:
                self._copy_default_file(default_file, file_path)
                return True
        else:
            return False


    def _validate_dir(self, path : Path, schema_file, default):
        if path.is_dir() and self._has_files(path):
            with self._get_schema_path(schema_file) as schema_path:
                for file in path.iterdir():
                    if str(file).endswith('json'):
                        if not self._validate_json_file(file, schema_path):
                            return False
                return True
        elif default:
            with self._get_default_file_path(default) as default_file:
                self._copy_default_file(default_file, Path(path, default))
                return True
        else:
            # empty folder is valid
            return True


    def _get_launches_info(self, proj_json: Path):
        with open(proj_json, 'r') as file:
            data = json.load(file)

        launch_info = []

        for package in data.get('packages', []):
            for launch in package.get('launches', []):
                if 'name' in launch:
                    launch_info.append((package.get('name', ''), launch['name']))
        
        return launch_info


    def _check_sim_file_contents(self, sim_file):
        with open(sim_file, 'r') as file:
            sim_data = json.load(file)

        param_setup = sim_data["parameter_setup"]
        launch_file = sim_data["launch"]["file"]
        
        if not Path(self.PARAMS_DIR, param_setup).exists():
            self.print(f"Could not find parameter setup file {param_setup} referenced in {sim_file}.", color='red')
            return False
        
        all_launch_names = [launch[1] for launch in self._get_launches_info(self.PROJECT_FILE)]
        if launch_file not in all_launch_names:
            self.print(f"Could not find launch file named {launch_file} referenced in {sim_file}.", color='red')
            return False
        
        return True
                
    
    def _validate_citros_files(self, create_default_if_empty : bool):
        """
        Assumption: project.json exists.
        """
        success = self._validate_dir(self.PARAMS_DIR, 'schema_param_setup.json', None)
        
        success = success and \
                  self._validate_dir(self.SIMS_DIR, 
                                    'schema_simulation.json', 
                                    'default_simulation.json' if create_default_if_empty else None)

        success = success and \
                  self._validate_dir(self.WORKFLOWS_DIR, 
                                    'schema_flow.json', 
                                    'default_flow.json' if create_default_if_empty else None)
        
        success = success and \
                  self._validate_file(self.SETTINGS_FILE, 
                                     'schema_settings.json',
                                     'default_settings.json')
        return success


    def _create_folders(self):
        if not self.CITROS_REPO_DIR.is_dir():
            self.CITROS_REPO_DIR.mkdir(parents=True)

        if not self.SIMS_DIR.is_dir():
            self.SIMS_DIR.mkdir(parents=True)

        if not self.PARAMS_DIR.is_dir():
            self.PARAMS_DIR.mkdir(parents=True)

        if not self.NOTEBOOKS_DIR.is_dir():
            self.NOTEBOOKS_DIR.mkdir(parents=True)

        if not self.WORKFLOWS_DIR.is_dir():
            self.WORKFLOWS_DIR.mkdir(parents=True)

        if not self.REPORTS_DIR.is_dir():
            self.REPORTS_DIR.mkdir(parents=True)

        if not self.RUNS_DIR.is_dir():
            self.RUNS_DIR.mkdir(parents=True)


    def _get_project_name(self):
        proj_file_path = self.PROJECT_FILE
        if proj_file_path.exists():
            with open(proj_file_path, "r") as proj_file:
                proj_file_data = json.load(proj_file)
                return proj_file_data.get("name", "")
        
        # return user's project directory name by default
        return self.USER_PROJ_DIR.name


    def _create_simulations(self):
        """
        create a default simulation.json for every launch file in the project.
        """
        if self.PROJECT_FILE.exists():
            launch_infos = self._get_launches_info(self.PROJECT_FILE)
            for package_name, launch_file in launch_infos:
                launch_name = launch_file.split('.')[0]

                with self._get_default_file_path('default_simulation.json') as default_file:
                    sim_file_path = str(Path(self.SIMS_DIR, f"simulation_{launch_name}.json"))
                    self._copy_default_file(default_file, sim_file_path)

                    with open(sim_file_path, 'r') as sim_file:
                        sim_json = json.load(sim_file)
                          
                    sim_json["launch"]["file"] = launch_file
                    sim_json["launch"]["package"] = package_name
                    
                    with open(sim_file_path, 'w') as sim_file:
                        json.dump(sim_json, sim_file, indent=4)


    def _create_gitignore(self):
        if not Path(self.CITROS_REPO_DIR, '.gitignore').exists():
            with open(Path(self.CITROS_REPO_DIR, '.gitignore'), 'w') as file:
                ignores = linesep.join(['runs/', 'auth']) # add more as needed.
                file.write(ignores)


    def _save_user_commit_hash(self):
        user_commit, _ = self.get_git_info(self.USER_PROJ_DIR)

        with open(Path(self.CITROS_REPO_DIR, 'user_commit'), 'w') as file:
            file.write(user_commit)


    def create_gitkeep_in_empty_dirs(self, ignored = []):
        for root, dirs, files in os.walk(str(self.CITROS_REPO_DIR)):
            if not dirs and not files and not root in ignored:
                gitkeep_file = Path(root, '.gitkeep')
                open(gitkeep_file, 'a').close()


    def internal_sync(self, on_init=False):
        # no synching or validation is done on the cluster - there is no user code.
        if self.CITROS_ENVIRONMENT == 'CLUSTER':
            return True

        self._create_folders()
        
        self.sync_project(self._get_project_name())

        if on_init:
            self._create_simulations()
            self._create_gitignore()

        success = self._validate_citros_files(on_init)

        at_least_one_sim = False

        for file in self.SIMS_DIR.iterdir():
            if str(file).endswith('.json'):
                at_least_one_sim = True
                success = success and self._check_sim_file_contents(file)

        if not at_least_one_sim:
            self.log.error(f"No simulation file found in {self.SIMS_DIR}")
            success = False

        self.create_gitkeep_in_empty_dirs([str(self.RUNS_DIR)])

        return success


    def check_project(self, on_init=False):
        if self.CITROS_REPO_DIR.exists():
            self.internal_sync(on_init)
            return True
        else:
            return False


    def sync_project(self, name):
        project_data = self.parser_ros2.parse(str(self.USER_PROJ_DIR), name)
        with open(self.PROJECT_FILE, 'w') as file:
            json.dump(project_data, file, sort_keys=True, indent=4)
        
        self.parser_ros2.generate_default_params_setup(self.PROJECT_FILE, 
                                                       Path(self.PARAMS_DIR,
                                                            'default_param_setup.json'))


    ############################## git ########################################

    def is_repo_empty(self, repo : git.Repo):
        items = os.listdir(repo.working_dir)

        items = [item for item in items if item != '.git']

        return len(items) == 0


    def check_uncommitted_changes(self, repo_path):
        repo = git.Repo(repo_path)
        return repo.is_dirty(untracked_files=True)
    

    def get_git_info(self, repo_path='.'):
        repo = git.Repo(repo_path)

        latest_commit_hash = repo.head.commit.hexsha
        current_branch_name = repo.active_branch.name

        return latest_commit_hash, current_branch_name


    def check_remotes(self):
        repo = git.Repo(self.CITROS_REPO_DIR)
        return len(repo.remotes) > 0


    def try_commit(self, message=""):
        user_dirty = self.check_uncommitted_changes(self.USER_PROJ_DIR)
        if user_dirty:
            self.log.error("Cannot commit: there are uncommitted changes in the user's repository.")
            self.print("Commit changes in your ROS project and try again.", color='yellow')
            return False

        success = self.internal_sync()
        if not success:
            self.log.error("Cannot commit: internal sync failed.")
            self.print("Commit failed. Fix errors and try again.", color='red')
            return False
        
        self._save_user_commit_hash()

        if not self.check_uncommitted_changes(self.CITROS_REPO_DIR):
            self.log.debug("try_commit: nothing to commit.")
            return True

        try:
            repo = git.Repo(self.CITROS_REPO_DIR)

            # Add and commit all files.
            # since we don't specify an author or committer, 
            # GitPython will use the configurations user.name and user.email 
            # from the git configuration as the author and committer.
            repo.git.add(A=True)
            repo.index.commit(message)
            return True
        except Exception as ex:
            self.handle_exceptions(ex)
            return False
        

    def git_push(self, branch='master'):
        try:
            repo = git.Repo(self.CITROS_REPO_DIR)

            if self.check_remotes():
                repo.remotes.origin.push(refspec=f"{branch}:{branch}")
            else:
                self.print(f"cannot push - no remote defined for repo {self.CITROS_REPO_DIR}", color='red')
        except Exception as ex:
            self.handle_exceptions(ex, exit=True)


    def git_pull(self, branch='master'):
        try:
            repo = git.Repo(self.CITROS_REPO_DIR)

            if self.check_remotes():
                if repo.active_branch != branch:
                    repo.git.checkout(branch)
                repo.remotes.origin.pull(branch)
            else:
                self.print(f"cannot pull - no remote defined for repo {self.CITROS_REPO_DIR}", color='red')
        except Exception as ex:
            self.handle_exceptions(ex, exit=True)


    def update_gitignore(self, repo_path, pattern):
        # Create .gitignore if it doesn't exist
        gitignore_path = Path(repo_path, ".gitignore")
        if not gitignore_path.exists():
            open(gitignore_path, 'a').close()

        def normalize_pattern(pattern):
            # Remove any trailing slash or asterisk
            return pattern.rstrip('*/')
            
        normalized_pattern = normalize_pattern(pattern)

        # Check if pattern exists in the .gitignore
        with open(gitignore_path, 'r+') as gitignore:
            lines = gitignore.readlines()
            for line in lines:
                if normalize_pattern(line.strip()) == normalized_pattern:
                    # pattern already exists in .gitignore.
                    return

            # Pattern not found in .gitignore, append it
            gitignore.write(linesep + pattern + {linesep})
            self.print(f"Pattern `{pattern}` appended to .gitignore in {repo_path}")

   
    def get_project_remote(self, encode=True):
        url = self.parser_ros2.get_git_remote_url(self.USER_PROJ_DIR)    
        if url:
            if encode:
                return self.utils.encode64(url)
            else:
                return url
        else:
            self.log.error("Could not obtain git remote url for user's project.")
            self.print(f"Make sure your project has a remote named `origin`.{linesep}" + \
                       f"If you're working inside a devcontainer, " + \
                       f"make sure your project is not a git sub-module.", color='red')
            return None
    

    def api_upsert_repo(self, name, origin):
        query = """
                mutation MyMutation($name: String!, $origin: String) {
                    upsertRepo(input: {repo: {name: $name, origin: $origin}}){
                        repo{
                            id
                        }
                    }
                }
                """
        result = self.gql_execute(query, variable_values={
            "name": name,
            "origin": origin
        })

        if result is None:
            raise Exception(f"Failed to upsert repo {name} ({origin}) to Citros.")
        
        self.repo_id = result['upsertRepo']['repo']['id']
    

    def get_citros_remote(self):
        return self.parser_ros2.get_git_remote_url(self.CITROS_REPO_DIR, True)    
        

    def get_citros_remote_from_api(self):
        name = self._get_project_name()
        origin = self.get_project_remote(False) 
        self.api_upsert_repo(name ,origin)

        organization = self.get_organization_slug()
        remote_url = f"{self.CITROS_GIT_URL}:{organization}/{name}.git"
        return remote_url


    def clone_repo(self, repo_path, repo_url):
        if not Path(repo_path).exists():
            try:
                repo = git.Repo.clone_from(repo_url, repo_path)
                self.log.info(f"Repository cloned from {repo_url} to {repo_path}.")
                return repo
            except git.exc.NoSuchPathError as ex:
                self.log.error(f"Clone failed: the path {repo_path} does not exist.")
                raise ex
            except git.exc.InvalidGitRepositoryError as ex:
                self.log.error(f"Clone failed: the URL {repo_url} is not a git repository.")
                raise ex
            except git.exc.GitCommandError as ex:
                self.log.error("Failed to clone repository.")
                raise ex
        else:
            self.log.warning(f"Repository already exists at {repo_path}.")
            return git.Repo(repo_path)


    def add_remote(self, repo_path, remote_name, remote_url):
        try:
            repo = git.Repo(repo_path)

            remotes = [remote.name for remote in repo.remotes]

            if remote_name in remotes:
                self.log.info(f"remote {remote_name} already exists.")
                return True

            remote = repo.create_remote(remote_name, remote_url)
            return True
        except git.exc.GitCommandError as ex:
            self.print("Failed to add remote repository.", color='red')
            self.handle_exceptions(ex)
            return False


    def get_username_and_hostname(self):
        import socket
        import getpass

        user = getpass.getuser() 
        hostname = socket.gethostname()
        return f"{user}@{hostname}"


    def setup_ssh(self):
        public_key = None
        key_name = self.utils.check_ssh_key_pair()
        if not key_name:
            public_key = self.utils.create_ssh_key_pair()
            key_name = self.utils.check_ssh_key_pair()
        else:
            with open(Path(Path("~/.ssh").expanduser(), f"{key_name}.pub"), "r") as key_file:
                public_key = key_file.read()
        
        if not self.utils.check_ssh_key_uploaded(key_name):
            if not self.isAuthenticated:
                print("You are not logged in and have not yet uploaded ssh keys to citros. Login and try again.")
                raise ValueError("not logged in when trying to upload ssh keys to citros.")

            self.upload_ssh_key(public_key, f"{self.get_username_and_hostname()}")

    
    def upload_ssh_key(self, pub_key, title):
        self.log.debug(f"upload_ssh_key: pub_key = {pub_key}, title  = {title}")

        query = """
                    mutation addSSHKey($title: String, $key: String) {
                        createSshKey(input: {sshKey: {key: $key, title: $title}}){
                            sshKey{
                            id
                            }
                        }
                    }
                """
        
        result = self.gql_execute(query, variable_values={
            "key": pub_key,
            "title": title
        })

        if result is None:
            raise Exception("Failed to upload SSH key to Citros.")


    def wait_till_repo_ready(self):
        timeout = 1.0

        slug = self.get_organization_slug()
        proj_name = self._get_project_name()

        while not self.utils.is_repo_ready(slug, proj_name):
            time.sleep(timeout)
            timeout = timeout * 2

            if timeout > 60:
                self.log.error("wait_till_repo_ready: timed out.")
                return False

        return True
        

    ############################## RUN ########################################
    
    def create_sim_run_dir(self, run_id):
        runs_dir = self.RUNS_DIR if self.CITROS_ENVIRONMENT != "CLUSTER" else \
                   Path("/var/lib/citros/runs")

        run_dir = Path(runs_dir, self._sim_name, self._batch_name, str(run_id))
        run_dir.mkdir(parents=True, exist_ok=False)
        self.SIM_RUN_DIR = str(run_dir)
        self.BAG_DIR = str(Path(self.SIM_RUN_DIR, 'bag'))
        self.MSGS_DIR = str(Path(self.SIM_RUN_DIR, 'msgs'))

        self.print(f"simulation run dir = [{self.SIM_RUN_DIR}]", only_verbose=True )


    def copy_msg_files(self):
        #sanity check
        if self.MSGS_DIR is None:
            self.log.error("MSG_DIRS has not been created.")
            return
        
        msg_paths = self.parser_ros2.get_msg_files(self.USER_PROJ_DIR)
        for msg_path in msg_paths:
            # assuming msg files are under package_name/msg/
            package_name = Path(msg_path).parent.parent.name
            target_dir = Path(self.MSGS_DIR, package_name, 'msg')
            self.utils.copy_files([msg_path], str(target_dir), True)


    def save_run_info(self):
        bag_hash = self.utils.compute_sha256_hash(Path(self.BAG_DIR, self.BAG_NAME))
 
        batch = self.batch.get_batch(self._batch_id, self._sim_name)

        with open(Path(self.SIM_RUN_DIR).parent / 'info.json', 'w') as sim_file:
            json.dump(batch, sim_file, indent=4)

        batch['batchId'] = self._batch_id
        batch['bagHash'] = bag_hash
        batch['id'] = self._run_id

        with open(Path(self.SIM_RUN_DIR, 'info.json'), 'w') as sim_file:
            json.dump(batch, sim_file, indent=4)
        

    def save_system_vars(self):
        # Get all environment variables
        env_vars = dict(os.environ)
        
        pip_freeze_output = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
        
        if pip_freeze_output.returncode != 0:
            self.log.error('pip freeze failed: ' + pip_freeze_output.stderr)
            python_packages = []
        else:
            python_packages = pip_freeze_output.stdout.split(linesep)

        data = {'environment_variables' : env_vars,
                'python_packages' : python_packages
                }
        
        with open(Path(self.SIM_RUN_DIR, 'environment.json'), 'w') as f:
            json.dump(data, f, indent=4)


    def save_run_data(self):
        self.copy_msg_files()
        self.save_run_info()
        self.save_system_vars()


    def single_simulation_run(self, batch_id, run_id, timeout):   
        # running inside ROS workspace context.  
        from launch import LaunchService 
        from citros.launches import generate_launch_description  

        self.print(f" + + running simulation [{run_id}]", color='blue')  

        self.create_sim_run_dir(run_id)
        
        self.set_logger(self.SIM_RUN_DIR, batch_id, run_id)

        launch_description = generate_launch_description(self, str(timeout))

        if launch_description is None:
            msg = f"Couldn\'t run run_id:[{run_id}]. Failed to create launch_description."
            self.log.error(msg)
            return
            # sys.exit(msg)
        
        launch_service = LaunchService(debug=(self.log_level == 'debug'))
        launch_service.include_launch_description(launch_description)

        self.utils.start_collecting_stats(self.STATS_INTERVAL, Path(self.SIM_RUN_DIR, 'metrics.csv'))

        ret = launch_service.run()

        self.utils.stop_collecting_stats()

        self.print(f" - - Finished simulation run_id = [{run_id}] with return code [{ret}].", color='blue') 

        self.save_run_data()


    def run_batch(self, batch_id, timeout, completions, description=""):
        self.print(f" + running batch [{batch_id}], description: {description}, repeating simulations: [{completions}]", color='blue')

        for run_id in range(0, completions):
            try:
                self.single_simulation_run(batch_id, run_id, timeout)                   
                time.sleep(1)
            except Exception as e:
                self.print("------------------------")   
                self.print (e, color='red')
                traceback.print_exc()
                self.print("------------------------")
                continue

        self.print(f" - Finished [{batch_id}] batch.", color='blue')


    def run_simulation_by_k8s(self, batch_id, run_id, timeout):
        """
        Used by the the Kubernetes cluster to run a single simulation run.
        Kubernetes runs this function as a `job`, a given number of times.
        The environment variable JOB_COMPLETION_INDEX will hold the index 
        of the current run (run_id). The command Kubernetes runs is:
        citros run <batch_id> JOB_COMPLETION_INDEX 
        This is how looping over all the batch runs is implemented on the cluster.
        
        Assumption: user is logged in, so we can query the db to get the 
                    simulation name given the batch_id.
        """
        if run_id == "JOB_COMPLETION_INDEX":
            run_id = config("JOB_COMPLETION_INDEX", "bad-value-from-k8s")
            self.log.info(f"got JOB_COMPLETION_INDEX={run_id} from k8s.")
        else:
            raise Exception("run_simulation_by_k8s: Expected run_id to be JOB_COMPLETION_INDEX")

        if run_id == "bad-value-from-k8s":
            raise Exception("run_simulation_by_k8s: bad value from k8s")
        
        # raise if not logged in
        batch = self.batch.get_batch(batch_id)

        self.events.otlp_context = batch["metadata"]
        
        # raise on error
        self._sim_name = str(batch["simulation"])

        self.check_batch_name()
        
        self.log.info(f"running a single simulation run from batch [{batch_id}]")
        self.single_simulation_run(batch_id, run_id, timeout)


    def run_simulation(self, sim_name, completions, timeout, remote):      
        where = "locally" if not remote else "on Citros cluster"

        cpu = self.get_simulation_info(sim_name)['CPU']
        gpu = self.get_simulation_info(sim_name)['GPU']
        mem = self.get_simulation_info(sim_name)['MEM']

        #remove `MB``
        mem = mem[:-2]

        # sanity check
        if remote and not self.repo_id:
            raise Exception("run_simulation: repo id is None")

        self._sim_name = sim_name
        self.check_batch_name()

        user_commit, user_branch = self.get_git_info(self.USER_PROJ_DIR)
        citros_commit, citros_branch = self.get_git_info(self.CITROS_REPO_DIR)

        batch_id = self.batch.generate_batch_id()

        # start the open-telemetry trace.
        self.events.creating(batch_id)

        self.log.info(f"created new batch_id: {batch_id}. Running {where}.")

        # create a new batch for this simulation. 
        # if remote is True, than the query to the db will trigger the Kubernetes 
        # worker to start the simulation on the cluster.
        if remote:
            batch_id = self.batch.create_batch(batch_id, self.repo_id, sim_name, gpu, cpu, mem, completions,
                                               user_commit, user_branch, citros_commit, citros_branch,
                                               name=self._batch_name, message=self._batch_message, 
                                               metadata=self.events.otlp_context)
            return
        
        self.run_batch(batch_id, timeout, completions, self._batch_message)