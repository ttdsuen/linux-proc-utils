import re


def _to_kb(value, unit):
    """Returns convert value to kb given unit"""
    if unit == 'kb':
        return value
    elif unit == 'mb':
        return value * 1024
    elif unit == 'gb':
        return value * 1024 * 1024
    elif unit == 'tb':
        return value * 1024 * 1024 * 1024
    elif unit == 'pb':
        return value * 1024 * 1024 * 1024 * 1024
    elif unit == 'eb':
        return value * 1024 * 1024 * 1024 * 1024 * 1024
    else:
        raise OSError


def _retrieve(fpath, keys, regex_table):
    v = dict()

    # assign default values
    for key in keys:
        if regex_table[key].get('unit_index', None) is not None:
            v[key] = None
        else:
            v[key] = { 'value': None, 'unit': None }
    try:
        with open(str(fpath), 'r') as f:
            def line_in_scope(line):
                for key in keys:
                    if re.match(regex_table[key]['regex'], line):
                        return True
                return False
            lines = [
                line for line in f if line_in_scope(line)
            ]
            for line in lines:
                for key in keys:
                    x = re.match(regex_table[key]['regex'], line)
                    if x:
                        if regex_table[key].get('unit_index', None) is not None:
                            v[key] = _to_kb(
                                regex_table[key]['value_index'](x),
                                regex_table[key]['unit_index'](x)
                            )
                        else:
                            v[key] = regex_table[key]['value_index'](x)
        return v
    except:
        raise OSError

