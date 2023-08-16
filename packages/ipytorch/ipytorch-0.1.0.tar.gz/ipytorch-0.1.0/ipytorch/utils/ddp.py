import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
from torch.nn.parallel import DistributedDataParallel as DDP

import logging
import os
from datetime import timedelta
from torch.distributed.constants import default_pg_timeout


def set_seed(seed):
    from accelerate.utils import set_seed

    set_seed(seed)





def ddp_test(debug=False):
    rank = dist.get_rank()
    if debug:
        from IPython.core.debugger import set_trace

        set_trace()
    # create local model
    model = nn.Linear(10, 10).to(rank)
    # construct DDP model
    ddp_model = DDP(model, device_ids=[rank])
    # define loss function and optimizer
    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.001)
    # forward pass
    outputs = ddp_model(torch.randn(20, 10).to(rank))
    labels = torch.randn(20, 10).to(rank)
    # backward pass
    loss_fn(outputs, labels).backward()
    # update parameters
    optimizer.step()

    return list(ddp_model.parameters())[0].grad


def init_pg(timeout=2, backend="nccl"):
    master_addr = os.environ.get("MASTER_ADDR", "localhost")
    master_port = int(os.environ.get("MASTER_PORT", "24950"))
    world_size = int(os.environ.get("WORLD_SIZE", "1"))
    rank = int(os.environ.get("RANK", "0"))
    server_store = dist.TCPStore(
        host_name=master_addr,
        port=master_port,
        world_size=world_size,
        is_master=(rank == 0),
        # timeout=timedelta(seconds=60),
    )

    dist.init_process_group(
        backend=backend,
        world_size=world_size,
        rank=rank,
        store=server_store,
        timeout=timedelta(seconds=timeout) if timeout > 0 else default_pg_timeout,
    )
