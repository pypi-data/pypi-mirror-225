import imgaug.augmenters as iaa

from terra_ai_datasets.creation.validators.inputs import AugmentationData


def create_image_augmentation(image_augmentation_data: AugmentationData):
    parameters = []
    for key, value in image_augmentation_data.parameters.dict().items():
        if value:
            parameters.append(getattr(iaa, key)(**value))
    seq = iaa.Sequential(parameters, random_order=True)
    return seq
