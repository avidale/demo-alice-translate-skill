from collections.abc import Mapping


def replace_dotted_keys(data, dot_symbol='~'):
    """ Replace dots in dict keys with other symbols, to comply with Pymongo checks """
    if isinstance(data, Mapping):
        result = {}
        for key, value in data.items():
            new_key = key
            if isinstance(key, str):
                new_key = new_key.replace('.', dot_symbol)
            result[new_key] = replace_dotted_keys(value, dot_symbol=dot_symbol)
        return result
    elif isinstance(data, list):
        return [replace_dotted_keys(item, dot_symbol=dot_symbol) for item in data]
    else:
        return data
