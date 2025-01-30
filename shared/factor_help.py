"""
factor_help.py

Author: forensicskween
Description:
This module provides utilities for integer factorization using a combination of methods, including:
- Factoring integers via the FactorDB API.
- Extended Collatz Method (ECM) for large integer factorization.
- Iterative submissions to FactorDB for improved accuracy.
- Utilities for formatting and handling factorization results.

The functions in this file allow for flexible and timeout-safe factorization, with options for retrieving results as factor dictionaries.

Dependencies:
- SageMath (`sage.all` for `ecm` and `is_prime`)
- requests
- factordb-pycli (FactorDB API client)
"""

import requests
from collections import Counter
from factordb.factordb import FactorDB
from sage.all import ecm,is_prime

from .run_timeouts import loop_func_with_timeout


def submit_manual(N):
    """
    Submits a number to the FactorDB website manually for factorization.

    Args:
        N (int): The number to be submitted to FactorDB.

    Raises:
        AssertionError: If the HTTP request to FactorDB fails.
    """
    php_site = f'http://factordb.com/index.php?query={str(N)}'
    ret = requests.get(php_site)
    return ret.ok


def factor_factordb(N):
    """
    Retrieves the factors of a number from FactorDB.

    Args:
        N (int): The number to factorize.

    Returns:
        list[int]: A list of factors retrieved from FactorDB.
    """
    N = int(N)
    try:
        f = FactorDB(N)
        f.connect()
        return f.get_factor_list()
    except Exception as e:
        print(f"Error connecting to FactorDB: {e}")
        return []



def iter_factordb(N,iter_count=3):
    """
    Submits a number to FactorDB multiple times and retrieves factors.
    As sometimes you need to submit a few times to get the factors.

    Args:
        N (int): The number to factorize.
        iter_count (int): The number of iterations to submit and retrieve results. Default is 3.

    Returns:
        list[int]: A list of factors retrieved from FactorDB.
    """
    for _ in range(iter_count): #makes sure we submit multiple times
        submit_manual(N)
        res = factor_factordb(N)
    return factor_factordb(N)


def call_factordb(N,iter_count=3):
    """
    Retrieves factors of a number using iterative submissions to FactorDB,
    with additional validation of results.

    Args:
        N (int): The number to factorize.
        iter_count (int): The number of iterations for submission and retrieval. Default is 3.

    Returns:
        list[int]: A list of validated factors.
    """
    res = iter_factordb(N,iter_count)
    res_check = iter_factordb(res[-1],iter_count)
    if res_check != res[-1]:
        res = iter_factordb(N)
    return res 


def fact_dict(fac_list):
    """
    Converts a list of factors into a dictionary with their powers.

    Args:
        fac_list (list[int]): A list of factors.

    Returns:
        list[int]: A sorted list of factors raised to their respective powers.
    """
    factor_counts = Counter(fac_list)
    return sorted([k**v for k, v in factor_counts.items()])



def factor_integer(N,timeout,max_timeout=None):
    """
    Factors an integer using FactorDB and ECM with timeout handling.

    Args:
        N (int): The number to factorize.
        timeout (int): The timeout duration for the ECM factorization.
        max_timeout (int, optional): The maximum allowed timeout for ECM. Default is None.

    Returns:
        list[int]: A list of factors of the integer.
    """
    factors = factor_factordb(N)
    if all(is_prime(x) for x in factors):
        return factors
    for X in factors:
        if not is_prime(X):
            additional_factors = loop_func_with_timeout(ecm.factor,X,timeout=timeout,max_timeout=max_timeout)
            if not additional_factors:
                pass
            else:
                factors.remove(X)
                factors.extend(additional_factors)
    return factors

def safe_factorization(func, value, timeout, max_timeout=None):
    """
    Safely executes a factorization function with timeout handling.

    Args:
        func (callable): The factorization function.
        value (int): The value to factorize.
        timeout (int): The timeout for the function.
        max_timeout (int, optional): The maximum timeout. Default is None.

    Returns:
        list[int]: The factors of the value, or an empty list if timeout occurs.
    """
    return loop_func_with_timeout(func, value, timeout=timeout, max_timeout=max_timeout)



def get_factors(N,timeout,max_timeout=None,factor_dict=False):
    """
    Retrieves the factors of an integer with optional factor dictionary formatting.

    Args:
        N (int): The number to factorize.
        timeout (int): The timeout duration for the ECM factorization.
        max_timeout (int, optional): The maximum allowed timeout for ECM. Default is None.
        factor_dict (bool): Whether to return the factors as a dictionary. Default is False.

    Returns:
        list[int] | tuple[list[int], list[int]]:
            - If `factor_dict` is False: A list of factors.
            - If `factor_dict` is True: A tuple containing the list of factors and their dictionary representation.
    """
    result = factor_integer(N,timeout,max_timeout)
    if factor_dict:
        return result,fact_dict(result)
    return result 

