
class Listen(object):
    Minecraft = "Minecraft"
    server = "server"
    client = "client"
    def __init__(self, event_name=None, event_type='Minecraft', system_name='main', priority=3):
        self.event_name = event_name
        self.event_type = event_type
        self.system_name = system_name
        self.priority = priority

    def __call__(self, func):
        func.listen_type = self.event_type
        func.listen_event = self.event_name or func.__name__
        func.system_name = self.system_name
        func.listen_priority = self.priority
        return func
