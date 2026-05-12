plugin_registry = {}
def Module(name):
    print "注册模块: " + name
    def decorator(cls):
        plugin_registry[name] = cls
        return cls
    return decorator

