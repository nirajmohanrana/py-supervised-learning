# data_collection.py
import os
import PySimpleGUI as sg
from PIL import Image
import io


def collect_data():
    image_dir = "images"
    data = []

    sg.theme("DefaultNoMoreNagging")

    # Supported image file extensions
    supported_extensions = (".jpg", ".jpeg", ".png")

    # Dropdown menu options
    label_options = ["bike", "car", "ganpati", "spider-man"]

    # Get a list of image files sorted by date in descending order
    image_files = sorted(
        [filename for filename in os.listdir(image_dir) if os.path.splitext(filename)[
            1].lower() in supported_extensions],
        key=lambda x: os.path.getmtime(os.path.join(image_dir, x)),
        reverse=True
    )

    for filename in image_files:
        image_path = os.path.join(image_dir, filename)
        image = Image.open(image_path)
        image.thumbnail((400, 300))

        # Convert the image to bytes for PySimpleGUI
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        image_bytes = bio.getvalue()

        layout = [
            [sg.Image(data=image_bytes)],
            [sg.Button("Previous"), sg.Button("Next"),
             sg.Button("Submit"), sg.Button("Exit")],
            [sg.Text("Select Label:"), sg.DropDown(label_options,
                                                   default_value="bike", key="label_dropdown")]
        ]

        window = sg.Window("Image Labeling", layout, finalize=True)

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == "Exit":
                window.close()
                return  # Close the application when the Exit button or window is closed
            elif event == "Previous":
                break
            elif event == "Next":
                break
            elif event == "Submit":
                label = values["label_dropdown"]
                data.append({"filename": filename, "label": label})
                break

        window.close()

    # Save the collected data to a file
    with open("data.csv", "w") as f:
        for item in data:
            f.write(f"{item['filename']},{item['label']}\n")


if __name__ == "__main__":
    collect_data()
