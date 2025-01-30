# Standard Library Imports
import json
import logging
import os
import sys
import unittest
from unittest.mock import patch

# Ensure correct path for local imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Local Imports
from invalid_curve_generator import InvalidCurveGenerator



# Setup logging for debugging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

### Smaller p for easier testing


class TestInvalidCurveGenerator(unittest.TestCase):
    def setUp(self):
        """Initialize test parameters."""
        # x^3 + 115792089210356248762697446949407573530086143415290314195533631308867097853948*x + 41058363725152142129326129780047268409114441015993725554835256314039467401291
        self.p = 183864092725132365247326101  # Prime number for finite field GF(p)
        self.a = 35464063352748132137167577  # Coefficient a of the elliptic curve
        self.generator = InvalidCurveGenerator(self.p, self.a, timeout=1, timeout_max=5, factor_ints=True, proof=True, deep=True)

    def test_generate_random_curves(self):
        """Test random invalid curve generation."""
        logging.info("Testing random invalid curve generation.")
        curves = self.generator.generate_curves(target=3, g0=True)
        self.assertEqual(len(curves), 3)
        for curve in curves:
            self.assertIn('b', curve)
            self.assertIn('order', curve)
            self.assertIn('factors', curve)

    def test_generate_targeted_curves(self):
        """Test targeted curve generation with predefined b values."""
        logging.info("Testing targeted invalid curve generation with predefined b values.")
        
        logging.info("Testing handling of invalid b values.")
        invalid_b_values = [-1, 0, self.p + 1]
        for b in invalid_b_values:
            with self.assertRaises(ValueError):
                self.generator.generate_curves(b_values=[b], g0=True)

        logging.info("Testing handling of valid b values.")
        # 🟢 Test valid b values (should generate curves successfully)
        valid_b_values = [26817580302667750510556583, 130818225255654574185820382, 55792094497497749139358188]
        curves = self.generator.generate_curves(b_values=valid_b_values, g0=True)
        
        self.assertEqual(len(curves), 3)  # Ensure 3 curves were generated
        for curve in curves:
            self.assertIn('b', curve)
            self.assertIn('order', curve)
            self.assertIn('factors', curve)

    def test_invalid_curve_output(self):
        """Test saving generated curves to a JSON file."""
        output_file = os.path.join(os.path.dirname(__file__), "test_invalid_curves.json")
        logging.info("Testing invalid curve output saving to file.")
        self.generator.generate_curves(target=12, g0=True, save_path=output_file)
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r") as f:
            data = json.load(f)
        self.assertIn("curve_params", data)
        self.assertIn("curves", data)
        logging.info("Invalid curve output successfully saved.")
        # os.remove(output_file)  # Keep file for later tests


if __name__ == "__main__":
    unittest.main()
