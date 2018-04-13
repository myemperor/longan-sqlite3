class Flesh:
    """"
    对数据库中取出来的数据进行了封装
    """

    def __init__(self, _dict=None, **kwargs):
        if not _dict:
            _dict = kwargs
        for k, v in _dict.items():
            self.__setattr__(k, v)

    def get(self, name):
        return self.__dict__[name]

    def set(self, name, value, force=True):
        if force or name not in self.__dict__:
            self.__dict__[name] = value

    def __str__(self):
        return str(self.__dict__)

    def keys(self):
        return list(self.__dict__.keys())

    def keys_str(self):
        return ",".join(self.keys())

    def values(self):
        return list(self.__dict__.values())

    def values_str(self):
        return str(self.values())[1:-1].replace('None', 'null')

    def join(self, s):
        ret_s = []
        for k, v in self.__dict__.items():
            if isinstance(v, str):
                v = '"{}"'.format(v)
            ret_s.append("{}{}{}".format(k, s, v))
        return ','.join(ret_s)
