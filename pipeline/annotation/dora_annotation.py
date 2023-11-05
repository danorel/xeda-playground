import copy

from utils.data_reader import read_members, read_target_sets, read_pipelines
from utils.data_writer import write_pipeline
from utils.debugging import logger
from pipeline.annotation import (
    annotate_pipeline_body,
    annotate_pipeline_body_item,
)

if __name__ == "__main__":
    members = read_members()
    for filename, pipeline in read_pipelines("dora", "raw"):
        pipeline_head, *pipeline_body = pipeline
        pipeline_body_annotation = annotate_pipeline_body(pipeline_body)
        annotated_pipeline_body = []
        for item in range(len(pipeline_body) - 1, 0, -1):
            current_pipeline_body_item, parent_pipeline_body_item = (
                pipeline_body[item],
                pipeline_body[item - 1],
            )
            pipeline_body_item_annotation = annotate_pipeline_body_item(
                current_pipeline_body_item, parent_pipeline_body_item, members
            )
            annotated_pipeline_body_item = copy.deepcopy(
                current_pipeline_body_item)
            annotated_pipeline_body_item["annotation"] = {
                **pipeline_body_annotation,
                **pipeline_body_item_annotation,
            }
            annotated_pipeline_body.insert(0, annotated_pipeline_body_item)
        annotated_pipeline = [pipeline_head] + annotated_pipeline_body
        write_pipeline(filename, annotated_pipeline, "dora", "annotated")
    logger.info("Annotation is done and saved!")
