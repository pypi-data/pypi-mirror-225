import importlib
import re

# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

def import_optional_dependency(name: str):
    """ Import an optional dependency.
    Derived from pandas:
    https://github.com/pandas-dev/pandas/blob/master/pandas/compat/_optional.py
    """
    msg = (
        f"Method is not supported because "
        f"an optional dependency is missing: '{name}'"
    )
    try:
        module = importlib.import_module(name)
    except ImportError:
        raise NotImplementedError(msg) from None
    return module


def parse_list_indices_from_string(str_list: str, list_to_slice: list):
    output_list = []
    regex = r"[0-9]+:[0-9]+"
    is_slice = re.findall(regex, str_list)
    if is_slice:
        s = map(int, str_list.split(':'))
        start, end = s
        output_list = list_to_slice[start:end + 1]
    else:
        try:
            s = list(map(int, str_list.split(',')))
            for i in s:
                output_list.append(i)
        except:
            output_list = str_list.split(',')
    return output_list
