from dataclasses import dataclass
from typing import List, Dict

@dataclass
class gen_Dataset:
    tokens: List[List[str]]
    true_tags: List[List[str]]
    label2id: Dict[str, int]
    id2label: Dict[int, str]

@dataclass
class PredictionResult:
    y_true: List[List[str]]
    y_pred: List[List[str]]

@dataclass
class EvalMetric:
    f1: float
    precision: float
    recall: float