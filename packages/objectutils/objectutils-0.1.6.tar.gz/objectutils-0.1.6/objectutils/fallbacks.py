def fallback(mapping=None):
    mapping = mapping or {}
    def dec(func):
        def wrapper(*args, exception=None, **kwargs):
            if exception == None:
                return func(*args, **kwargs)
            try:
                return mapping[type(exception)](*args, **kwargs)
            except Exception as e:
                raise exception
        return wrapper 
    return dec