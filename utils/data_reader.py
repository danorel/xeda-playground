import json
import pandas as pd
import pathlib
import typing as t

from tqdm import tqdm

from data_types.pipeline import PipelineChild, PipelineParent
from utils.debugging import logger


def read_pipelines() -> t.Iterator[t.Tuple[PipelineChild, PipelineParent]]:
    root = pathlib.Path.cwd()
    data = root / "data" / "pipelines"
    logger.info("Starting reading pipelines...")
    for pipeline_path in tqdm(data.rglob("*.json")):
        pipeline_file = pathlib.Path(pipeline_path)
        uuid, pipeline = (
            pipeline_file.name.split("_")[1],
            json.loads(pipeline_file.read_text())
        )
        parent, *children = pipeline
        yield uuid, parent, children
    logger.info("Finished reading pipelines...")


def read_target_set(target_set_name: str) -> t.Set[str]:
    root = pathlib.Path.cwd()
    target_set_path = root / "data" / "target_sets" / f"{target_set_name}.json"
    target_set_file = pathlib.Path(target_set_path)
    return set(json.loads(target_set_file.read_text()))


def read_index() -> pd.DataFrame:
    root = pathlib.Path.cwd()
    index = root / "data" / "index.csv"
    logger.info("Starting reading index...")
    index_df = pd.read_csv(index)
    logger.info("Finished reading index...")
    return index_df
