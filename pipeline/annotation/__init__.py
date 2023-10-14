import pandas as pd
import statistics
import typing as t

from data_types.annotation import PipelineBodyAnnotation, PipelineBodyItemAnnotation
from data_types.pipeline import AnnotatedPipelineBodyItem, PipelineBodyItem


def find_item_set(
    members: pd.DataFrame, pipeline_body_item: PipelineBodyItem
) -> t.Set[str]:
    input_set_id = pipeline_body_item["inputSet"]["id"]
    members = members.loc[members["id"] == input_set_id]["members"].iloc[0]
    input_set = set(members[1:-1].split(", "))
    return input_set


# TODO: Double-check whether curiosity is stored in 'curiosity_weight' feature
def _find_curiosity(pipeline_body_item: PipelineBodyItem) -> float:
    return float(
        pipeline_body_item.get("requestData", {}).get(
            "curiosity_weight", "0.0")
    )


# TODO: Find where familiarity is stored. Possibly, during policy training.
def _find_familiarity(pipeline_body_item: PipelineBodyItem) -> float:
    return 0.0


# TODO: Find where remaining operators are stored. Possibly, in pipeline JSON.
def _find_remaining_operators(pipeline_body_item: PipelineBodyItem):
    return []


def annotate_pipeline_body(pipeline_body: t.List[PipelineBodyItem]) -> dict:
    leaf_pipeline_body_item = pipeline_body[-1]
    return PipelineBodyAnnotation(
        final_curiosity=_find_curiosity(leaf_pipeline_body_item),
        average_curiosity=statistics.mean(
            [_find_curiosity(pipeline_body_item)
             for pipeline_body_item in pipeline_body]
        ),
        final_familiarity=_find_familiarity(leaf_pipeline_body_item),
        average_familiarity=statistics.mean(
            [
                _find_familiarity(pipeline_body_item)
                for pipeline_body_item in pipeline_body
            ]
        ),
        total_length_of_pipeline=len(pipeline_body) + 1,
    )


def annotate_pipeline_body_item(
    current_pipeline_body_item: PipelineBodyItem,
    parent_pipeline_body_item: PipelineBodyItem,
    members: pd.DataFrame,
    target_set: t.Set[str],
) -> AnnotatedPipelineBodyItem:
    current_pipeline_body_item_set = find_item_set(
        members, current_pipeline_body_item)
    return PipelineBodyItemAnnotation(
        target_set_rate=len(
            current_pipeline_body_item_set.intersection(target_set))
        / len(target_set),
        delta_curisity=_find_curiosity(current_pipeline_body_item)
        - _find_curiosity(parent_pipeline_body_item),
        delta_familiarity=_find_familiarity(current_pipeline_body_item)
        - _find_familiarity(parent_pipeline_body_item),
        remaining_operators=_find_remaining_operators(
            current_pipeline_body_item),
    )
