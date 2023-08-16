import os

import colorlog
from absl import logging
from socket import gethostname

# %%


class IPytorchFormatter(colorlog.ColoredFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rank = os.environ.get("RANK", "0")
        self.world_size = os.environ.get("WORLD_SIZE", "1")
        rank = f"RANK {self.rank}/{self.world_size}" if int(self.world_size) > 1 else ""
        self.prefix = f"{rank} {gethostname()}: "

    def format(self, record):
        return self.prefix + super().format(record)
        # record = ColoredRecord(record, self.escape_codes)


def init_logger():
    ipformatter = IPytorchFormatter(
        # "%(log_color)s%(levelname)s %(asctime)s %(thread)d:%(filename)s:%(lineno)d] %(message)s",
        "%(log_color)s%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
        datefmt="%I:%M:%S %p",
    )

    # %%

    logging.get_absl_handler().setFormatter(ipformatter)
    logging.use_absl_handler()
    logging._warn_preinit_stderr = 0
    logging.set_verbosity(logging.INFO)


init_logger()
