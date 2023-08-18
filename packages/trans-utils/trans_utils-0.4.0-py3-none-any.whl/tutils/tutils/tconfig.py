
class Config(object):
    def __init__(self):
        super().__init__()
        self.TUTILS_DEBUG = False
        self.TUTILS_INFO = False
        self.TUTILS_WARNING = True

    def set_print_debug(self, setting=True):
        self.TUTILS_DEBUG = setting

    def set_print_info(self, setting=True):
        self.TUTILS_INFO = setting

    def set_print_warning(self, setting=True):
        self.TUTILS_WARNING = setting

_C = Config()