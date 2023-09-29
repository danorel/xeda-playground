import json
import pathlib

from data_types.pipeline import Pipeline
from data_types.sampling import SamplingMethod


def write_pipeline(
    uuid: str,
    pipeline: Pipeline,
    sampling_method: SamplingMethod,
):
    root = pathlib.Path.cwd()
    annotated_data = root / "annotated_data" / sampling_method
    annotated_data.mkdir(parents=True, exist_ok=True)
    annotated_pipeline = json.dumps(pipeline)
    annotated_pipeline_path = annotated_data / f"pipeline_{uuid}"
    annotated_pipeline_file = pathlib.Path(annotated_pipeline_path)
    annotated_pipeline_file.write_text(annotated_pipeline)
