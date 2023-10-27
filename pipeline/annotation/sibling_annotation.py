import copy

from utils.data_reader import read_members, read_target_sets, read_pipelines
from utils.data_writer import write_pipeline
from utils.debugging import logger
from pipeline.annotation import (
    annotate_pipeline_body,
    annotate_pipeline_body_item,
)

if __name__ == "__main__":
    target_set_dir = "node_sampling"
    members, target_set = (read_members(), read_target_sets(target_set_dir))
    logger.info(
        "Annotating pipelines in the target set directory '{0}' having {1} elements".format(
            target_set_dir, len(target_set)
        )
    )
    for uuid, pipeline_head, pipeline_body in read_pipelines():
        pipeline_body_annotation = annotate_pipeline_body(pipeline_body)
        annotated_pipeline_body = []
        for item in range(len(pipeline_body) - 1, 0, -1):
            current_pipeline_body_item, parent_pipeline_body_item = (
                pipeline_body[item],
                pipeline_body[item - 1],
            )
            pipeline_body_item_annotation = annotate_pipeline_body_item(
                current_pipeline_body_item, parent_pipeline_body_item, members, target_set
            )
            annotated_pipeline_body_item = copy.deepcopy(
                current_pipeline_body_item)
            annotated_pipeline_body_item["annotation"] = {
                **pipeline_body_annotation,
                **pipeline_body_item_annotation,
            }
            annotated_pipeline_body.insert(0, annotated_pipeline_body_item)
        annotated_pipeline = [pipeline_head] + annotated_pipeline_body
        write_pipeline(
            uuid,
            pipeline=annotated_pipeline,
            sampling_method="sibling_sampling",
        )
    logger.info("Annotation is done and saved!")
