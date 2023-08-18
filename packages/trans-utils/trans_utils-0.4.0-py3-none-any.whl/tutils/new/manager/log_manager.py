from .loggers import MultiLogger



class LoggerManager:
    
    def get_logger(self, config):
        config_base = config['base']
        config_logger = config['logger']
        logger = MultiLogger(logdir=config_base['runs_dir'], 
                            record_mode=config_logger.get('record_mode', None), 
                            tag=config_base['tag'], 
                            extag=config_base.get('experiment', None),
                            action=config_logger.get('action', 'k')) # backup config.yaml
        return logger