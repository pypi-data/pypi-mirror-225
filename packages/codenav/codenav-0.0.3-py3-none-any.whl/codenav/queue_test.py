"""
module docstring here
"""

import time
import logging


def main():
    """main."""
    logging.basicConfig(
        format="    %(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%d-%m-%y %H:%M:%S",
        level=logging.INFO,
    )
    logger = logging.getLogger("printlog")
    timestep = 0.02
    for i in range(100):
        time.sleep(timestep)
        logstr = f"queue_test_index: {i}"
        logger.info(logstr)
    logstr = f"queue_total_time: {timestep * 100}"
    logger.info(logstr)
    # raise FileExistsError("dis for testing lol")
    # extra comment here


main()
