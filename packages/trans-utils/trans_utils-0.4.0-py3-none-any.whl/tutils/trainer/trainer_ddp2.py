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
    def __init__(self, 
                logger=None, 
                config=None,
                tester=None, 
                monitor=None,
                **kwargs):
        """
            mode:
                ps:  Parameter Server
                ddp: Distributed data parallel
        """
        super(DDPTrainer, self).__init__(config, tester, monitor, rank='cuda', world_size=0)
        self.logger = logger


    def init_model(self, rank, world_size, model, trainset, **kwargs):
        setup(rank, world_size)
        assert len(trainset) > 0 , f"Got {len(trainset)}"
        self.trainloader = DataLoader(dataset=trainset,
                                      batch_size=self.batch_size,
                                      num_workers=self.num_workers,
                                      shuffle=True,
                                      drop_last=True,
                                      pin_memory=True)
        if self.load_pretrain_model:
            model.load()
            
        return model

    
        

