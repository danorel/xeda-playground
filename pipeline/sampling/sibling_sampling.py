import os
import pandas as pd
import typing as t

from data_types.pipeline import PipelineBodyItem
from utils.data_reader import read_definitions, read_pipelines
from utils.data_writer import write_target_set
from utils.debugging import logger

SIBLING_SAMPLING_RATE = float(os.environ.get("SIBLING_SAMPLING_RATE", "0.5"))


def find_item_set(
    definitions: pd.DataFrame, pipeline_body_item: PipelineBodyItem
) -> t.Set[str]:
    input_set_id = pipeline_body_item["inputSet"]["id"]
    definition = definitions.loc[definitions["id"]
                                 == input_set_id]["definition"].iloc[0]
    return set(definition[1:-1].split(", "))


def sibling_sampling(definitions: pd.DataFrame, pipeline_body: t.List[PipelineBodyItem]):
    leaf_pipeline_body_item = pipeline_body[-1]
    leaf_pipleine_item_set = find_item_set(
        definitions, leaf_pipeline_body_item)
    minimum, maximum = 0., 0.
    return set([])


if __name__ == "__main__":
    definitions = read_definitions()
    logger.info("Sibling sampling of pipelines started...")
    for uuid, pipeline_head, pipeline_body in read_pipelines():
        target_set = sibling_sampling(index, pipeline_body)
        write_target_set(
            uuid,
            target_set=target_set,
            sampling_method="sibling_sampling",
        )
    logger.info("Sibling sampling is done and saved!")
