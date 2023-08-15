
class AsyncClass(object):
    def __init__(self):
        pass

    def __await__(self):
        async def closure():
            return self

        return closure().__await__()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def initialize(self):
        raise NotImplementedError("Subclass should override")
