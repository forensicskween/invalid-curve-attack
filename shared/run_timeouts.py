"""
Author: forensicskween

Description:
This module provides utilities for executing functions with **timeout handling**, ensuring that 
long-running operations do not exceed their allocated time limits.

It supports:
- Running functions with a **strict timeout** (`run_func_with_timeout`).
- **Loop-based timeout handling**, where execution is retried with increasing time limits (`loop_func_with_timeout`).

These functions are useful for cryptographic operations, factorization, and any scenario where
a function's runtime is unpredictable.

Features:
- **SIGALRM-based timeout enforcement** for Linux/macOS.
- **Graceful handling of timeouts** by returning `None` instead of blocking execution.
- **Adjustable retry logic** for better results when timeouts occur.

Dependencies:
- **Python Standard Library** (`signal` for timeout handling)
- **SageMath** (if used within cryptographic applications)
"""


import signal

class TimeoutException(Exception):
    """
    Custom exception raised when a function exceeds the allowed execution time.
    """
    pass


def timeout_handler(signum, frame):
    """
    Signal handler that raises a TimeoutException when a function times out.

    Args:
        signum (int): The signal number.
        frame (FrameType): The current stack frame.

    Raises:
        TimeoutException: Always raises this exception to interrupt execution.
    """
    raise TimeoutException


def run_func_with_timeout(func, *args, timeout=1, **kwargs):
    """
    Executes a function with a time limit. If the function does not complete 
    within the specified timeout, it is interrupted and returns None.

    Args:
        func (callable): The function to execute.
        *args: Positional arguments for the function.
        timeout (int): Maximum allowed execution time in seconds (default: 1).
        **kwargs: Keyword arguments for the function.

    Returns:
        Any: The function's return value, or None if it times out.

    Example:
        def slow_function():
            time.sleep(5)
            return "Done"

        result = run_func_with_timeout(slow_function, timeout=2)
        print(result)  # Output: None (since function exceeded timeout)
    """
    assert timeout > 0, "Timeout must be positive"
    # Set the signal handler for SIGALRM
    signal.signal(signal.SIGALRM, timeout_handler)
    # Schedule the SIGALRM to be sent after the specified timeout
    signal.alarm(timeout)

    try:
        result = func(*args, **kwargs)
    except TimeoutException:
        result = None
    finally:
        # Cancel the alarm
        signal.alarm(0)

    return result


def loop_func_with_timeout(func, *args, timeout=1, **kwargs):
    """
    Repeatedly attempts to execute a function with increasing timeouts 
    until a maximum timeout is reached.

    Args:
        func (callable): The function to execute.
        *args: Positional arguments for the function.
        timeout (int): Initial timeout in seconds (default: 1).
        max_timeout (int, optional): Maximum allowed timeout (default: timeout + 5).
        **kwargs: Keyword arguments for the function.

    Returns:
        Any: The function's return value if successful, otherwise None.

    Raises:
        AssertionError: If max_timeout is not greater than the initial timeout.

    Example:
        def maybe_slow_function():
            time.sleep(random.randint(1, 6))
            return "Success"

        result = loop_func_with_timeout(maybe_slow_function, timeout=2, max_timeout=6)
        print(result)  # Output: "Success" if it completes within max_timeout, else None
    """
    start_timeout = timeout
    max_timeout = kwargs.pop('max_timeout', start_timeout + 5)
    assert max_timeout > start_timeout, "Max Timeout must be greater than the initial timeout!"
    assert timeout > 0, "Timeout must be positive"  # Ensure valid timeout
    result = None
    while start_timeout < max_timeout:
        result = run_func_with_timeout(func, *args, timeout=start_timeout, **kwargs)
        if result:
            return result
        start_timeout += 1  # Increment timeout for the next attempt

    return result  # Return None if function never succeeds within max_timeout
