from utils.data_reader import read_pipelines
from utils.data_writer import write_pipeline
from utils.debugging import logger
from pipeline.annotation import (
    annotate_pipeline,
)

if __name__ == "__main__":
    logger.info("Into node_annotation")

    for uuid, pipeline in read_pipelines("eda4sum", "annotated"):
        annotated_pipeline = annotate_pipeline(pipeline)
        write_pipeline(uuid, annotated_pipeline, "eda4sum", "annotated")

    logger.info("Annotation is done and saved!")
