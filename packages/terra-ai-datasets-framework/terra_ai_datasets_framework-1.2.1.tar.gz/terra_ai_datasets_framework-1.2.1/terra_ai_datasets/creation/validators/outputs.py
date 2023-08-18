from enum import Enum
from typing import Dict, Optional, List

from pydantic import BaseModel
from pydantic.types import PositiveInt
from pydantic.color import Color

from terra_ai_datasets.creation.validators.inputs import ImageProcessTypes


class RegressionScalers(str, Enum):
    none = None
    min_max_scaler = "MinMaxScaler"
    standard_scaler = "StandardScaler"


class RegressionValidator(BaseModel):
    preprocessing: RegressionScalers = RegressionScalers.none


class ClassificationValidator(BaseModel):
    one_hot_encoding: bool
    classes_names: Optional[List[str]] = None


class SegmentationValidator(BaseModel):
    rgb_range: PositiveInt
    classes: Dict[str, Color]
    height: Optional[PositiveInt] = None
    width: Optional[PositiveInt] = None
    process: Optional[ImageProcessTypes] = None


# --- Timeseries validators ---
class DepthScalers(str, Enum):
    none = None
    min_max_scaler = "MinMaxScaler"
    standard_scaler = "StandardScaler"


class DepthValidator(BaseModel):
    depth: PositiveInt
    preprocessing: DepthScalers
    length: Optional[PositiveInt] = None
    step: Optional[PositiveInt] = None


class TrendValidator(BaseModel):
    deviation: float
    one_hot_encoding: bool
    classes_names: List[str] = ["Не изменился", "Вверх", "Вниз"]
    length: Optional[PositiveInt] = None
    step: Optional[PositiveInt] = None
