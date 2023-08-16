from .cluster import Cluster
import logging
from IPython import get_ipython
import gc


def collect_garbage():
    before_count = len(gc.get_objects())
    unreachable_objects_count = gc.collect()
    after_count = len(gc.get_objects())
    cleaned_count = before_count - after_count
    if cleaned_count > 0:
        logging.info(f"Successfully cleaned {cleaned_count} objects!")
    else:
        logging.info("No objects were cleaned.")

    if unreachable_objects_count > 0:
        logging.debug(f"Found {unreachable_objects_count} unreachable objects.")

    if len(gc.garbage) > 0:
        logging.debug(f"Warning: {len(gc.garbage)} uncollectable objects found!")


def gc_magic(line):
    try:
        import torch

        collect_garbage()

        torch.cuda.empty_cache()
    except Exception as e:
        pass
    collect_garbage()


def skip_if(line, cell=None):
    """Skips execution of the current line/cell if line evaluates to True."""
    IP = get_ipython()
    if IP.run_cell(line).result:
        logging.info("Skipping cell")
        return

    logging.debug(cell)
    # print(cell)
    IP.run_cell(cell)


def run_if(line, cell=None):
    IP = get_ipython()
    if IP.run_cell(line).result:
        logging.debug(cell)
        # print(cell)
        IP.run_cell(cell)
    else:
        logging.info("Skipping cell")


def load_ipython_extension(ipython):
    ipython.register_magics(Cluster)
    ipython.register_magic_function(skip_if, "line_cell")
    ipython.register_magic_function(run_if, "line_cell")
    ipython.register_magic_function(gc_magic, "line", "gc")
    # ipython.ast_node_interactivity = "all"


__all__ = ["load_ipython_extension"]
