
### TODO

from _collections_abc import dict_items
from typing import Any, Dict, List
import os
import yaml
import yamlloader
import argparse
import copy
from collections import OrderedDict
import shutil
from datetime import datetime

from tutils.new.utils.core_utils import _get_time_str, _tprint, _ordereddict_to_dict
from tutils.new.utils.core_utils import _tfilename as tfilename


BASE_CONFIG = {
    # params used in Initializer
    'base': {
        'base_dir': './runs_debug/',
        'experiment': "",
        'tag': '',
        'stage': '', 
        'extag': '',
        'config': '',
        'test': False,
        'func': 'train',
        'gpus': '',
        'ms': False,
        'runs_dir': None, # 
        },    
    # params used in Logger
    'logger':{
        'use_logger': True,
        'record_mode': ["tensorboard"], # "wandb", "tensorboard", 'csv'
        'action': 'k', 
        'logging_mode': None,
    },
    'training': {
        'gpus': None,
        'ddp': {
            'master_addr': 'localhost',
            'master_port': '25807',
            },
        'num_epochs' : 2500, 
        'batch_size' : 8,
        'num_workers' : 8,
        'save_interval' : 50,
        'load_pretrain_model': False,
        'load_optimizer': False,
        'val_check_interval': 10,
        'use_amp': False,
        'training_log_interval': 1,
        'save_latest_only': False,
        'save_all_records': True,
    },
    'ready': False,
}

class ConfigManager(dict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def auto_init(self, file, args=None, ex_config=None):
        _tprint("Add BASE_CONFIG")
        self.add_basic_config()

        _tprint("Set file ")
        self.set_file(file)

        if args is not None:
            _tprint("Add Args and args config")
            self.add_config(args)
        
        if ex_config is not None:
            _tprint("Add EX_config")
            self.add_config(ex_config)

        self.init()

        return self

    def set_file(self, file, set_expname=True):
        parent, name = os.path.split(file)
        self["base"]["__file__"] = file
        if set_expname:
            name = name[:-3]
            _tprint(f"Change experiment name from {self['base'].get('experiment', '')} to {name}")
            self['base']['experiment'] = name
        return self

    def add_config(self, config):
        if isinstance(config, dict):
            # Add config directly
            config_dict = config
            config_dict = _clear_config(config_dict)
            self.update(_merge_two_dict(self, config_dict))
        elif isinstance(config, str):
            # Load config from *.yaml file
            if config.endswith(".yaml") or config.endswith(".yml"):
                config_dict = self._add_yaml_config(config)
                config_dict = _clear_config(config_dict)
                self.update(_merge_two_dict(self, config_dict))
        elif isinstance(config, argparse.Namespace):
            args = config
            if args.config is not None:
                with open(args.config) as f:
                    config_file = yaml.load(f, Loader=yamlloader.ordereddict.CLoader)    
                    config_file = _clear_config(config_file)
                    self.update(_merge_two_dict(self, config_file))

            config_args = vars(copy.deepcopy(args))
            config_args = _clear_config(config_args)
            config_args = {'base': config_args}  # Insert args into 'base'
            self.update(_merge_two_dict(self, config_args))       
        else:
            raise ValueError
        
        return self
    
    def add_basic_config(self):
        config_basic = _clear_config(BASE_CONFIG)
        self.update(_merge_two_dict(config_basic, self))
        return self

    def show_basic_config(self):
        _print_dict(BASE_CONFIG)
    
    def print(self):
        # def _print_dict(_dict, layer=0):
        _print_dict(self)

    def to_yaml(self, path=None):
        path = self['base']['runs_dir'] + "/config.yaml" if path is None else path
        path = tfilename(path)
        if os.path.isfile(path):
            backup_name = path + '.' + _get_time_str()
            shutil.move(path, backup_name)
            _tprint(f"Existing yaml file '{path}' backuped to '{backup_name}' ")
        with open(path, "w") as f:
            config = _ordereddict_to_dict(self)
            yaml.dump(config, f)
        _tprint(f"Saved config.yaml to {path}")

    def save(self, file=None, path=None):
        # run_dir = self['run_dir']
        self.to_yaml(path=tfilename(self['base']['runs_dir']))

    def init(self):
        config_base = self['base']
        config_base['tag'] = config_base['tag'] if ('tag' in config_base.keys()) and (config_base['tag']!="") else str(datetime.now()).replace(' ', '-')
        config_base['extag'] = config_base.get('extag', None)
        config_base['__INFO__'] = {}
        config_base['__INFO__']['runtime'] = str(datetime.now()).replace(' ', '-')
        experiment = config_base.get('experiment', '')
        stage = config_base.get('stage', '')

        config_base['runs_dir'] = os.path.join(config_base['base_dir'], experiment, config_base['tag'], stage)
        if not os.path.exists(config_base['runs_dir']):
            print(f"Make dir '{config_base['runs_dir']}' !")
            os.makedirs(config_base['runs_dir'])

        file = self['base'].get('__file__', None)
        if file is not None:
            print(f"Save running script to {self['base']['runs_dir']} from {file}")
            save_script(self['base']['runs_dir'], file)

        if not self.get('ready', False):
            self['ready'] = True
        return self

    def _add_yaml_config(self, config_filename):
        with open(config_filename) as f:
            file_config = yaml.load(f, Loader=yamlloader.ordereddict.CLoader)
        return file_config
    

########################  Utils  ##########################

def save_script(runs_dir, _file_name, logger=None):
    file_path = os.path.abspath(_file_name)
    parent, name = os.path.split(_file_name)
    time = _get_time_str()
    output_path = tfilename(runs_dir, "scripts", name)

    if os.path.isfile(output_path):
        backup_name = output_path + '.' + _get_time_str()
        shutil.move(output_path, backup_name)
        _tprint(f"Existing yaml file '{output_path}' backuped to '{backup_name}' ")

    shutil.copy(file_path, output_path)
    # with open(os.path.join(runs_dir, "save_script.log"), "a+") as f:
    #     f.write(f"Script location: {_file_name};  Time: {time}\n")
    _tprint(f"Saved script file: from {file_path} to {output_path}")

def _print_dict(_dict, layer=0):
    if isinstance(_dict, (dict, OrderedDict)):
        for key, value in _dict.items():
            if isinstance(value, (dict, OrderedDict)):
                print("    "*layer, key, end=": {\n")
                _print_dict(value, layer+1)
                print("    "*layer, "}")
            else:
                if isinstance(value, str):
                    value = f'"{value}"'
                print("    "*layer, f"{key}: {value},")
    else:
        print("    "*layer, _dict)    

def _merge_two_dict(d1:Dict, d2:Dict) -> ConfigManager:
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
    return ConfigManager(ret_dict)


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


if __name__ == "__main__":
    config = ConfigManager(BASE_CONFIG)
    import ipdb; ipdb.set_trace()