from .config_manager import ConfigManager
from .log_manager import LoggerManager

def trans_init(args=None, file=None, ex_config=None):
    config = ConfigManager()
    config.auto_init(file=file, args=args, ex_config=ex_config)
    
    logger = LoggerManager().get_logger(config)
    return logger, config
