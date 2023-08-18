from enum import Enum
from typing import Optional, List, Tuple, Dict, Any

from pydantic import BaseModel, validator
from pydantic.types import PositiveInt, PositiveFloat

from terra_ai_datasets.creation.validators import augmentation_params
from terra_ai_datasets.creation.validators.augmentation_params import AugmentationMode


class BaseAugmentation(BaseModel):
    augmentation_coef: PositiveFloat = 0.0

    # @validator("augmentation_coef")
    # def apply_coef_range(cls, v):
    #     if not 0.0 < v:
    #         raise ValueError('Ensure "augmentation_coef" is positive')
    #     return v

    class Config:
        use_enum_values = True


class AugmentationTypes(str, Enum):
    image = "Image"


# --- Image validators ---
class ImageScalers(str, Enum):
    none = None
    min_max_scaler = "MinMaxScaler"
    terra_image_scaler = "TerraImageScaler"


class ImageNetworkTypes(str, Enum):
    linear = "Linear"
    convolutional = "Convolutional"


class ImageProcessTypes(str, Enum):
    stretch = "Stretch"
    fit = "Fit"
    cut = "Cut"


class AugmentationData(BaseAugmentation):
    aug_type: AugmentationTypes
    mode: AugmentationMode
    parameters: Any = None

    @validator("parameters", always=True)
    def validate_date(cls, value, values):
        if values.get("mode"):
            return getattr(augmentation_params, f"{values.get('aug_type')}AugmentationParameters")(
                **getattr(augmentation_params, f"{values.get('aug_type').lower()}_mode_config")[values["mode"]]
            )


class ImageValidator(BaseModel):
    height: PositiveInt
    width: PositiveInt
    network: ImageNetworkTypes = ImageNetworkTypes.convolutional
    process: ImageProcessTypes = ImageProcessTypes.stretch
    preprocessing: ImageScalers = ImageScalers.none
    augmentation: Optional[AugmentationMode] = None


# --- Text validators ---
class TextModeTypes(str, Enum):
    full = "Full"
    length_and_step = "Length and step"


class TextProcessTypes(str, Enum):
    none = "None"
    embedding = "Embedding"
    bag_of_words = "Bag of words"
    word_to_vec = "Word2Vec"


class TextValidator(BaseModel):
    filters: str = '–—!"#$%&()*+,-./:;<=>?@[\\]^«»№_`{|}~\t\n\xa0–\ufeff'
    preprocessing: TextProcessTypes
    max_words_count: Optional[PositiveInt] = None
    word2vec_size: Optional[PositiveInt] = None
    mode: TextModeTypes
    pymorphy: bool
    max_words: Optional[PositiveInt] = None
    length: Optional[PositiveInt] = None
    step: Optional[PositiveInt] = None

    @validator("mode")
    def _validate_mode(cls, value):
        if value == TextModeTypes.full:
            cls.__fields__["max_words"].required = True
            cls.__fields__["length"].required = False
            cls.__fields__["step"].required = False
        elif value == TextModeTypes.length_and_step:
            cls.__fields__["max_words"].required = False
            cls.__fields__["length"].required = True
            cls.__fields__["step"].required = True
        return value

    @validator("preprocessing")
    def _validate_preprocessing(cls, value):
        if value == TextProcessTypes.word_to_vec:
            cls.__fields__["max_words_count"].required = False
            cls.__fields__["word2vec_size"].required = True
        else:
            cls.__fields__["max_words_count"].required = True
            cls.__fields__["word2vec_size"].required = False
        return value


# --- Audio validators ---
class AudioScalers(str, Enum):
    none = None
    min_max_scaler = "MinMaxScaler"
    standard_scaler = "StandardScaler"


class AudioParameterTypes(str, Enum):
    audio_signal = "Audio signal"
    chroma_stft = "Chroma stft"
    mfcc = "MFCC"
    rms = "RMS"
    spectral_centroid = "Spectral centroid"
    spectral_bandwidth = "Spectral bandwidth"
    spectral_rolloff = "Spectral rolloff"
    zero_crossing_rate = "Zero crossing rate"


class AudioResampleTypes(str, Enum):
    kaiser_best = "Kaiser best"
    kaiser_fast = "Kaiser fast"
    scipy = "Scipy"


class AudioFillTypes(str, Enum):
    last_millisecond = "Last millisecond"
    loop = "Loop"


class AudioModeTypes(str, Enum):
    full = "Full"
    length_and_step = "Length and step"


class AudioValidator(BaseModel):
    sample_rate: PositiveInt
    mode: AudioModeTypes
    parameter: List[AudioParameterTypes]
    fill_mode: AudioFillTypes
    resample: AudioResampleTypes
    preprocessing: AudioScalers
    max_seconds: Optional[PositiveFloat] = None
    length: Optional[PositiveFloat] = None
    step: Optional[PositiveFloat] = None

    @validator("mode")
    def _validate_mode(cls, value: AudioModeTypes) -> AudioModeTypes:
        if value == AudioModeTypes.full:
            cls.__fields__["max_seconds"].required = True
            cls.__fields__["length"].required = False
            cls.__fields__["step"].required = False
        elif value == AudioModeTypes.length_and_step:
            cls.__fields__["max_seconds"].required = False
            cls.__fields__["length"].required = True
            cls.__fields__["step"].required = True
        return value


# --- Dataframe validators ---
class CategoricalValidator(BaseModel):
    one_hot_encoding: bool
    classes_names: Optional[List[str]] = None


class RawValidator(BaseModel):
    pass


# --- Timeseries validators ---
class TimeseriesScalers(str, Enum):
    none = None
    min_max_scaler = "MinMaxScaler"
    standard_scaler = "StandardScaler"


class TimeseriesValidator(BaseModel):
    length: PositiveInt
    step: PositiveInt
    preprocessing: TimeseriesScalers
