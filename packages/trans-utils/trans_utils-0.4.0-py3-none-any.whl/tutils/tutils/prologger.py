from .metriclogger import MetricLogger
from .ttimer import timer
from .recorder import Recorder
from .functools import tprint


# def usage2():
#     from tutils import trans_args, trans_init, print_dict
#     args = trans_args()
#     logger, config = trans_init(args)
#     print_dict(config)
#
#     metriclogger = MetricLogger(logger=None)
#
#     for data in metriclogger.log_every(range(20), print_freq=2, header="[trans]"):
#         i = 0
#         metriclogger.update(**{"ind": i, "data": data})
#
#     results = metriclogger.return_final_dict()


def usage():
    from tutils import trans_args, trans_init, print_dict
    args = None
    logger, config = trans_init(args)
    dataloader = range(20)
    prologger = ProLogger(metric=("mre", "dec"), epoch=10)
    # prologger = ProLogger(metric=("mre", "dec"), epoch=config['training']['epoch'], logger=logger)
    for epoch, trainlogger, dtrain, monitor in prologger:
        for data in trainlogger(dataloader):
            i = 0
            trainlogger.update(**{"ind": i, "data": data, "mre": data})
            # tprint("Metriclogger logging!")
            d = {"ind": i, "data": data, "mre": data}
            best = monitor.record(d, epoch=epoch)

        # for data in testlogger(dataloader):


class ProLogger:
    """
    Progress Logger
    """
    def __init__(self, iterable=None,
                 metric=None,
                 epoch=100,
                 val_interval=50,
                 logger=None,
                 config=None,
                 rank=0,
                 *args,
                 **kwargs):

        self.iterable = iterable
        self.metric = metric
        self.val_interval = val_interval
        self.num_epoch = epoch
        self.logger = logger if rank == 0 else None
        self.config = config
        self.trainlogger = MetricLogger(logger=logger, no_print=True)
        # self.testlogger = Recorder()
        self.timer = timer()
        self.init_monitor()
        pass

    def init_monitor(self):
        self.monitor = None
        if self.metric is not None:
            assert isinstance(self.metric, tuple), f"Got {self.metric}"
            monitor = Monitor(key=self.metric[0], mode=self.metric[1])
            self.monitor = monitor

    def log(self, msg, *args, **kwargs):
        if self.logger is None:
            tprint(msg, *args, **kwargs)
        else:
            self.logger.info(msg, *args, **kwargs)

    def __iter__(self):
        # timer1 = timer()
        d_train = {}
        for i in range(self.num_epoch):
            t = self.timer()
            yield i, self.trainlogger, d_train, self.monitor

            time_run = self.timer() - t
            # tprint("metriclogger.return_final_dict")
            d_train = self.trainlogger.return_final_dict()
            d_train['running_time'] = time_run
            d_train['epoch'] = i
            d_train_str = "[Prologger] "
            for k, v in d_train.items():
                if isinstance(v, float):
                    v = f"{v:.6f}"
                d_train_str += f"{k}:{v} "
            self.log(d_train_str)



class Monitor(object):
    def __init__(self, key, mode="inc"):
        """ mode = inc or dec """
        self.mode = mode
        assert mode in ['inc', 'dec']
        self.best_epoch = None
        self.best_value = None
        self.key = key
        self.best_dict = None

    def is_better(self, v):
        if self.mode == "inc":
            return v > self.best_value
        else:
            return v < self.best_value

    def record(self, d, epoch):
        isbest = self._record(d[self.key], epoch)
        if isbest:
            tprint("[Monitor] `Achive New Record` ")
            self.best_dict = d
        return {"isbest":isbest, "best_value":self.best_value, "best_epoch":self.best_epoch, **self.best_dict}

    def _record(self, v, epoch):
        if self.best_epoch is None or self.best_value is None:
            self.best_value = v
            self.best_epoch = epoch
            return True
        if self.is_better(v):
            self.best_value = v
            self.best_epoch = epoch
            return True
        else:
            return False


if __name__ == '__main__':
    usage()


