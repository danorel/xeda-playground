import pandas as pd
import typing as t

from data_types.pipeline import PipelineEda4Sum, PipelineItemEda4Sum, AnnotatedPipelineEda4Sum, AnnotatedPipelineItemEda4Sum
from data_types.annotation import Annotation

from utils.data_reader import read_members
from utils.debugging import logger

SEEN_GALAXIES = []
MEMBERS = read_members()


def find_item_set(
        members: pd.DataFrame, pipeline_body_item: PipelineItemEda4Sum
) -> t.Set[str]:
    input_set_id = pipeline_body_item["inputSet"]["id"]
    members = members.loc[members["id"] == input_set_id]["members"].iloc[0]
    input_set = set(members[1:-1].split(", "))
    return input_set


def _find_remaining_operators(pipeline: PipelineEda4Sum) -> dict:
    operators = {}
    pipeline = pipeline[1:]
    for pipeline_item in pipeline:
        current_operator = pipeline_item["operator"]
        if current_operator in operators.keys():
            operators[current_operator] += 1
        else:
            operators[current_operator] = 1

    return operators


def _find_delta_uniformity(pipeline_item_current: PipelineItemEda4Sum,
                           pipeline_item_next: PipelineItemEda4Sum) -> float:
    return pipeline_item_next["uniformity"] - pipeline_item_current["uniformity"]


def _find_delta_novelty(pipeline_item_current: PipelineItemEda4Sum,
                        pipeline_item_next: PipelineItemEda4Sum) -> float:
    return pipeline_item_next["novelty"] - pipeline_item_current["novelty"]


def _find_delta_diversity(pipeline_item_current: PipelineEda4Sum,
                          pipeline_item_next: PipelineEda4Sum) -> float:
    return pipeline_item_next["distance"] - pipeline_item_current["distance"]


def _find_delta_galaxy_score(pipeline_item_current: PipelineEda4Sum,
                             pipeline_item_next: PipelineEda4Sum) -> float:
    return pipeline_item_next["galaxy_class_score"] - pipeline_item_current["galaxy_class_score"]


def _find_utility_weights(pipeline_item_current: PipelineEda4Sum,
                          pipeline_item_next: PipelineEda4Sum) -> t.List[float]:
    return [pipeline_item_next["utilityWeights"][i] - pipeline_item_current["utilityWeights"][i] for i in range(3)]


def _find_familiarity_curiosity(item_members) -> t.Tuple[float, float]:
    if len(SEEN_GALAXIES) == 0:
        return [0.0, 0.0]
    else:
        common_members_number = sum(
            1 for elem in item_members if elem in SEEN_GALAXIES)
        familiarity = common_members_number / (len(SEEN_GALAXIES))
        separate_members_number = sum(
            1 for elem in item_members if elem not in SEEN_GALAXIES)
        curiosity = separate_members_number / (len(SEEN_GALAXIES))
        return [familiarity, curiosity]


def annotate_pipeline(pipeline: PipelineEda4Sum) -> AnnotatedPipelineEda4Sum:
    length = len(pipeline)
    annotated_pipeline: AnnotatedPipelineEda4Sum = []

    for item in range(length):
        if item is not length - 1:
            delta_uniformity = _find_delta_uniformity(
                pipeline[item], pipeline[item + 1])
            delta_novelty = _find_delta_novelty(
                pipeline[item], pipeline[item + 1])
            delta_diversity = _find_delta_diversity(
                pipeline[item], pipeline[item + 1])
            delta_galaxy_score = _find_delta_galaxy_score(
                pipeline[item], pipeline[item + 1])
            delta_utility_weights = _find_utility_weights(
                pipeline[item], pipeline[item + 1])
        else:
            delta_uniformity = 0
            delta_novelty = 0
            delta_diversity = 0
            delta_galaxy_score = 0
            delta_utility_weights = [0.0, 0.0, 0.0]

        familiarity = 0.0
        curiosity = 0.0

        if "requestData" in pipeline[item].keys():

            input_set_id = pipeline[item]["selectedSetId"]
            item_members = MEMBERS.loc[MEMBERS["id"]
                                       == input_set_id]["members"]

            for i in item_members:
                list_members = i[1:-1].split(", ")
                result_members = [int(num) for num in list_members]

            if item_members.empty:
                logger.warn(f"Node[id={input_set_id}] is missing in .csv")
            else:
                familiarity, curiosity = _find_familiarity_curiosity(
                    result_members)

                SEEN_GALAXIES.extend(result_members)

        annotation = Annotation(total_length=length,
                                remaining_operators=_find_remaining_operators(
                                    pipeline[item:]),
                                current_operator=pipeline[item]["operator"],
                                delta_uniformity=delta_uniformity,
                                delta_novelty=delta_novelty,
                                delta_diversity=delta_diversity,
                                delta_score_galaxy=delta_galaxy_score,
                                delta_utilityWeights=delta_utility_weights,
                                current_uniformity=pipeline[item]["uniformity"],
                                current_novelty=pipeline[item]["novelty"],
                                current_diversity=pipeline[item]["distance"],
                                current_score_galaxy=pipeline[item]["galaxy_class_score"],
                                current_utilityWeights=pipeline[item]["utilityWeights"],
                                final_uniformity=pipeline[-1]["uniformity"],
                                final_novelty=pipeline[-1]["novelty"],
                                final_diversity=pipeline[-1]["distance"],
                                final_score_galaxy=pipeline[-1]["galaxy_class_score"],
                                final_utilityWeights=pipeline[-1]["utilityWeights"],
                                familiarity=familiarity,
                                curiosity=curiosity)
        annotated_pipeline_item = AnnotatedPipelineItemEda4Sum(
            **pipeline[item], annotation=annotation)
        annotated_pipeline.append(annotated_pipeline_item)

    return annotated_pipeline
