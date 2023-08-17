# to run: python3 -m pytest test_eval_distribution.py

import pytest
from citros.citros_params import citros_params  # replace with the actual import path
from citros import Citros  # replace with the actual import path
import numpy as np

def test_eval_distribution():
	# instantiate your class
	with Citros() as citros:
		cparams = citros_params(citros)

		# case 1: distribution_type = STRING
		parameter_setting = {
			"distribution_type": "STRING",
			"distribution_param1": "foo"
		}
		assert cparams._eval_distribution(parameter_setting) == "foo"

		# case 2: distribution_type = FLOAT, param1_type = FLOAT
		parameter_setting = {
			"distribution_type": "FLOAT",
			"distribution_param1": 1.5,
			"param1_type": "FLOAT"
		}
		assert cparams._eval_distribution(parameter_setting) == 1.5

		# case 3: distribution_type = FLOAT, param1_type = INT
		parameter_setting = {
			"distribution_type": "FLOAT",
			"distribution_param1": 1.5,
			"param1_type": "INT"
		}
		assert cparams._eval_distribution(parameter_setting) == 1.5

		# for deterministic results
		np.random.seed(0)

		# case 4: distribution_type = NORMAL
		parameter_setting = {
		"distribution_type": "NORMAL",
		"distribution_param1": 0,  # mean
		"param1_type": "FLOAT",
		"distribution_param2": 1,  # standard deviation
		"param2_type": "FLOAT"
		}
		results = [cparams._eval_distribution(parameter_setting) for _ in range(100)]
		assert min(results) > -5 and max(results) < 5

		# Add additional cases for each distribution_type
		# Note: the exact values are dependent on the numpy random seed and could be different with another seed or without it.
		distributions = [
		("EXPONENTIAL", 0.1, "FLOAT", None, "FLOAT", 0, 20),  # exponential distribution with scale of 0.1, expected range is 0 to ~20
		("LAPLACE", 0, "FLOAT", 1, "FLOAT", -10, 10),  # laplace distribution with mean 0 and scale of 1, expected range is -10 to 10
		("POISSON", 1, "INT", None, "FLOAT", 0, 6),  # poisson distribution with lambda=1, expected range is 0 to 6
		("POWER", 1, "FLOAT", None, "FLOAT", 0, 1),  # power distribution with a=1, expected range is 0 to 1
		("UNIFORM", -1, "FLOAT", 1, "FLOAT", -1, 1),  # uniform distribution between -1 and 1
		("ZIPF", 1.5, "FLOAT", None, "FLOAT", 1, np.inf),  # zipf distribution with a=1.5, expected minimum is 1
		("VONMISES", 0, "FLOAT", 1, "FLOAT", -np.pi, np.pi),  # vonmises distribution with mean 0 and dispersion of 1, expected range is -pi to pi
		("RAYLEIGH", 1, "FLOAT", None, "FLOAT", 0, 5),  # rayleigh distribution with scale of 1, expected range is 0 to ~5
		]

		for i, (distribution_type, param1, param1_type, param2, param2_type, min_value, max_value) in enumerate(distributions):
			parameter_setting = {
					"distribution_type": distribution_type,
					"distribution_param1": param1,
					"param1_type": param1_type,
			}
			if param2 is not None:
					parameter_setting["distribution_param2"] = param2
					parameter_setting["param2_type"] = param2_type
			results = [cparams._eval_distribution(parameter_setting) for _ in range(100)]
			assert min(results) >= min_value and max(results) <= max_value, f"Test case {i + 4} failed"

