# image_classifier.py
import os
import csv
import cv2
import numpy as np
import PySimpleGUI as sg
import io
from PIL import Image


def load_data(data_file):
    images = []
    labels = []
    label_mapping = {}
    current_label = 0
    with open(data_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            filename, label = row
            if label not in label_mapping:
                label_mapping[label] = current_label
                current_label += 1
            image = cv2.imread(os.path.join(
                "images", filename), cv2.IMREAD_GRAYSCALE)
            if image is not None:
                # Resize the image to a fixed size
                image = cv2.resize(image, (100, 75))
                images.append(image)
                labels.append(label_mapping[label])
    return np.array(images), np.array(labels), label_mapping


def train_classifier(images, labels):
    knn = cv2.ml.KNearest_create()
    knn.train(images, cv2.ml.ROW_SAMPLE, labels)
    return knn


def main():
    data_file = "data.csv"
    images, labels, label_mapping = load_data(data_file)
    classifier = train_classifier(images.reshape(
        len(images), -1).astype(np.float32), labels.astype(np.float32))

    sg.theme("DefaultNoMoreNagging")

    layout = [
        [sg.Text("Select an image:")],
        [sg.Input(size=(50, 1), key="image_path"), sg.FileBrowse()],
        [sg.Button("Classify"), sg.Button("Exit")],
        [sg.Image(key="image_display")],
        [sg.Text("Predicted Label: "), sg.Text("", key="prediction")]
    ]

    window = sg.Window("Image Classifier", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Classify":
            image_path = values["image_path"]
            if image_path:
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if image is not None:
                    image = cv2.resize(image, (100, 75))
                    _, result, _, _ = classifier.findNearest(
                        image.reshape(1, -1).astype(np.float32), k=1)
                    predicted_label_id = int(result[0, 0])
                    predicted_label = list(label_mapping.keys())[list(
                        label_mapping.values()).index(predicted_label_id)]
                    window["prediction"].update(predicted_label)

            # Display the selected image
            if image_path:
                image = cv2.imread(image_path)
                image = cv2.resize(image, (400, 300))
                bio = io.BytesIO()
                # Convert BGR to RGB
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image_pil = Image.fromarray(image)
                image_pil.save(bio, format="PNG")
                window["image_display"].update(data=bio.getvalue())

    window.close()


if __name__ == "__main__":
    main()
