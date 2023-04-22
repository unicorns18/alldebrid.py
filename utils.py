"""
Utility functions (decorators, etc.)
"""

def handle_exceptions(*, exceptions):
    """
    Decorator to handle exceptions, if any.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as exc:
                print(f"Exception occurred: {exc}")
        return wrapper
    return decorator
