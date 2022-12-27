from .flesh import Flesh


def convert_dicts(fields, items):
    """
    :param fields:
    :param items:
    :return: list(Flesh)
    :rtype: list
    """
    ret_items = []
    for i in items:
        item_dict = {}
        for k, v in enumerate(fields):
            item_dict[v] = i[k]
        ret_items.append(Flesh(item_dict))
    return ret_items


def add_quotes(value):
    if isinstance(value, str):
        if value.upper() == 'NULL' or value.upper() == 'NOT NULL':
            value = value.upper()
        else:
            value = '"{}"'.format(value.replace('"', "'"))
    return value
