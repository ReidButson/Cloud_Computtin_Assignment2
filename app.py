from flask import Flask, render_template, request
from pathlib import Path
import io
import os
import itunes
from mailjet_rest import Client
import wikipedia
import pyrebase
import requests

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./secrets/ccpk.json"

config = {
    "apiKey": "AIzaSyBRPX7V7XORhX7oip-mcbJLMzyUfyA-ciQ",
    "authDomain": "level-abode-232421.firebaseapp.com",
    "databaseURL": "https://level-abode-232421.firebaseio.com",
    "projectId": "level-abode-232421",
    "storageBucket": "level-abode-232421.appspot.com",
    "messagingSenderId": "461402881664"
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

app = Flask(__name__)

skull = "./static/SkullD.png"

print(skull)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_image", methods = ['POST'])
def upload_image():
    Path(Path.cwd().joinpath("static", "uploads")).mkdir(parents=True, exist_ok=True)

    file = request.files["file"]
    filename = file.filename
    destination = Path.cwd().joinpath("static", "uploads", filename)
    file.save(str(destination))
    storage.child("images/{}".format(filename)).put(str(destination))
    url = storage.child("images/{}".format(filename)).get_url(None)

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

    os.remove(str(destination))


    return render_template("itworked.html",
                           best_guess=best_guess.upper(),
                           imsrc=url,
                           results=results)

@app.route("/send_knowledge", methods = ['POST'])
def send_knowledge():
    subject = wikipedia.random(1)
    summary = wikipedia.summary(subject)
    email = request.form['email']
    name = request.form['name']
    body = "A brief summary of: {}\n{}".format(subject, summary)
    bodyhtml = "<div><h2>A brief summary of: {}</h2><br /><p>{}</p></div><br /><br /><p>Your friend {} thought you should know<p>".format(
        subject, summary, name)

    api = '1b3a86b86c9b6d15fd254f2e5edcfe09'
    secret = '6fa9ad8d7d8392adca139d7c587a6a3a'

    mailjet = Client(auth=(api, secret), version='v3.1')

    data = {
        'Messages': [
            {
                "From": {
                    "Email": "randominfoyounowknow@gmail.com",
                    "Name": "Random Info"
                },
                "To": [
                    {
                        "Email": email,
                        "Name": "you"
                    }
                ],
                "Subject": "A little info about: {}".format(subject),
                "TextPart": body,
                "HTMLPart": bodyhtml
            }
        ]
    }
    result = mailjet.send.create(data=data)
    status = result.status_code

    if status == 200:
        return render_template("knowledgesent.html",
                               subject=subject,
                               body=body)
    else:
        return render_template("error.html", status=status)

@app.route("/podcast", methods=['post'])
def podcast():
    podname = request.form['podname']

    episodes = itunes.podcasts(podname)
    return render_template("podcasts.html", episodes=episodes)

@app.route("/cat_facts", methods=['POST'])
def cat_facts():
    response = requests.get('https://cat-fact.herokuapp.com/facts/random?animal=cat&amount=1')
    json_response = response.json()
    fact= json_response['text']

    return render_template("catfact.html", fact=fact)

if __name__ == "__main__":
    app.run()