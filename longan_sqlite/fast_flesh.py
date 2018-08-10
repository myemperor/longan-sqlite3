from .flesh import Flesh


class FastFlesh(Flesh):
    def __init__(self, fields=(), values=(), opt=None):
        dct = {}
        for i in range(len(fields)):
            dct[fields[i].name] = values[i] if opt is None else opt(values, i)
        Flesh.__init__(self, **dct)
