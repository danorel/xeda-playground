import json
import pathlib
import typing as t

from data_types.pipeline import Pipeline, PipelineType, PipelineKind
from data_types.sampling import SamplingMethod


def write_pipeline(
    filename: str,
    pipeline: Pipeline,
    pipeline_type: PipelineType,
    pipeline_kind: PipelineKind = "raw"
):
    root = pathlib.Path.cwd()
    pipeline_dir = root / "datasets" / "pipelines" / pipeline_type / pipeline_kind
    pipeline_dir.mkdir(parents=True, exist_ok=True)
    pipeline = json.dumps(pipeline)
    pipeline_path = pipeline_dir / f"pipeline_{filename}"
    pipeline_file = pathlib.Path(pipeline_path)
    pipeline_file.write_text(pipeline)


def write_target_set(
    filename: str,
    target_set: t.Set[str],
    sampling_method: SamplingMethod,
):
    root = pathlib.Path.cwd()
    sampling_target_set_dir = root / "datasets" / "target_sets" / sampling_method
    sampling_target_set_dir.mkdir(parents=True, exist_ok=True)
    sampling_target_set = json.dumps(list(target_set))
    sampling_target_set_path = sampling_target_set_dir / \
        f"target_set_{filename}"
    sampling_target_set_file = pathlib.Path(sampling_target_set_path)
    sampling_target_set_file.write_text(sampling_target_set)
