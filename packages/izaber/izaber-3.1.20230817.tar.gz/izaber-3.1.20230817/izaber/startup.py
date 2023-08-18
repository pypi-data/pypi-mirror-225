import sys

app_config = {}
dependancies = {}

initializer_lookup = {}
initialization_rack = {}

def initializer(key,before=[]):
    def rack(key,f):
        initialization_rack[key] = f
        initializer_lookup[key] = f
        if before:
            for b in before:
                dependancies.setdefault(b,[])
                dependancies[b].append(key)
        return f

    return lambda f: rack(key,f)

def initialize(name=None, **kwargs):
    """ Invokes the initialization code for all the izaber.* modules
        that are hanging off of the system.
    """
    if name is None:
        name = sys.argv[0] or ''
    kwargs['name'] = name
    app_config.update(kwargs)

    # Reset load sequence if required
    if kwargs.get('force'):
        initialization_rack.update(initializer_lookup)

    # Go through load sequence handling dependancies as we go
    for key, func in dict(initializer_lookup).items():
        # If the initialization rack doesn't have the key, it means
        # we've already visited the initializer
        if not initialization_rack[key]:
            continue

        # Let's now ensure all the deps of this module are handled
        # (They need to be initialized before we can invoke this one)
        if key in dependancies:
            for b in dependancies.get(key,[]):
                result = request_initialize(b, **kwargs)
                if result:
                    kwargs = result

        # Was getting a weird error with flask where kwargs become None
        if not kwargs: kwargs = {}
        kwargs = request_initialize(key, **kwargs)
        initialization_rack[key] = None

def request_initialize(key, **kwargs):
    """ Force the initialization of another module tagged via `key`
    """

    # If the initialization rack doesn't have the key, it means
    # we've already visited the initializer
    if not initialization_rack[key]:
        return

    # Then invoke the initializer and log that we've completed
    replace_kwargs = initializer_lookup[key](**kwargs)
    initialization_rack[key] = None

    if replace_kwargs: return replace_kwargs
    return kwargs

