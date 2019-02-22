from flask import Flask, render_template, request
from pathlib import Path
import io
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./secrets/ccpk.json"
'''
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    './static/SkullD.png')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)
'''
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

    #return "<img src='./static/uploads/{}' alt=\"y tho\">".format(filename)
    return render_template("itworked.html", imsrc="/static/uploads/{}".format(filename))

if __name__ == "__main__":
    app.run()