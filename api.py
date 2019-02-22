from flask import Flask, render_template
from pathlib import Path
import io
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./secrets/ccpk.json"

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

app = Flask(__name__)

skull = "./static/SkullD.png"
try:
    Path(Path.cwd().joinpath("new")).mkdir(parents=True, exist_ok=True)
    print('yay')
except:
    print('damn')

print(skull)
@app.route("/")
def hello():
    return render_template('index.html', title="TESTING", image_f=skull)

if __name__ == "__main__":
    app.run()