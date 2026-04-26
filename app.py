from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Create static folder if not exists
if not os.path.exists("static"):
    os.makedirs("static")

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

            # Temporary prediction for deployment
            result = "Plant detected successfully"
            medicine = "AI prediction + medicine recommendation will be connected after deployment"

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
