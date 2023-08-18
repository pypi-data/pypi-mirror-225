"""
    Utils that will be used in all files
"""
import os
from datetime import datetime
from collections import OrderedDict



def _get_time_str():
    return datetime.now().strftime('%m%d-%H%M%S')


def _tfilename(*filenames):
    def checkslash(name):
        if name.startswith("/"):
            name = name[1:]
            return checkslash(name)
        else:
            return name
    if len(filenames) <= 1:
        filename = filenames[0]
    else:
        names = [filenames[0]]
        for name in filenames[1:]:
            names.append(checkslash(name))
        filename = os.path.join(*names)
    # d(filename)
    parent, name = os.path.split(filename)
    if parent != '' and not os.path.exists(parent):
        # d(parent)
        os.makedirs(parent)
    return filename



def _tprint(*args, **kwargs):
    print("[Tutils] ", end="")
    print(*args, **kwargs)



def _print_dict(_dict, layer=0):
    if isinstance(_dict, (dict, OrderedDict)):
        for key, value in _dict.items():
            if isinstance(value, (dict, OrderedDict)):
                print("    "*layer, key, end=":\n")
                _print_dict(value, layer+1)
            else:
                print("    "*layer, f"{key}: {value}")
    else:
        print("    "*layer, _dict)



def _merge_cascade_dict(dicts):
    num_dict = len(dicts)
    ret_dict = {}
    for d in dicts:
        assert isinstance(d, dict), f"Got d1: {d}"
        ret_dict = _merge_two_dict(ret_dict, d)
    return ret_dict

def _merge_two_dict(d1, d2):
    # Use d2 to overlap d1
    d1 = {} if d1 is None else d1
    d2 = {} if d2 is None else d2
    assert isinstance(d1, dict), f"Got d1: {d1}"
    assert isinstance(d2, dict), f"Got d1: {d2}"
    ret_dict = {**d2, **d1}
    if isinstance(d2, dict):
        for key, value in d2.items():
            if isinstance(value, dict):
                ret_dict[key] = _merge_two_dict(ret_dict[key], d2[key])
            else:
                ret_dict[key] = d2[key]
    return ret_dict 


def _ordereddict_to_dict(d):
    if not isinstance(d, dict):
        return d
    for k, v in d.items():
        if type(v) == OrderedDict:
            v = _ordereddict_to_dict(v)
            d[k] = dict(v)
        elif type(v) == list:
            d[k] = _ordereddict_to_dict(v)
        elif type(v) == dict:
            d[k] = _ordereddict_to_dict(v)
    return d

# def _clear_config(config):
#     # if type(config) is dict or type(config) is OrderedDict:
#     if isinstance(config, (dict, OrderedDict)):
#         pop_key_list = []
#         for key, value in config.items():
#             # print("debug: ", key, value)
#             if value is None or value == "" or value == "None":
#                 # print("debug: poped", key, value)
#                 pop_key_list.append(key)
#             elif isinstance(config, (dict, OrderedDict)):
#                 _clear_config(value)
#             else:
#                 pass
#         for key in pop_key_list:
#             config.pop(key)
#     return config

