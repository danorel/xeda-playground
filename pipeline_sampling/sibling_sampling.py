import copy
import typing as t

from data_types.pipeline import AnnotatedPipelineChild, PipelineChild
from utils.data_reader import read_pipelines
from utils.data_writer import write_pipeline


def get_items_set(child: PipelineChild) -> t.Set[str]:
    return set(child["requestData"]["target_items"])


def annotate(child: PipelineChild, target_set: t.Set[str]) -> AnnotatedPipelineChild:
    child_set = get_items_set(child)
    total, overlap = len(target_set), len(child_set.intersection(target_set))
    percentage_of_overlap = (overlap / total) * 100
    annotated_child: AnnotatedPipelineChild = copy.deepcopy(child)
    annotated_child["annotation"] = f"{percentage_of_overlap}%"
    return annotated_child


def build_target_set(children: t.List[PipelineChild]) -> t.Set[str]:
    leaf_child = children[-1]
    target_set = get_items_set(leaf_child)
    return target_set


if __name__ == "__main__":
    for uuid, parent, children in read_pipelines():
        target_set = build_target_set(children)
        annotated_children = list(
            reversed([annotate(child, target_set) for child in children[::-1]]))
        write_pipeline(uuid, parent, annotated_children,
                       sampling_method="sibling_sampling")
