from typing import Any, Literal, Optional, TypeAlias, TypedDict

ID: TypeAlias = str
Operator = Literal["by_facet", "by_neighbors"]
Dimension = Literal["i", "r", "z"]
TargetSet = Literal["Scattered"]


class Predicate(TypedDict):
    dimension: Dimension
    value: str


class InputSet(TypedDict):
    length: int
    id: int
    predicate: list[Predicate]
    silhouette: Optional[Any]
    novelty: Optional[Any]


class RequestData(TypedDict):
    get_scores: bool
    get_predicted_scores: bool
    seen_predicates: list[str]
    input_set_id: int
    dimensions: list[str]
    target_set: str
    curiosity_weight: float
    target_items: list[ID]
    found_items_with_ratio: dict[ID, float]
    previous_set_states: list[list[float]]
    previous_operation_states: list[list[float]]


class PipelineParent(TypedDict):
    selectedSetId: Optional[str]
    operator: str
    checkedDimension: str
    url: str
    inputSet: Optional[InputSet]
    reward: float
    curiosityReward: float


class PipelineChild(PipelineParent):
    requestData: RequestData
