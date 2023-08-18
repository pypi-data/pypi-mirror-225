
### TODO

from _collections_abc import dict_items
from typing import Any, Dict, List
from .functools import _merge_two_dict
import os
import yaml
import yamlloader
import argparse
import copy


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
}

class ConfigManager(Dict):
    def __init__(self, config_dict=None) -> None:
        self.config = BASE_CONFIG
        self.args = None
        if config_dict is not None:
            self.config = _merge_two_dict(self.config, config_dict)

    def keys(self):
        return self.config.keys()
    

    def add_config(self, config):
        if isinstance(config, dict):
            # Add config directly
            config_dict = config
        if isinstance(config, str):
            # Load config from *.yaml file
            if config.endswith(".yaml") or config.endswith(".yml"):
                config_dict = self._add_yaml_config(config)
        if isinstance(config, argparse.Namespace):
            args = config
            config_dict = vars(copy.deepcopy(args))
            config_dict = _clear_config(config_dict)
            if args.config is not None:
                with open(args.config) as f:
                    config_dict = yaml.load(f, Loader=yamlloader.ordereddict.CLoader)    
                config_dict_0 = _clear_config(config_dict)
                config_dict = _merge_two_dict(config_dict_0, config_dict)

        config_dict = _clear_config(config_dict)
        self.config = _merge_two_dict(self.config, config_dict)

    
    def _add_yaml_config(self, config_filename):
        with open(config_filename) as f:
            file_config = yaml.load(f, Loader=yamlloader.ordereddict.CLoader)
        return file_config
    
    def items(self) -> dict_items:
        return self.config.items()
    