# **Invalid Curve Attack Implementation**

This repository provides an implementation of the **Invalid Curve Attack** on **Elliptic Curve Cryptography (ECC)** using **SageMath**. It supports both small and large prime field sizes for performance flexibility.

## **📌 Features**

- **Invalid Curve Attack**: Exploits weak implementations of ECC.
- **Precomputed Attack Option**: Load precomputed invalid curves for faster execution.
- **Custom Curve Generation**: Generate invalid elliptic curves dynamically.
- **Supports Two Test Modes**:
  - **`small_p`**** tests**: Suitable for lower computational resources.
  - **`big_p`**** tests**: Uses real-world cryptographic curves (e.g., `secp256r1` / `NIST P-256`).
- **Modular & Expandable**: Easily integrate into larger cryptanalysis tools.
- **Uses SageMath** for ECC calculations.
- **Includes a lightly modified server implementation from HTB Challenge 400 Curves.**

## **📂 Project Structure**

```
📁 invalid_curve_attack/          # Main directory
│── invalid_curve_attack.py      # Attack execution script
│── invalid_curve_generator.py   # Generates invalid elliptic curves
│── logger.py                    # Logging utility
│── shared/
│   ├── factor_help.py           # Integer factorization utilities
│   ├── run_timeouts.py          # Timeout handling functions
│
📁 tests/                        # Test cases
│── small_p/                     # Tests with small prime field sizes
│   ├── test_invalid_curve_generator_small_p.py
│   ├── test_invalid_attack_small_p.py
│── big_p/                       # Tests with large cryptographic primes
│   ├── test_invalid_curve_generator_big_p.py
│   ├── test_invalid_attack_big_p.py
```

## **🚀 Installation & Requirements**

### **1️⃣ Install SageMath**

The project requires **SageMath**, which includes the necessary ECC libraries.

🔹 Install SageMath:

```bash
sudo apt install sagemath  # Ubuntu/Debian
brew install sagemath      # macOS (Homebrew)
```

Alternatively, download it from: [SageMath Official Website](https://www.sagemath.org/download.html)

### **2️⃣ Install Dependencies**

Run the following command to install additional Python dependencies:

```bash
pip install requests factordb-pycli
```

## **⚡ Usage**

### **1️⃣ Generate Invalid Curves**

Run the **invalid curve generator** to create **precomputed attack parameters**:

```bash
python invalid_curve_generator.py --p <prime> --a <curve_a> --x <num_curves>
```

#### **📌 Explanation of Arguments for Curve Generation:**

- `--p <prime>`: Defines the prime field modulus `p`.
- `--a <curve_a>`: Specifies the `a` parameter in the elliptic curve equation.
- `--factor`: Enables factorization of the curve order.  _Optional_
- `--proof`: Ensures all factors are prime (only applicable if `--factor` is set).  _Optional_
- `--g`: Includes generator points in the output.  _Optional_
- `--d`: Enables deep factorization using ECM.  _Optional_
- `--t <timeout>`: Timeout for order calculation (default: 5 seconds). _Optional_
- `--target_len <length>`: Minimum required number of factors.  _Optional_
- `--output <file>`: Saves the generated curves to a JSON file. _Optional but recommended_
- `--x <num_curves>`: Number of random invalid curves to generate. _One of those is required_
- `--numbers <file_or_list>`: Specific `b` values (instead of random ones). _One of those is required_
- `--range <start,end>`: Generate curves for a range of `b` values. _One of those is required_

- Example for **NIST P-256**:

```bash
python invalid_curve_generator.py --p 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff \
                                  --a 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc \
                                  --x 10 --output invalid_curves.json
```

### **2️⃣ Run the Attack**

Once invalid curves are generated, use them to execute the attack:

**Note:** `invalid_curve_attack.py` is **not** designed to be run from the CLI. Instead, import and use it as follows:

```python
from invalid_curve_attack import run_attack

b = original_b_from_the_servers_curve
attack_dict_file = "curve_params.json"

def oracle(P):
   result = server_function_that_multiplies_P_with_secret(P)
   return result

run_attack(attack_dict_file, oracle, b)
```

### **3️⃣ Run Tests**

#### **Small Prime Field Tests**

```bash
python -m unittest tests/small_p/test_invalid_curve_generator_small_p.py
python -m unittest tests/small_p/test_invalid_curve_attack_small_p.py"
```

#### **Big Prime Field Tests**

```bash
python -m unittest tests/big_p/test_invalid_curve_generator_big_p.py
python -m unittest tests/big_p/test_invalid_curve_attack_big_p.py"
```

## **🔬 How It Works**

1. **Invalid Curve Generation:**
   - Modifies the `b` coefficient in the ECC equation:
     ```
     y² = x³ + ax + b (mod p)
     ```
   - Ensures the new curve has small order factors.
2. **Invalid Curve Attack Execution:**
   - Uses an oracle function (e.g., an ECC server) to exploit incorrect curve handling.
   - Computes **discrete logarithm leaks** to recover the private key.

## **⚠️ Disclaimer**

🚨 **This project is for educational and research purposes only.** Do not use it for unauthorized or malicious activities.

## **📜 License**

GPL v3 - This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

---

**💡 Contributions & Feedback Welcome!** 🚀

