from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import urllib.request

app = Flask(__name__)

MODEL_PATH = "model/plant_disease_model.h5"
MODEL_URL = "PASTE_YOUR_HUGGINGFACE_MODEL_LINK_HERE"

# Create model folder if missing
if not os.path.exists("model"):
    os.makedirs("model")

# Download model if not present
if not os.path.exists(MODEL_PATH):
    print("Downloading model from Hugging Face...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Model downloaded successfully!")

# Load trained model
model = tf.keras.models.load_model(MODEL_PATH)

class_names = [
    "Pepper_bell_Bacterial_spot",
    "Pepper_bell_healthy",
    "Potato_Early_blight",
    "Potato_healthy",
    "Potato_Late_blight",
    "Tomato_Target_Spot",
    "Tomato_mosaic_virus",
    "Tomato_YellowLeaf_Curl_Virus",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_healthy",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites"
]

medicine_dict = {
    "Potato_Early_blight": "Use Mancozeb Fungicide",
    "Potato_Late_blight": "Use Copper Fungicide",
    "Tomato_Early_blight": "Use Chlorothalonil Spray",
    "Tomato_Late_blight": "Use Copper Oxychloride",
    "Tomato_Leaf_Mold": "Use Sulfur Fungicide",
    "Pepper_bell_Bacterial_spot": "Use Copper-based Bactericide"
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    medicine = ""

    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename != "":
            filepath = os.path.join("static", file.filename)
            file.save(filepath)

            img = image.load_img(filepath, target_size=(128, 128))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            prediction = model.predict(img_array)
            predicted_class = class_names[np.argmax(prediction)]

            result = predicted_class
            medicine = medicine_dict.get(
                predicted_class,
                "General plant care recommended"
            )

    return render_template(
        "index.html",
        result=result,
        medicine=medicine
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
