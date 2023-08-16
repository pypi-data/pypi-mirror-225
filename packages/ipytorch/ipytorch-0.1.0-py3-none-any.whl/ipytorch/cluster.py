import asyncio
import re
import shlex
import time
from functools import partial
from pathlib import Path

import ipyparallel as ipp
import nest_asyncio
from IPython import get_ipython
from IPython.core.magic import Magics, line_magic, magics_class

# from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

# from ipyparallel.client.magics import ParallelMagics
from .ippmagic import ParallelMagics
from .utils import kill_by_port
from .logger import logging

nest_asyncio.apply()

# %%


def get_conn_file(a):
    import re

    match = re.search(r"kernel-[a-f0-9\-]+\.json", str(a))
    if match:
        extracted_string = match.group(0)
    else:
        print("No match found.")

    return extracted_string


def write_conn_file(kernels):
    import yaml

    data = {
        "session_name": "ipytorch",
        "windows": [
            {
                "window_name": "dev",
                "layout": "tiled",
                "shell_command_before": ["cd ~/.ipython/profile_default/security"],
                "panes": [],
            }
        ],
    }

    for kernel in kernels:
        data["windows"][0]["panes"].append(f"jupyter console --existing {kernel}")
    yaml_string = yaml.dump(data)
    path = Path.home() / ".ipython/tmux_profile.yaml"
    with open(path, "w") as file:
        file.write(yaml_string)
    logging.info(f"Write connect info to {path}")


def _init(
    rank=None,
    master_addr="localhost",
    master_port=24950,
    seed=62,
    **kwargs,
):
    world_size = kwargs.get("world_size", None) or (
        kwargs.get("nproc_per_node", 1) * kwargs.get("nnodes", 1)
    )

    # assert kwargs['world_size'] is not None
    # if world_size is None:
    #     world_size = nnodes * nproc_per_node
    # assert world_size == nnodes * nproc_per_node
    import os

    # import torch
    # import torch.distributed as dist

    # try:
    #     assert rank is not None
    #     assert world_size is not None

    # except Exception:
    #         from mpi4py import MPI

    #         comm = MPI.COMM_WORLD
    #         world_size = comm.Get_size()
    #         rank = comm.Get_rank()
    #     else:
    #         rank = int(os.environ["RANK"])
    #         world_size = int(os.environ["WORLD_SIZE"])

    # torch.backends.cuda.matmul.allow_tf32 = True

    """
    Overwrite cuda visible settings
    """
    # if devices:
    #     assert world_size == len(devices)
    # devices = ",".join(map(str, range(world_size))) if devices is None else devices
    # os.environ["CUDA_VISIBLE_DEVICES"] = devices
    # server_store = dist.TCPStore(
    #     host_name=master_addr,
    #     port=master_port,
    #     world_size=world_size,
    #     is_master=(rank == 0),
    #     # timeout=timedelta(seconds=60),
    # )

    # dist.init_process_group(
    #     backend=backend,
    #     world_size=world_size,
    #     rank=rank,
    #     store=server_store,
    #     timeout=timedelta(seconds=2),
    # )

    """
    Set environment
    """
    os.environ["MASTER_ADDR"] = str(master_addr)
    os.environ["MASTER_PORT"] = str(master_port)
    os.environ["RANK"] = str(rank)
    os.environ["WORLD_SIZE"] = str(world_size)
    os.environ["LOCAL_RANK"] = str(rank)
    os.environ["LOCAL_WORLD_SIZE"] = str(world_size)
    os.environ["NODE_RANK"] = str(int(rank / world_size))
    # os.environ["BACKEND"]=backend

    from ipytorch.logger import init_logger

    init_logger()


@magics_class
class Cluster(Magics):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initialized = False

    def activate(self, slice: slice = slice(None, None)):
        view: ipp.client.view.DirectView = self.client[slice]
        view.block = True
        M = IPytorchMagics(self.shell, view, "")
        # M._enable_autopx()
        M.autopx()
        self.ipymagic = M
        self.shell.magics_manager.register(M)
        logging.info(f"initialized magic {M.unique_id} at view {view}")

    def init(self):
        if self.initialized is not True:
            logging.info("Initializing cluster...")
            if self.cluster_is_local:
                kill_by_port(self.init_kwargs["master_addr"])
            view = self.client[:]
            n = self.client.cluster.n
            view.map_sync(
                partial(_init, **self.init_kwargs),
                range(n),
            )
            self.activate()
            self.initialized = True
        else:
            logging.info("Cluster is already initialized")

    def is_locally(self):
        return self.master_addr == "localhost"

    def start(self, n=None, **kwargs):
        init_kwargs = {}
        if n is None:
            import torch

            n = torch.cuda.device_count()
        n = int(n)
        init_kwargs["world_size"] = n
        init_kwargs["seed"] = kwargs.pop("seed", 62)
        init_kwargs["master_addr"] = kwargs.pop("master_addr", "localhost")
        init_kwargs["master_port"] = int(kwargs.pop("master_port", 24950))
        init_kwargs["backend"] = kwargs.pop("backend", "nccl")
        init_kwargs["init"] = kwargs.pop("backend", "nccl")
        self.init_kwargs = init_kwargs
        self.cluster_is_local = init_kwargs["master_addr"] in [
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
        ] and kwargs.get("engines", "locally") not in ["pbs", "slurm"]

        cluster = ipp.Cluster(n=n, **kwargs)
        cluster.log.setLevel(logging.get_verbosity())
        self.client = cluster.start_and_connect_sync(activate=False)
        assert len(self.client.ids) == n
        self.init()

    def wait_for_stop(self):
        sleep_timeout = 60
        sleep_time = 0
        while self.client.ids and sleep_time < sleep_timeout:
            logging.debug("Waiting for engines to stop")
            time.sleep(1)
            sleep_time += 1
        self.stopped = True

    def restart(self):
        self.ipymagic.autopx()

        async def f():
            await self.client.cluster.restart_engines()

        # task=asyncio.create_task(self.client.cluster.restart_engines())

        asyncio.run(f())
        self.wait_for_stop()
        self.client.wait_for_engines()

        # self.shell.run_cell(
        #     """
        # cluster=%cluster
        # await cluster.client.cluster.restart_engines()
        # cluster.wait_for_stop()
        # cluster.client.wait_for_engines()
        # # """
        # )
        # assert self.client[:].apply_async(lambda: 1).wait(timeout=60)
        logging.info("All engines are ready")
        self.initialized = False
        self.init()

    def parse_args(self, parts):
        args = {}
        for part in parts:
            try:
                if "=" in part:
                    key, value = part.split("=")
                    args[key.lstrip("-")] = value
                else:
                    next_part = parts[parts.index(part) + 1]
                    if not next_part.startswith("-"):
                        args[part.lstrip("-")] = next_part
                        parts.remove(next_part)
            except Exception as e:
                pass

        return args

    # @magic_arguments()
    # @argument("command", help="Command to execute")
    @line_magic
    def cluster(self, line):
        parts = shlex.split(line)
        try:
            command = parts[0]
            assert command in [
                "start",
                "stop",
                "restart",
                "status",
                "kill",
            ], "Command not supported"
        except Exception as e:
            logging.debug(f"no command specified in {line}, return cluster")
            if hasattr(self, "client"):
                return self
            else:
                return None
        parts = parts[1:]
        kwargs = self.parse_args(parts)

        logging.debug(f"running command: {command} with args: {kwargs}")
        # args = vars(parse_argstring(self.cluster, line))

        getattr(self, command)(**kwargs)

    def get_kernels(self):
        view = self.client[:]
        view.execute("import ipyparallel as ipp; ipp.bind_kernel()").wait()
        view.execute("%%capture a\n%connect_info").wait()
        kernels = list(map(get_conn_file, view.pull("a").get()))
        write_conn_file(kernels)
        return kernels


class IPytorchMagics(ParallelMagics):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import uuid

        self.unique_id = str(uuid.uuid4())[:8]

    def pxrun_nodes(self, *args, **kwargs):
        cell = self._px_cell
        logging.debug(f"using magic provided by {self.unique_id}")
        logging.debug(f"Running cell:\n{cell} at {self.view}")
        if re.search(r"^\s*%autopx\b", cell):
            self._disable_autopx()
            return False
        if re.search(r"^\s*%cluster\b", cell):
            print("Cluster magic is not supported in parallel execution, skip")
            return False
        if re.search(r"^\s*%nopx\b", cell):
            print("%autopx temporally disabled")
            cell = cell[6:]
            pxrun_nodes = self.shell.run_ast_nodes
            self.shell.run_ast_nodes = self._original_run_nodes
            self._original_run_cell(cell)
            if (
                self.shell.magics_manager.registry[self.__class__.__name__].unique_id
                != self.unique_id
            ):
                logging.info("Detecting cluster restart, do not restore %autopx")
            else:
                self.shell.run_ast_nodes = pxrun_nodes
        else:
            try:
                self.parallel_execute(cell)
            except Exception:
                self.shell.showtraceback()
                raise Exception
            else:
                return False
