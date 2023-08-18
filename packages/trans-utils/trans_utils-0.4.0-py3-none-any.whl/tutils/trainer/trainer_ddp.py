import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data import DataLoader, Dataset
from .trainer_abstract import AbstractTrainer

import torch.multiprocessing as mp
import torch.distributed as dist
import tempfile
from torch.nn.parallel import DistributedDataParallel as DDP
from tutils import tfilename
from torch.cuda.amp import autocast, GradScaler

# export MASTER_ADDR=192.168.1.100
# export MASTER_PORT=12345


def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'

    # initialize the process group
    dist.init_process_group("gloo", rank=rank, world_size=world_size)

def cleanup():
    dist.destroy_process_group()


def ddp(rank, world_size):
    print(f"Running basic DDP example on rank {rank}.")

    # create model and move it to GPU with id rank
    model = model.to(rank)
    ddp_model = DDP(model, device_ids=[rank])

    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.001)

    optimizer.zero_grad()
    outputs = ddp_model(torch.randn(20, 10))
    labels = torch.randn(20, 5).to(rank)
    loss_fn(outputs, labels).backward()
    optimizer.step()

    cleanup()



class DDPTrainer(AbstractTrainer):
    def __init__(self, config, tester=None, monitor=None, rank='cuda', world_size=0, logger=None):
        super().__init__(config, tester, monitor, rank, world_size)
        self.rank = rank
        self.logger = logger
        self.logging_available =  (self.rank == 0 or self.rank == 'cuda')
        print("Running on ", rank)
        if self.logging_available:
            print(f"Logger at Process(rank={rank})")
            self.recorder = Recorder(reduction=self.recorder_mode)
            self.recorder_test = Recorder(reduction=self.recorder_mode)
            self.logger = None
            self.csvlogger = CSVLogger(tfilename(self.runs_dir, "best_record"))
            self.csvlogger_all = CSVLogger(tfilename(self.runs_dir, "all_record"))
            self.monitor = monitor
            self.tester = tester
            
            self.logger = get_logger(config)
            assert self.logger is not None, f"Got rank {self.rank}"
        
        if self.use_amp:
            self.scalar = GradScaler()
            print("Debug settings: use amp=",self.use_amp)

    def init_model(self, model, trainset, **kwargs):
        assert len(trainset) > 0 , f"Got {len(trainset)}"

        # Use CacheDataset
        # trainset = CacheDataset(trainset, num_workers=12, cache_rate=0.5)
        self.trainloader = DataLoader(dataset=trainset,
                                      batch_size=self.batch_size,
                                      num_workers=8,
                                      shuffle=True,
                                      drop_last=True,
                                      pin_memory=True)
        if self.load_pretrain_model:
            model.module.load()
        rank = self.rank
        model = model.to(rank)
        ddp_model = DDP(model, device_ids=[rank])
        return ddp_model

    def configure_optim(self, model, **kwargs):
        # Set optimizer and scheduler
        optim_configs = model.module.configure_optimizers()
        assert isinstance(optim_configs, dict)
        optimizer = optim_configs['optimizer']
        scheduler = optim_configs['scheduler']

        if self.load_optimizer:
            start_epoch = model.module.load_optim(optimizer)
        else:
            start_epoch = self.start_epoch
        return optimizer, scheduler, start_epoch

    def save(self, model, epoch, type=None, optimizer=None, **kwargs):
        if self.logging_available:
            if type is None:
                # if self.save_interval > 0 and epoch % self.save_interval == 0:
                save_name = "/ckpt/model_epoch_{}.pth".format(epoch)
                model.module.save(tfilename(self.runs_dir, save_name), epoch=epoch)
                self.logger.info(f"Epoch {epoch}: Save model to ``{save_name}``! ")
            elif type == 'best':
                # save_name = "/ckpt/best_model_epoch_{}.pth".format(epoch)
                save_name2 = "/ckpt_v/model_best.pth"
                # model.save(tfilename(self.runs_dir, save_name), epoch=epoch, is_best=True)
                model.module.save(tfilename(self.runs_dir, save_name2), epoch=epoch, is_best=True)
                self.logger.info(f"[Best model] Epoch {epoch}: Save model to ``{save_name2}``! ")
            elif type == 'latest':
                if self.save_interval > 0 and epoch % self.save_interval == 0:
                    save_name = "/ckpt_v/model_latest.pth"
                    model.module.save(tfilename(self.runs_dir, save_name), epoch=epoch, is_latest=True)
                    save_optim_name = "/ckpt/optim_latest.pth"
                    model.module.save_optim(tfilename(self.runs_dir, save_optim_name), optimizer=optimizer, epoch=epoch)
                    self.logger.info(f"Epoch {epoch}: Save checkpoint to ``{save_name}``")

    def train(self, model, trainloader, epoch, optimizer, scheduler=None, do_training_log=True):
        model.train()
        out = {}
        if do_training_log and self.logging_available:
            self.recorder.clear()
            time_record = 0.1111
            self.timer_batch()

        success_count = 0
        failed_count = 0
        for load_time, batch_idx, data in tenum(trainloader):
            optimizer.zero_grad()
            self.timer_data()
            # training steps
            for k, v in data.items():
                if isinstance(v, torch.Tensor):
                    data[k] = v.to(self.rank)
            time_data_cuda = self.timer_data()
            if self.use_amp:           
                with autocast():
                    self.timer_net()
                    try:
                        out = model.module.training_step(data, batch_idx, epoch=epoch)
                    except Exception as e:
                        msg = f"Ignore Error! {e}"
                        if self.logging_available:
                            self.logger.info(msg)
                        else:
                            print(msg)
                        continue
                    assert isinstance(out, dict)
                    time_fd = self.timer_net()
                    loss = out['loss']
                    self.scalar.scale(loss).backward()
                    self.scalar.step(optimizer)
                    self.scalar.update()
                    time_bp = self.timer_net()
            else:
                self.timer_net()
                try:
                    out = model.module.training_step(data, batch_idx, epoch=epoch)
                except Exception as e:
                    msg = f"Ignore Error! {e}"
                    if self.logging_available:
                        self.logger.info(msg)
                    else:
                        print(msg)
                    continue
                if out['loss'] is None:
                    failed_count += 1
                    continue
                if torch.isnan(out['loss']):
                    print("Ignore Nan Value: ", out['loss'])
                    failed_count += 1
                    # raise ValueError(f"Get loss: {out['loss']}")
                assert isinstance(out, dict)
                time_fd = self.timer_net()
                loss = out['loss']
                loss.backward()
                optimizer.step()
                time_bp = self.timer_net()
                success_count += 1

            time_batch = self.timer_batch()
            # batch logger !
            if self.logging_available and do_training_log:
                out['time_load'] = load_time
                out['time_cuda'] = time_data_cuda
                out['time_forward'] = time_fd
                out['time_bp'] = time_bp
                out['time_record'] = time_record
                out['time_batch'] = time_batch
                self.timer_data()
                self.recorder.record(out)
                time_record = self.timer_data()
                print(f"Epoch: {epoch}. Processing batch_idx:{batch_idx} / {len(trainloader)}, time_load: {load_time}", end='\r')
                # for debug !
                if epoch == 0:
                    if self.logging_available:
                        self.logger.info("[*] Debug Checking Pipeline !!!")
                    return
        if scheduler is not None:
            scheduler.step()        
    
    
        

