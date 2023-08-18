from tutils.new.manager import ConfigManager

config = ConfigManager()
config.add_basic_config()
config

config.auto_init(file=__file__).print()