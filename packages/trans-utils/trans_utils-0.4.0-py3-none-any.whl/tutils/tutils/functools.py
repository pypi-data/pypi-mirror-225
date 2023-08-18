
import yaml
import yamlloader
from pathlib import Path
from datetime import datetime
from collections import OrderedDict
# from .tconfig import _C
import os


def tprint(*args, **kwargs):
    print("[Tutils] ", end="")
    print(*args, **kwargs)


def _get_time_str():
    return datetime.now().strftime('%m%d-%H%M%S')


def _clear_config(config):
    # if type(config) is dict or type(config) is OrderedDict:
    if isinstance(config, (dict, OrderedDict)):
        pop_key_list = []
        for key, value in config.items():
            # print("debug: ", key, value)
            if value is None or value == "" or value == "None":
                # print("debug: poped", key, value)
                pop_key_list.append(key)
            elif isinstance(config, (dict, OrderedDict)):
                _clear_config(value)
            else:
                pass
        for key in pop_key_list:
            config.pop(key)
    return config


def print_dict(config):
    _print_dict(config)


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


def flatten_dict(d, parent_name=None):
    """
    flatten dict: 
    config={
        'base':
            'experiment': 'test',
    }
        ==> 
    config={
        'base.experiment': 'test',
    }
    """
    s = parent_name + "." if parent_name is not None else ""
    if isinstance(d, dict):
        _d = dict()
        for k, v in d.items():
            if not isinstance(v, dict):
                _d = {**_d, **{s+k: v}}
            else:
                _d = {**_d, **flatten_dict(d[k], s + k)}
        return _d


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




######################################################

def _tprint(*s, end="\n", **kargs):
    if len(s) > 0:
        for x in s:
            print(x, end="")
        print("", end=end)
    if len(kargs) > 0:
        for key, item in kargs.items():
            print(key, end=": ")
            print(item, end="")
        print("", end=end)


def merge_cascade_dict(dicts):
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


def dump_yaml(logger=None, config=None, path=None, verbose=True):
    # Backup existing yaml file
    assert config is not None
    path = config['base']['runs_dir'] + "/config.yaml" if path is None else path
    path = tfilename(path)
    if os.path.isfile(path):
        backup_name = path + '.' + _get_time_str()
        shutil.move(path, backup_name)
        if logger is not None:
            logger.info(f"Existing yaml file '{path}' backuped to '{backup_name}' ")
        else:
            print(f"Existing yaml file '{path}' backuped to '{backup_name}' ")
    with open(path, "w") as f:
        config = _ordereddict_to_dict(config)
        yaml.dump(config, f)
    if verbose:
        if logger is not None:
            logger.info(f"Saved config.yaml to {path}")
        else:
            print(f"Saved config.yaml to {path}")


    