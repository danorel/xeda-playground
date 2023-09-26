from typing import Any, Dict, List, Optional
from typing_extensions import Literal, TypeAlias, TypedDict

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
    predicate: List[Predicate]
    silhouette: Optional[Any]
    novelty: Optional[Any]


class RequestData(TypedDict):
    get_scores: bool
    get_predicted_scores: bool
    seen_predicates: List[str]
    input_set_id: int
    dimensions: List[str]
    target_set: str
    curiosity_weight: float
    target_items: List[ID]
    found_items_with_ratio: Dict[ID, float]
    previous_set_states: List[List[float]]
    previous_operation_states: List[List[float]]


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
