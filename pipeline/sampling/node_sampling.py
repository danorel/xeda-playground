import pandas as pd
import typing as t
import os
import random

from data_types.pipeline import PipelineBodyItem
from utils.data_reader import read_members, read_pipelines
from utils.data_writer import write_target_set
from utils.debugging import logger


NODE_SAMPLING_RATE = float(os.environ.get("NODE_SAMPLING_RATE", "0.5"))


def find_item_set(
    members: pd.DataFrame, pipeline_body_item: PipelineBodyItem
) -> t.Set[str]:
    input_set_id = pipeline_body_item["inputSet"]["id"]
    members = members.loc[members["id"] == input_set_id]["members"].iloc[0]
    item_set = set(members[1:-1].split(", "))
    return item_set


def node_sampling(members: pd.DataFrame, pipeline_body: t.List[PipelineBodyItem]) -> list:
    leaf_pipeline_body_item = pipeline_body[-1]
    leaf_pipleine_item_set = find_item_set(
        members, leaf_pipeline_body_item)
    sampled_item_set = random.choices(list(leaf_pipleine_item_set), k=(
        round(len(leaf_pipleine_item_set) * NODE_SAMPLING_RATE)))
    return sampled_item_set


if __name__ == "__main__":
    members = read_members()
    logger.info("Node sampling of pipelines started...")
    for uuid, pipeline_head, pipeline_body in read_pipelines():
        target_set = node_sampling(members, pipeline_body)
        write_target_set(
            uuid,
            target_set=target_set,
            sampling_method="node_sampling",
        )
    logger.info("Node sampling is done and saved!")
