import re


def _to_kb(value, unit):
    """Given a recognized `unit`, returns `value` in kb

    :param unit: One of `'kb'`, `'mb'`, `'gb'`, `'tb'`, `'pb'`, or `'eb'`
    :type unit: str
    :returns: `value` converted to kb from the given unit
    :rtype: int or float
    :raises: RuntimeError on unsupported `unit`

    """
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
        raise RuntimeError(
            '_to_kb(): unsupported unit parameter {}'.format(unit)
        )


def _retrieve(file, keys, regex_table):
    """Retrieve lines from `file` matching some regex
   
    :param fpath: file to be opened
    :type fpath: str
    :param keys: list of keys into the dictionary regex_table
    :type keys: list
    :param regex_table: dictionary whose values contain regex and convertion logics
    :type regex_table: dict
    :returns: 

    """
    v = dict()

    # assign default values
    for key in keys:
        v[key] = None
    def line_in_scope(line):
        for key in keys:
            if re.match(regex_table[key]['regex'], line):
                return True
        return False

    try:
        with open(str(file), 'r') as f:
            #
            # lines[] would contain lines matching one of
            # the regex specified by the key to the regex_table
            #
            lines = [
                line for line in f if line_in_scope(line)
            ]
            for line in lines:
                for key in keys:
                    x = re.match(regex_table[key]['regex'], line)
                    if x:
                        value_lmbda = regex_table[key]['value_index']
                        v[key] = value_lmbda(x)
                        unit_lmbda = regex_table[key].get(
                            'unit_index', None
                        )
                        if unit_lmbda is not None:
                            # unit exists -> do conversion
                            v[key] = _to_kb(
                                v[key],
                                unit_lmbda(x)
                            )
        return v
    except FileNotFoundError:
        raise RuntimeError('_retrieve{}: {} not found'.format(file))

