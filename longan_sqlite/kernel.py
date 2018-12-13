import json


class Kernel:
    """
    此类是对表的字段进行封装
    """

    def __init__(self, field_info):
        if len(field_info) < 6:
            raise RuntimeError("Error Field!")
        self.order_id = field_info[0]
        self.name = field_info[1]
        self.type = field_info[2]
        self.not_null = field_info[3]
        self.default = field_info[4]
        self.primary = field_info[5]

    def __str__(self):
        return json.dumps(self.__dict__)
