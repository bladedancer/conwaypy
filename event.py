class PubSub(object):
    __handlers = {}

    @classmethod
    def subscribe(cls, event, handler):
        if not event in cls.__handlers:
            cls.__handlers[event] = []
        cls.__handlers[event].append(handler)

    @classmethod
    def publish(cls, event, *args, **keywargs):
        if not event in cls.__handlers:
            return
        for handler in cls.__handlers[event]:
            handler(*args, **keywargs)
