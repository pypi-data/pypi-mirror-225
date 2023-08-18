from tutils.tutils.initializer import trans_configure, trans_init, trans_args, trans_config


class TestConfig:
    def test_trans_init(self):
        print("testing : test_trans_init")
        logger, config = trans_init()
        print(config)
        assert config is not None
        assert logger is not None

