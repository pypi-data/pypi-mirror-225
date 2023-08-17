def find_value_from_nested_keys(keys, dict_):
    dict_value = dict_
    for key in keys:
        dict_value = dict_value.get(key)
        if not dict_value:
            return None
    return dict_value
