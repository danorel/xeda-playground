import json
import pathlib
import typing as t

from data_types.pipeline import PipelineChild, PipelineParent


def read_pipelines() -> t.Iterator[t.Tuple[PipelineChild, PipelineParent]]:
    root = pathlib.Path.cwd()
    data = root / "data"

    for pipeline_path in data.rglob("*.json"):
        pipeline_file = pathlib.Path(pipeline_path)
        uuid, pipeline = (
            pipeline_file.name.split("_")[1],
            json.loads(pipeline_file.read_text())
        )
        parent, *children = pipeline
        yield uuid, parent, children
