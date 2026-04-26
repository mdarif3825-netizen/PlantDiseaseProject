from flask import Flask, render_template, request
import os

app = Flask(__name__)

if not os.path.exists("static"):
    os.makedirs("static")

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    medicine = ""

    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename != "":
            filepath = os.path.join("static", file.filename)
            file.save(filepath)

            # Demo prediction for deployment
            result = "Tomato Early Blight"
            medicine = "Use Chlorothalonil Spray"

        else:
            result = "No file uploaded"
            medicine = "Please upload a plant image"

    return render_template(
        "index.html",
        result=result,
        medicine=medicine
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
