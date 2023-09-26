import json
import pathlib
import typing as t

from data_types.pipeline import PipelineParent, PipelineChild


def read_pipelines():
    root = pathlib.Path.cwd()
    data = root / "data"

    for pipeline_path in data.rglob("*.json"):
        pipeline_file = pathlib.Path(pipeline_path)
        pipeline = json.loads(pipeline_file.read_text())
        parent: PipelineParent = pipeline.pop()
        children: t.List[PipelineChild] = pipeline
        yield parent, children
