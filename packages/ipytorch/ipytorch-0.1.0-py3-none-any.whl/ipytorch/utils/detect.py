import os
import re
import sys
from pathlib import Path

import IPython

# FROM yolov3

import signal
import psutil


def kill_by_port(port):
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            connections = proc.connections()
            for conn in connections:
                if conn.laddr.port == port:
                    proc.send_signal(signal.SIGKILL)
                    logging.info(f"Killed process {proc.pid} using port {port}")
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass


def is_ascii(s=""):
    # Is string composed of all ASCII (no UTF) characters? (note str().isascii() introduced in python 3.7)
    s = str(s)  # convert list, tuple, None, etc. to str
    return len(s.encode().decode("ascii", "ignore")) == len(s)


def is_chinese(s="人工智能"):
    # Is string composed of any Chinese characters?
    return bool(re.search("[\u4e00-\u9fff]", str(s)))


def is_colab():
    # Is environment a Google Colab instance?
    return "google.colab" in sys.modules


def is_notebook():
    # Is environment a Jupyter notebook? Verified on Colab, Jupyterlab, Kaggle, Paperspace
    ipython_type = str(type(IPython.get_ipython()))
    return "colab" in ipython_type or "zmqshell" in ipython_type


def is_kaggle():
    # Is environment a Kaggle Notebook?
    return (
        os.environ.get("PWD") == "/kaggle/working"
        and os.environ.get("KAGGLE_URL_BASE") == "https://www.kaggle.com"
    )


def is_kaggle_test():
    return os.getenv("KAGGLE_IS_COMPETITION_RERUN")


def is_docker() -> bool:
    """Check if the process runs inside a docker container."""
    if Path("/.dockerenv").exists():
        return True
    try:  # check if docker is in control groups
        with open("/proc/self/cgroup") as file:
            return any("docker" in line for line in file)
    except OSError:
        return False


def is_writeable(dir, test=False):
    # Return True if directory has write permissions, test opening a file with write permissions if test=True
    if not test:
        return os.access(dir, os.W_OK)  # possible issues on Windows
    file = Path(dir) / "tmp.txt"
    try:
        with open(file, "w"):  # open file with write permissions
            pass
        file.unlink()  # remove file
        return True
    except OSError:
        return False
