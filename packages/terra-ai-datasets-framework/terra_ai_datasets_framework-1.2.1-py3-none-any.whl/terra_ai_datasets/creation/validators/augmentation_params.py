from enum import Enum
from typing import Tuple, Dict

from pydantic import BaseModel, validator
from pydantic.types import PositiveInt


class AugmentationMode(Enum):
    light = "Light"
    medium = "Medium"
    maximum = "Maximum"


# --- Image augmentation ---
class ImageAugmentationFliplr(BaseModel):
    p: float

    @validator("p")
    def _validate_p(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Ensure "p" value is in range between 0.0 and 1.0')
        return v


class ImageAugmentationFlipud(BaseModel):
    p: float

    @validator("p")
    def _validate_p(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Ensure "p" value is in range between 0.0 and 1.0')
        return v


class ImageAugmentationCrop(BaseModel):
    px: Tuple[PositiveInt, PositiveInt]


class ImageAugmentationLinearContrast(BaseModel):
    alpha: Tuple[float, float]

    @validator("alpha")
    def _validate_alpha(cls, v):
        if not v[0] < v[1]:
            raise ValueError(f'First value "{v[0]}" must be no greater than second "{v[1]}"')
        return v


class ImageAugmentationAffine(BaseModel):
    scale: Dict[str, Tuple[float, float]]
    translate_percent: Dict[str, Tuple[float, float]]
    rotate: Tuple[int, int]
    shear: Tuple[int, int]


class ImageAugmentationAdditiveGaussianNoise(BaseModel):
    loc: int
    scale: Tuple[float, float]
    per_channel: float


class ImageAugmentationMultiply(BaseModel):
    mul: Tuple[float, float]
    per_channel: float


class ImageAugmentationParameters(BaseModel):
    Fliplr: ImageAugmentationFliplr = None
    Flipud: ImageAugmentationFlipud = None
    Crop: ImageAugmentationCrop = None
    LinearContrast: ImageAugmentationLinearContrast = None
    AdditiveGaussianNoise: ImageAugmentationAdditiveGaussianNoise = None
    Multiply: ImageAugmentationMultiply = None
    Affine: ImageAugmentationAffine = None


image_mode_config = {
    AugmentationMode.light.value: {
        "Fliplr": {"p": 0.5},
        "Crop": {"px": (1, 16)},
    },
    AugmentationMode.medium.value: {
        "Fliplr": {"p": 0.5},
        "Flipud": {"p": 0.5},
        "Crop": {"px": (1, 16)},
        "LinearContrast": {"alpha": (0.75, 1.5)},
        "AdditiveGaussianNoise": {"loc": 0, "scale": (0.0, 0.05 * 255), "per_channel": 0.5}
    },
    AugmentationMode.maximum.value: {
        "Fliplr": {"p": 0.5},
        "Flipud": {"p": 0.5},
        "Crop": {"px": (1, 16)},
        "LinearContrast": {"alpha": (0.75, 1.5)},
        "Multiply": {"mul": (0.8, 1.2), "per_channel": 0.2},
        "AdditiveGaussianNoise": {"loc": 0, "scale": (0.0, 0.05 * 255), "per_channel": 0.5},
        "Affine": {
            "scale": {"x": (0.8, 1.2), "y": (0.8, 1.2)},
            "translate_percent": {"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
            "rotate": (-25, 25),
            "shear": (-8, 8)
        }
    }
}
