import yaml
import yamlloader
import shutil
import os
from pathlib import Path
from datetime import datetime
from collections import OrderedDict
from pathlib import Path
from datetime import datetime
from torchvision.utils import save_image as tv_save_image

def _get_time_str():
    return datetime.now().strftime('%m%d-%H%M%S')

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


def save_script(runs_dir, _file_name, logger=None):
    file_path = os.path.abspath(_file_name)
    parent, name = os.path.split(_file_name)
    time = _get_time_str()
    output_path = tfilename(runs_dir, "scripts", name)

    if os.path.isfile(output_path):
        backup_name = output_path + '.' + _get_time_str()
        shutil.move(output_path, backup_name)
        print(f"Existing yaml file '{output_path}' backuped to '{backup_name}' ")

    shutil.copy(file_path, output_path)
    # with open(os.path.join(runs_dir, "save_script.log"), "a+") as f:
    #     f.write(f"Script location: {_file_name};  Time: {time}\n")
    print(f"Saved script file: from {file_path} to {output_path}")

    
def tfilename(*filenames):
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
    d(filename)
    parent, name = os.path.split(filename)
    if parent != '' and not os.path.exists(parent):
        d(parent)
        os.makedirs(parent)
    return filename


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