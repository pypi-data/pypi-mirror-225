# -*- coding: utf-8 -*-
# File: logger.py

'''
    How To Use :
    from mylogger import get_mylogger, set_logger_dir, auto_set_dir
    logger = get_mylogger()
    logger.warning("warning")
    set_logger_dir(logger, "test")
'''
import errno
import logging
from logging import Logger
import os
import os.path
import shutil
import sys
from logging import INFO, DEBUG, WARNING, CRITICAL, ERROR
from termcolor import colored
import sys
from collections import OrderedDict
from tutils.new.utils.core_utils import _get_time_str, _tprint, _tfilename
import torch
from tensorboardX import SummaryWriter

INFO = INFO
DEBUG = DEBUG
WARNING = WARNING
CRITICAL = CRITICAL
ERROR = ERROR



class TBLogger:
    def __init__(self, logdir, *args, **kwargs):
        _tprint(f"Use Tensorboard, log at '{os.path.join(logdir, 'tb')}'")
        self.tb_logger = SummaryWriter(logdir=os.path.join(logdir, "tb"))
        self.step = 0

    def record(self, d, step=-1, tag='std'):
        # debug:
        if step < 0:
            step = self.step
            self.step += 1
        to_record = {}
        for k, v in d.items():
            if isinstance(v, (float, int, )) or torch.is_tensor(k):
                to_record[k] = v
        # print("[Tuils] [TBLogger]: ", d)
        self.tb_logger.add_scalars(tag, to_record, global_step=step)


class MultiLogger(Logger):
    def __init__(self, 
                 logdir, 
                 record_mode=None, 
                 logging_mode=None,
                 tag="MyLogger",
                 extag=None, 
                 level=logging.INFO, 
                 action='k', 
                 file_name='log.log'):
        """
        record_mode: "wandb", "tb" or "tensorboard", "csv" : ["wandb", "tensorboard", "csv"]
        """
        super(MultiLogger, self).__init__(tag)
        self.logdir = logdir
        self.record_mode = "logging_only" if record_mode is None else record_mode
        self.logging_mode = logging_mode
        self.multi_recorder = MultiRecorder(record_mode, logdir, tag)
        
        # --------- Standard init        
        self.propagate = False
        self.setLevel(level)

        if self.logging_mode != "file_only":
            # Set StreamHandler, for console
            handler = logging.StreamHandler()
            # handler = logging.FileHandler('test.log', 'w', 'utf-8') # or whatever
            handler.setFormatter(_MyFormatter(tag=tag, extag=extag, datefmt='%Y-%m-%d %H:%M:%S'))
            self.addHandler(handler)

        # if self.logging_mode == "file_only":
        # Set FileHandler
        dirname = self.set_logger_dir(_tfilename(logdir, "log"), action, file_name, tag=tag, extag=extag)
        self._set_FileHandler(os.path.join(dirname, file_name), tag=tag, extag=extag)
    
    def add_scalars(self, *args, **kwargs):
        self.multi_recorder.add_scalars(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.info(*args, **kwargs)

    def _set_FileHandler(logger, path, tag=None, extag=None):
        if os.path.isfile(path):
            backup_name = path + '.' + _get_time_str()
            shutil.move(path, backup_name)
            logger.info("Existing log file '{}' backuped to '{}'".format(path, backup_name))  # noqa: F821
        hdl = logging.FileHandler(
            filename=path, encoding='utf-8', mode='w')
        hdl.setFormatter(_MyFormatter(tag=tag, extag=extag, datefmt='%Y-%m-%d-%H:%M:%S', colorful=False))

        _FILE_HANDLER = hdl
        logger.addHandler(hdl)
        logger.info("Argv: python " + ' '.join(sys.argv))

    def set_logger_dir(self, dirname='log', action='k', file_name='log.log', tag=None, extag=None):
        """
        Set the directory for global logging.
        Args:
            dirname(str): log directory
            action(str): an action of ["k","d","q"] to be performed
                when the directory exists. Will ask user by default.
                    "d": delete the directory. Note that the deletion may fail when
                    the directory is used by tensorboard.
                    "k": keep the directory. This is useful when you resume from a
                    previous training and want the directory to look as if the
                    training was not interrupted.
                    Note that this option does not load old models or any other
                    old states for you. It simply does nothing.
                    "b" : copy the old dir
                    "n" : New an new dir by time
        """
        def dir_nonempty(dirname):
            # If directory exists and nonempty (ignore hidden files), prompt for action
            return os.path.isdir(dirname) and len([x for x in os.listdir(dirname) if x[0] != '.'])

        if dir_nonempty(dirname):
            dirname = os.path.join(dirname, "logs")
            if action == 'b':
                backup_name = dirname + _get_time_str()
                shutil.move(dirname, backup_name)
                self.info("Directory '{}' backuped to '{}'".format(dirname, backup_name))  # noqa: F821
            elif action == 'd':
                shutil.rmtree(dirname, ignore_errors=True)
                if dir_nonempty(dirname):
                    shutil.rmtree(dirname, ignore_errors=False)
            elif action == 'n':
                dirname = dirname + _get_time_str()
                self.info("Use a new log directory {}".format(dirname))  # noqa: F821
            elif action == 'k':
                pass
            else:
                raise OSError("Directory {} exits!".format(dirname))
        _mkdir_p(dirname)
        return dirname


class MultiRecorder(object):
    """
        Extra Log Writer , including TensorBoard, wandb
    """
    def __init__(self, record_mode, logdir, tag="Log") -> None:
        super().__init__()

        self.step = -1
        self.wandb_logger = None
        self.tb_logger = None
        self.csv_logger = None
        self.text_logger = None

        if record_mode == None: record_mode = []
        if type(record_mode) is str: record_mode = [record_mode]
        if "wandb" in record_mode:
            import wandb
            wandb.init(project=tag)
            wandb.watch_called = False
            self.wandb_logger = wandb
        if "tb" in record_mode or "tensorboard" in record_mode:
            from tensorboardX import SummaryWriter
            if logdir is None:
                _tprint(f"Failed to turn on Tensorboard due to logdir=None")
            else:
                # _tprint(f"Use Tensorboard, log at '{os.path.join(logdir, 'tb')}'")
                # self.tb_logger = SummaryWriter(logdir=os.path.join(logdir, "tb"))
                self.tb_logger = TBLogger(logdir=logdir)
        # if "csv" in record_mode:
        #     self.csv_logger = CSVLogger(logdir=os.path.join(logdir, "csv"))
        self.extra_logger = True if len(record_mode) > 0 else False
        
    def add_scalars(self, dicts:dict={}, step=-1, tag="train", verbose=True):
        if not self.extra_logger:
            return 
        if self.wandb_logger is not None:
            self.wandb_logger.log(dicts)

        if self.tb_logger is not None:
            self.tb_logger.record(d=dicts, step=step, tag=tag)
            
        self.step = self.step + 1
        if self.text_logger is not None:
            if verbose:
                string = f"[tlog] Step:{self.step}  "
                for key, value in dicts.items():
                    string += f"{key}:{value};"
                self.info(string)


class _MyFormatter(logging.Formatter):
    def __init__(self, tag=None, extag=None, colorful=True, *args, **kwargs):
        self.tag = tag
        self.extag = extag
        self.colorful = colorful
        extag = '-' + extag if (extag is not None and extag != '') else ''
        # _tprint(tag, extag)
        self.taginfo = self._colored_str(f'[{tag}{extag}]', 'cyan') if tag is not None else ''
        super(_MyFormatter, self).__init__(*args, **kwargs)
        
    def format(self, record):    
        if not self.colorful:
            # Logging file
            date = self._colored_str('[%(asctime)s @%(filename)s:%(lineno)d] ', 'green')
        else:
            # Terminal
            date = self._colored_str('[%(asctime)s] ', 'green')
        date = date + self.taginfo
        msg = '%(message)s'
        if record.levelno == logging.WARNING or record.levelno == logging.DEBUG:
            fmt = date + ' ' + self._colored_str('WRN', 'yellow', attrs=['blink']) + '' + msg + ' \nPath: [%(pathname)s] ' + \
                 '\nProcess: [%(process)d %(processName)s]' + '\nThread: [%(thread)d %(threadName)s]'
        elif record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:
            fmt = date + ' ' + self._colored_str('ERR', 'red', attrs=['blink', 'underline']) + ' ' + msg + ' \nPath: [%(pathname)s] ' + \
                 '\nProcess: [%(process)d %(processName)s]' + '\nThread: [%(thread)d %(threadName)s]'
        # elif record.levelno == logging.INFO:
        #     fmt = date + ' ' + self._colored_str('INFO', 'cyan', attrs=['bold']) + ' ' + msg
        else:
            fmt = date + ' ' + msg
        if hasattr(self, '_style'):
            # Python3 compatibility
            self._style._fmt = fmt
        self._fmt = fmt
        return super(_MyFormatter, self).format(record)

    def _colored_str(self, text, *args, **kwargs):
        if self.colorful:
            return colored(text, *args, **kwargs)
        else:
            return text


def _mkdir_p(dirname):
    """ Like "mkdir -p", make a dir recursively, but do nothing if the dir exists
    Args:
        dirname(str):
    """
    assert dirname is not None
    if dirname == '' or os.path.isdir(dirname):
        return
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
