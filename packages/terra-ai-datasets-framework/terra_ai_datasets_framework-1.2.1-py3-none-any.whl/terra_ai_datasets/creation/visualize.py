import random

from IPython.display import Audio, display
import matplotlib.pyplot as plt
import numpy as np
from imgaug import SegmentationMapsOnImage

from terra_ai_datasets.creation.augmentation import create_image_augmentation
from terra_ai_datasets.creation.utils import create_put_array, preprocess_put_array


def visualize_image_classification(dataframe, put_instructions, preprocessing, augmentation):

    x_data = dataframe.loc[:, "1_Image"].tolist()
    y_data = dataframe.loc[:, "2_Classification"].tolist()

    x_instructions = put_instructions[1]['1_Image']
    y_instructions = put_instructions[2]['2_Classification']

    classes_names = y_instructions.parameters.classes_names

    img_aug = augmentation.get("1_Image")

    fig, ax = plt.subplots(1, len(classes_names), figsize=(3 * len(classes_names), 5))
    for i, cls_name in enumerate(classes_names):
        sample_idx = random.choice([idx for idx, cl_n in enumerate(y_data) if cl_n == cls_name])
        x_sample = x_data[sample_idx]
        y_sample = y_data[sample_idx]

        x_array = create_put_array(x_sample, x_instructions)
        y_array = create_put_array(y_sample, y_instructions)

        if img_aug and "augm" in x_sample:
            x_array = img_aug(image=x_array)

        if preprocessing.get("1_Image"):
            x_array = preprocess_put_array(
                x_array, x_instructions, preprocessing["1_Image"]
            )

        ax[i].imshow(x_array)
        ax[i].set_title(f"{cls_name} - {str(y_array)}")

    plt.show()


def visualize_image_segmentation(dataframe, put_instructions, preprocessing, augmentation):

    sample_idx = random.randint(0, len(dataframe) - 1)

    img_aug = augmentation.get("1_Image")

    x_sample = str(dataframe.loc[sample_idx, "1_Image"])
    y_sample = str(dataframe.loc[sample_idx, "2_Segmentation"])

    x_instructions = put_instructions[1]['1_Image']
    y_instructions = put_instructions[2]['2_Segmentation']

    x_array = create_put_array(x_sample, x_instructions)
    y_array = create_put_array(y_sample, y_instructions)

    if img_aug and "augm" in x_sample:
        y_maps = SegmentationMapsOnImage(y_array, shape=y_array.shape)
        x_array, y_array = img_aug(image=x_array, segmentation_maps=y_maps)
        y_array = y_array.arr

    if preprocessing.get("1_Image"):
        x_array = preprocess_put_array(
            x_array, x_instructions, preprocessing["1_Image"]
        )

    num_classes = len(y_instructions.parameters.classes.items())
    fig, ax = plt.subplots(1, num_classes+1, figsize=(5*num_classes+1, 5))
    ax[0].imshow(x_array)
    ax[0].set_title(f"Вход")

    for i, (class_name, color) in enumerate(y_instructions.parameters.classes.items()):
        ax[i + 1].imshow(y_array[:, :, i])
        ax[i + 1].set_title(f"{class_name} - {str(color.as_rgb())}")

    plt.show()


def visualize_timeseries_depth(dataframe, put_instructions, preprocessing, **kwargs):

    plt.figure(figsize=(15, 5))
    sample_idx = None
    for col_name, col_data in put_instructions[1].items():
        x_instructions = put_instructions[1][col_name]
        if sample_idx is None:
            sample_idx = random.randint(0, len(dataframe) // x_instructions.parameters.length - 10)
        x_data = dataframe.loc[:, col_name][sample_idx*x_instructions.parameters.length: sample_idx*x_instructions.parameters.length + x_instructions.parameters.length + 1].tolist()
        x_array = create_put_array(x_data, x_instructions)
        if preprocessing.get(col_name):
            x_array = preprocess_put_array(
                x_array, x_instructions, preprocessing[col_name]
            )
        plt.plot(x_array.flatten(), label=f"{col_name} (inp)")

    for col_name, col_data in put_instructions[2].items():
        y_instructions = put_instructions[2][col_name]
        y_data = dataframe.loc[:, col_name][sample_idx*y_instructions.parameters.length + y_instructions.parameters.length: sample_idx*y_instructions.parameters.length + y_instructions.parameters.length + y_instructions.parameters.depth].tolist()
        y_array = create_put_array(y_data, y_instructions)
        if preprocessing.get(col_name):
            y_array = preprocess_put_array(
                y_array, y_instructions, preprocessing[col_name]
            )
        plt.plot([None for _ in range(col_data.parameters.length)] + y_array[:, 0].tolist(), label=f"{col_name} (out)")
        plt.axvline(x=y_instructions.parameters.length, color='r', linestyle="--", linewidth=2)

    plt.grid(True, alpha=0.3)
    plt.legend()


def visualize_timeseries_trend(dataframe, put_instructions, preprocessing, **kwargs):

    plt.figure(figsize=(15, 5))
    sample_idx = None
    for col_name, col_data in put_instructions[1].items():
        x_instructions = put_instructions[1][col_name]

        if sample_idx is None:
            sample_idx = random.randint(0, len(dataframe) // x_instructions.parameters.length - 10)
        x_data = dataframe.loc[:, col_name][sample_idx*x_instructions.parameters.length: sample_idx*x_instructions.parameters.length + x_instructions.parameters.length].tolist()
        x_array = create_put_array(x_data, x_instructions)
        if preprocessing.get(col_name):
            x_array = preprocess_put_array(
                x_array, x_instructions, preprocessing[col_name]
            )
        plt.plot(x_array.flatten(), label=f"{col_name} (inp)")

    for col_name, col_data in put_instructions[2].items():
        y_instructions = put_instructions[2][col_name]
        y_data = dataframe.loc[:, col_name][sample_idx*y_instructions.parameters.length + y_instructions.parameters.length - 1: sample_idx*y_instructions.parameters.length + y_instructions.parameters.length + 1].tolist()
        y_array = create_put_array(y_data, y_instructions)
        if y_instructions.parameters.one_hot_encoding:
            y_array = np.argmax(y_array)
        if y_array == 1:
            color = "green"
        elif y_array == 2:
            color = "red"
        else:
            color = "cyan"
        start_idx, stop_idx = y_data
        plt.plot([None for _ in range(y_instructions.parameters.length)] + [stop_idx], marker="o", markersize=2,
                 markeredgecolor=color, markerfacecolor=color)
        plt.arrow(y_instructions.parameters.length - 1, start_idx, 1, stop_idx - start_idx, width=0.2, color=color)
        plt.grid(alpha=0.3)
        plt.legend()
        plt.show()


def visualize_text_classification(dataframe, put_instructions, **kwargs):

    x_data = dataframe.loc[:, "1_Text"].tolist()
    y_data = dataframe.loc[:, "2_Classification"].tolist()

    classes_names = put_instructions[2]['2_Classification'].parameters.classes_names

    for i, cls_name in enumerate(classes_names):
        sample_idx = random.choice([idx for idx, cl_n in enumerate(y_data) if cl_n == cls_name])
        x_sample = x_data[sample_idx]
        y_sample = y_data[sample_idx]

        print(f"Класс: \033[1m{y_sample}\033[0m")
        display(x_sample)
        if i + 1 != len(classes_names):
            print()


def visualize_audio_classification(dataframe, put_instructions, **kwargs):

    cls_idx = len(dataframe.columns.tolist())
    x_data = dataframe.loc[:, "1_Audio"].tolist()
    y_data = dataframe.loc[:, f"{cls_idx}_Classification"].tolist()

    x_instructions = put_instructions[1]['1_Audio']
    y_instructions = put_instructions[cls_idx][f'{cls_idx}_Classification']

    sample_rate = x_instructions.parameters.sample_rate
    classes_names = y_instructions.parameters.classes_names

    for i, cls_name in enumerate(classes_names):
        sample_idx = random.choice([idx for idx, cl_n in enumerate(y_data) if cl_n == cls_name])
        x_sample = x_data[sample_idx]
        y_sample = y_data[sample_idx]

        x_array = create_put_array(x_sample, x_instructions)

        file_path, rng = x_sample.split(';')

        print(f"Класс: \033[1m{y_sample}\033[0m\nФайл: {file_path}\nОтрезок: {rng}")
        display(Audio(data=x_array, rate=sample_rate))
        if i + 1 != len(classes_names):
            print()


def visualize_dataframe_classification(dataframe, put_instructions, preprocessing):
    pass


def visualize_dataframe_regression(dataframe, put_instructions, preprocessing):
    pass
