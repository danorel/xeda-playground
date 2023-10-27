import json
import pathlib
import typing as t

from data_types.pipeline import Pipeline
from data_types.sampling import SamplingMethod


def write_pipeline(
    uuid: str,
    pipeline: Pipeline,
    sampling_method: SamplingMethod,
):
    root = pathlib.Path.cwd()
    annotated_data_dir = root / "annotated_data" / sampling_method
    annotated_data_dir.mkdir(parents=True, exist_ok=True)
    annotated_pipeline = json.dumps(pipeline)
    annotated_pipeline_path = annotated_data_dir / f"pipeline_{uuid}"
    annotated_pipeline_file = pathlib.Path(annotated_pipeline_path)
    annotated_pipeline_file.write_text(annotated_pipeline)


def write_target_set(
    filename: str,
    target_set: t.Set[str],
    sampling_method: SamplingMethod,
):
    root = pathlib.Path.cwd()
    sampling_target_set_dir = root / "data" / "target_sets" / sampling_method
    sampling_target_set_dir.mkdir(parents=True, exist_ok=True)
    sampling_target_set = json.dumps(list(target_set))
    sampling_target_set_path = sampling_target_set_dir / \
        f"target_set_{filename}"
    sampling_target_set_file = pathlib.Path(sampling_target_set_path)
    sampling_target_set_file.write_text(sampling_target_set)
