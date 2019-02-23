from flask import Flask, render_template, request
from pathlib import Path
import io
import os
import itunes

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./secrets/ccpk.json"

app = Flask(__name__)

skull = "./static/SkullD.png"

print(skull)
@app.route("/")
def index():
    return render_template("upload_image.html")

@app.route("/upload_image", methods = ['POST'])
def upload_image():
    Path(Path.cwd().joinpath("static", "uploads")).mkdir(parents=True, exist_ok=True)

    file = request.files.get("file")
    filename = file.filename
    destination = Path.cwd().joinpath("static", "uploads", filename)
    file.save(str(destination))



    # Instantiates a client
    client = vision.ImageAnnotatorClient()


    # Loads the image into memory
    with io.open(str(destination), 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.web_detection(image=image)
    annotations = response.web_detection

    best_guess = "Best Guess"
    if annotations.best_guess_labels:
        for guess in annotations.best_guess_labels:
            best_guess = guess.label


    results = []
    if annotations.web_entities:
        for entity in annotations.web_entities:
            top = itunes.top_result(entity.description)
            if top:
                top['tag'] = entity.description
                if top not in results:
                    results.append(top)

    relative_path = "/static/uploads/{}".format(filename)


    return render_template("itworked.html",
                           best_guess=best_guess.upper(),
                           imsrc=relative_path,
                           results=results)

if __name__ == "__main__":
    app.run()