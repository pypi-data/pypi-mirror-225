def set_open(func):
    setattr(func, 'open', True)
    return func