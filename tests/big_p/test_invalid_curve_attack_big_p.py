# Standard Library Imports
import json
import logging
import os
import sys
import unittest

# Ensure correct path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Third-Party / SageMath Imports
from sage.all import Integer

# Local Imports
from invalid_curve_attack import run_attack, load_invalid_curves_from_params
from .server_test_big_p import server_oracle, secret

# Setup logging for debugging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def oracle(P):
    return server_oracle(P.xy())

class TestInvalidCurveAttackWithServer(unittest.TestCase):
    def setUp(self):
        """Load attack parameters from generated test_invalid_curves.json."""
        self.attack_dict_file = os.path.join(os.path.dirname(__file__), "test_invalid_curves.json")
        # Ensure file exists before loading
        self.assertTrue(os.path.exists(self.attack_dict_file), "Attack dictionary file does not exist!")
        with open(self.attack_dict_file, "r") as f:
            self.attack_dict = json.load(f)
        self.b = 41058363725152142129326129780047268409114441015993725554835256314039467401291  # secp b

    def test_load_invalid_curves(self):
        """Test loading precomputed invalid curves."""
        E, G0, params = load_invalid_curves_from_params(self.attack_dict, self.b)
        self.assertIsNotNone(E)
        self.assertIsNotNone(G0)
        self.assertGreater(len(params), 0)
        logging.info("Precomputed invalid curves loaded successfully.")

    def test_run_attack_with_server(self):
        """Test executing the attack using the real server_oracle."""
        result = run_attack(self.attack_dict_file, oracle, self.b)
        
        self.assertIsNotNone(result, "Attack failed to compute discrete log!")
        if isinstance(result, (int,Integer)):
            self.assertGreater(result, 0, "Discrete log result should be positive.")
            self.assertEqual(result, secret, "Recovered the Secret")
        else:
            self.assertGreater(len(result), 0, "Attack did not produce valid logs and moduli.")
        logging.info(f"Attack completed. Result: {result}")

if __name__ == "__main__":
    unittest.main()
