import random

from utils.data_reader import read_group
from utils.debugging import logger


def node_sampling(percent=0.5) -> list:
    group = read_group()
    logger.info("Node sampling started...")
    node = group.sample().iloc[0, 2]
    node = node.split(", ")
    indexes = random.choices(node, k=(round(len(node) * percent)))
    logger.info("Node sampling finished ...")
    return indexes


if __name__ == "__main__":
    print(node_sampling(0.5))
