import copy
import pandas as pd
import typing as t

from data_types.pipeline import AnnotatedPipelineChild, PipelineChild
from utils.data_reader import read_index, read_target_set, read_pipelines
from utils.data_writer import write_pipeline
from utils.debugging import logger


def get_items_set(index_df: pd.DataFrame, child: PipelineChild) -> t.Set[str]:
    input_set_id = child["inputSet"]["id"]
    input_set = index_df.loc[index_df['id'] == input_set_id]
    print(input_set)
    return set(input_set['definition'])


def annotate(child: PipelineChild, index_df: pd.DataFrame, target_set: t.Set[str]) -> AnnotatedPipelineChild:
    child_set = get_items_set(index_df, child)
    total, overlap = len(target_set), len(child_set.intersection(target_set))
    percentage_of_overlap = (overlap / total) * 100
    annotated_child: AnnotatedPipelineChild = copy.deepcopy(child)
    annotated_child["annotation"] = f"{percentage_of_overlap}%"
    return annotated_child


if __name__ == "__main__":
    index_df, target_set = (
        read_index(),
        read_target_set('grean-peas')
    )
    logger.info("Annotating pipelines with {0} target set".format(target_set))
    for uuid, parent, children in read_pipelines():
        annotated_children = list(
            reversed([annotate(child, index_df, target_set) for child in children[::-1]]))
        write_pipeline(uuid, parent, annotated_children,
                       sampling_method="sibling_sampling")
    logger.info("Annotation is done as saved!")
