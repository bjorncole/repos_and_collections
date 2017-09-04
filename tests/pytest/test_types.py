from types import SimpleNamespace

class TrialNamespace(SimpleNamespace):

    def __init__(self):
        self.object_name = ''

    def __repr__(self):
        return 'Object ' + self.object_name + ' [' + str(hex(id(self))) + ']'