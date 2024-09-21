def remote_procedure(fn):
    """
    Marker decorator to declare that a function is a remote_procedure
    Decoratored callables will result in a result API endpoint
    """

    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper
