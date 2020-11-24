from aspectlib import Aspect

def log_errors(*args, **kwargs):
    try:
        yield
    except Exception as e:
        print("Raised %r for %s/%s" % (e, args, kwargs))
