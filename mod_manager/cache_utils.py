from functools import wraps

def cache_result(f):
    """Caches the result of a function call. The function must have no arguments (e.g. property)."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        assert len(args) == 0 and len(kwargs) == 0, "Wrapped call must be empty"
        if not hasattr(f, "cached_result"):
            f.cached_result = f()
        return f.cached_result
    return wrapper
