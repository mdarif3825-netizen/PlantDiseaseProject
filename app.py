from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Create static folder automatically if not present
if not os.path.exists("static"):
    os.makedirs("static")

# Temporary class names for demo deployment
class_names = [
    "Tomato Leaf",
    "Potato Leaf",
    "Pepper Leaf",
    "Healthy Plant",
    "Diseased Plant"
]

# Temporary medicine suggestions
medicine_dict = {
    "Tomato Leaf": "Use balanced fertilizer and check for fungal infection",
    "Potato Leaf": "Use Copper Fungicide for protection",
    "Pepper Leaf": "Use Copper-based Bactericide",
    "Healthy Plant": "No medicine needed, continue normal care",
    "Diseased Plant": "Inspect leaf and apply suitable fungicide"
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    medicine = ""
    filename = ""

    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename != "":
            filepath = os.path.join("static", file.filename)
            file.save(filepath)

            filename = file.filename

            # Temporary prediction logic for Render deployment
            # (TensorFlow will be connected later)
            result = "Diseased Plant"
            medicine = medicine_dict.get(result, "General plant care recommended")

        else:
            result = "No file uploaded"
            medicine = "Please upload a plant leaf image"

    return render_template(
        "index.html",
        result=result,
        medicine=medicine,
        filename=filename
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
