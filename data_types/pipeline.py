import typing as t
import typing_extensions as te

from data_types.annotation import Annotation


"""
common variables for pipeline formats 
"""

ID: te.TypeAlias = str
Operator = te.Literal["by_facet", "by_neighbors", "by_superset"]
Dimension = te.Literal["i", "r", "z"]
TargetSet = te.Literal["Scattered"]


class Predicate(te.TypedDict):
    dimension: Dimension
    value: str


"""
dora pipeline format
"""


class InputSetDora(te.TypedDict):
    length: int
    id: int
    predicate: t.List[Predicate]
    silhouette: t.Optional[t.Any]
    novelty: t.Optional[t.Any]


class RequestDataDora(te.TypedDict):
    get_scores: bool
    get_predicted_scores: bool
    seen_predicates: t.List[str]
    input_set_id: int
    dimensions: t.List[str]
    target_set: str
    curiosity_weight: float
    target_items: t.List[ID]
    found_items_with_ratio: t.Dict[ID, float]
    previous_set_states: t.List[t.List[float]]
    previous_operation_states: t.List[t.List[float]]


class PipelineItemDora(te.TypedDict):
    selectedSetId: t.Optional[str]
    operator: str
    checkedDimension: str
    url: str
    inputSet: t.Optional[InputSetDora]
    reward: float
    curiosityReward: float
    requestData: RequestDataDora


class AnnotatedPipelineItemDora(PipelineItemDora):
    annotation: Annotation


"""
eda4sum pipeline format
"""


class InputSetEda4Sum(te.TypedDict):
    length: int
    id: int
    predicate: t.List[Predicate]
    item_class: str
    uniformity: int


class RequestDataEda4Sum(te.TypedDict):
    get_scores: bool
    get_predicted_scores: bool
    seen_sets: t.List[int]
    dataset_to_explore: str
    utility_weights: t.List[float]
    input_set_id: int
    previous_set_statest: t.List
    target_set: str
    curiosity_weight: str
    target_items: str
    found_items_with_ratio: str
    previous_operations: t.List[str]
    dataset_ids: t.List[int]
    evolving_parameter: str
    evolution_type: str
    weights_mode: str


class PipelineItemEda4Sum(te.TypedDict):
    selectedSetId: int
    operator: Operator
    checkedDimension: str
    url: str
    inputSet: t.Optional[InputSetEda4Sum]
    requestData: t.Optional[RequestDataEda4Sum]
    reward: int
    utility: float
    uniformity: float
    novelty: float
    distance: float
    utilityWeights: t.List[float]
    galaxy_class_score: float
    class_score_found_12: int
    class_score_found_15: int
    class_score_found_18: int
    class_score_found_21: int


class AnnotatedPipelineItemEda4Sum(PipelineItemEda4Sum):
    annotation: Annotation


PipelineType = te.Literal["dora", "eda4sum"]
PipelineKind = te.Literal["raw", "annotated"]

PipelineDora = t.List[PipelineItemDora]
PipelineEda4Sum = t.List[PipelineItemEda4Sum]

AnnotatedPipelineDora = t.List[AnnotatedPipelineItemDora]
AnnotatedPipelineEda4Sum = t.List[AnnotatedPipelineItemEda4Sum]

T = te.TypeVar("T")
K = te.TypeVar("K")

# TODO: te.Generic[T, K]
Pipeline = t.List
