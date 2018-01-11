
class ServiceInterface(object):

    def __init__(self, **kargs):
        pass

    def update(self, **kargs):
        raise Exception("Not implemented for this class")

    def load(self, **kargs):
        raise Exception("Not implemented for this class")

    def check(self, domain=None, **kargs):
        raise Exception("Not implemented for this class")
