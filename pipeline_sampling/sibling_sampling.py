import copy
import pandas as pd
import typing as t

from data_types.pipeline import AnnotatedPipelineChild, PipelineChild
from utils.data_reader import read_index, read_target_set, read_pipelines
from utils.data_writer import write_pipeline
from utils.debugging import logger


def find_child_set(index: pd.DataFrame, child: PipelineChild) -> t.Set[str]:
    query = child["inputSet"]["id"]
    definition = index.loc[index['id'] == query]['definition'].iloc[0]
    ids = definition[1:-1].split(', ')
    return set(ids)


def annotate(child: PipelineChild, index: pd.DataFrame, target_set: t.Set[str]) -> AnnotatedPipelineChild:
    child_set = find_child_set(index, child)
    total, overlap = len(target_set), len(child_set.intersection(target_set))
    percentage_of_overlap = (overlap / total) * 100
    annotated_child: AnnotatedPipelineChild = copy.deepcopy(child)
    annotated_child["annotation"] = f"{percentage_of_overlap}%"
    return annotated_child


if __name__ == "__main__":
    target_set_name = 'grean-peas'
    index, target_set = (
        read_index(),
        read_target_set(target_set_name)
    )
    logger.info("Annotating pipelines with target set '{0}' having {1} elements".format(
        target_set_name,
        len(target_set)
    ))
    for uuid, parent, children in read_pipelines():
        annotated_children = list(
            reversed([annotate(child, index, target_set) for child in children[::-1]]))
        write_pipeline(uuid, parent, annotated_children,
                       sampling_method="sibling_sampling")
    logger.info("Annotation is done and saved!")
