# Importing Necessary packages
from flask import Flask,render_template, request, jsonify
import numpy as np
from fastai.basics import *
from fastai.vision import *
from fastai.vision.all import *
import PIL
import pickle 
import io
import os

# setting working dir
cwd = os.getcwd()
path= cwd + '/model'

# Initialiazing flask app
app = Flask(__name__)

# Loading  saved model
model = load_learner(path + '/snakes_learner_export.pkl')

snakes = [
        { 'common_name':  'Banded Rock Rattlesnake', 'species': 'Crotalus lepidus klauberi', 'venomous': 'V' },
        { 'common_name':  'Blacktail Rattlesnake', 'species': 'Crotalus molossus', 'venomous': 'V' },
        { 'common_name':  'Blind Snake', 'species': 'Leptotyphlops dulcis', 'venomous': 'NV' },
        { 'common_name':  'Broadband Copperhead', 'species': 'Agkistrodon contortrix laticinctus', 'venomous': 'V' },
        { 'common_name':  'Bull Snake', 'species': 'Pituophis catenifer', 'venomous': 'NV' },
        { 'common_name':  'Buttermilk Racer', 'species': 'Clouber constrictor anthicus', 'venomous': 'NV' },
        { 'common_name':  'DeKays Brown Snake', 'species': 'Storeria dekayi', 'venomous': 'NV' },
        { 'common_name':  'Desert Massasauga Rattlesnake', 'species': 'Sistrurus catenatus edwardsii', 'venomous': 'V' },
        { 'common_name':  'Diamond-Backed Water Snake', 'species': 'Nerodia rhombifer', 'venomous': 'NV' },
        { 'common_name':  'Eastern Copperhead', 'species': 'Agkistrodon contortrix', 'venomous': 'V' },
        { 'common_name':  'Lined Snake', 'species': 'Tropidoclonion lineatum', 'venomous': 'NV' },
        { 'common_name':  'Milk Snake', 'species': 'Lampropeltis triangulum', 'venomous': 'NV' },
        { 'common_name':  'Mojave Rattlesnake', 'species': 'Crotalus scutulatus', 'venomous': 'V' } ,
        { 'common_name':  'Mottled Rattlesnake', 'species': 'Crotalus lepidus', 'venomous': 'V' },
        { 'common_name':  'Plain-Bellied Water Snake', 'species': 'Nerodia erythrogaster', 'venomous': 'NV' },
        { 'common_name':  'Prairie Kingsnake', 'species': 'Lampropeltis calligaster', 'venomous': 'NV' },
        { 'common_name':  'Prairie Rattlesnake', 'species': 'Crotalus viridis', 'venomous': 'V' },
        { 'common_name':  'Pygmy Rattlesnake', 'species': 'Sistrurus miliarius', 'venomous': 'V' },
        { 'common_name':  'Ring-Necked Snake', 'species': 'Diadophis punctatus', 'venomous': 'NV' },
        { 'common_name':  'Rough Earth Snake', 'species': 'Virginia striatula', 'venomous': 'NV' },
        { 'common_name':  'Rough Green Snake', 'species': 'Opheodrys aestivus', 'venomous': 'NV' },
        { 'common_name':  'Speckled Kingsnake', 'species': 'Ampropeltis getula holbrooki', 'venomous': 'NV' },
        { 'common_name':  'Texas Coral Snake', 'species': 'Micrurus tener', 'venomous': 'V' },
        { 'common_name':  'Texas Garter Snake', 'species': 'Thamnophis sirtalis annectens', 'venomous': 'NV' },
        { 'common_name':  'Texas Indigo', 'species': 'Drymarchon melanurus erebennus', 'venomous': 'NV' },
        { 'common_name':  'Timber Rattlesnake', 'species': 'Crotalus horridus', 'venomous': 'V' },
        { 'common_name':  'Water Moccasin', 'species': 'Agkistrodon piscivorous', 'venomous': 'V' },
        { 'common_name':  'Western Coachwhip' , 'species': 'Masticophis flagellum testaceus', 'venomous': 'NV' },
        { 'common_name':  'Western Diamondback Rattlesnake', 'species': 'Crotalus Atrox', 'venomous': 'V' } ,
        { 'common_name':  'Western Hognose Snake', 'species': 'Heterodon nasicus', 'venomous': 'NV' },
        { 'common_name':  'Western Massasauga Rattlesnake', 'species': 'Sistrurus catenatus', 'venomous': 'V' },
        { 'common_name':  'Western Rat Snake', 'species': 'Pantherophis obsoletus', 'venomous': 'NV' },
        { 'common_name':  'Yellow-Bellied Racer', 'species': 'Coluber constrictor flaviventris', 'venomous': 'NV' },
]

# Rendering index.html at /
@app.route('/')
def index():
    return render_template('index.html')

# Getting data with POST Method
@app.route('/upload', methods=["POST"])
def upload():
    # try:
        # Getting img from POST
        file = request.files['user-img'].read()
        # Resizing img to 224 X 224 , This is the size on which model was trained
        img = PILImage.create(io.BytesIO(file))

        # Prediction using model
        pred_class,pred_idx,probabilities = model.predict(img)

        # Getting Prediction ready to sent it to frontend
        i = int(pred_idx)

        prediction = "<table>"
        if snakes[i]['venomous'] == "V":
            prediction += "<tr style='background-color: red'>"
        else:
            prediction += "<tr style='background-color: green'>"

        prediction += "<th>%s</th><th>%s</th><th>%s</th><th>%.3f</th><th><a target='_blank' href='https://www.wikipedia.org/search-redirect.php?family=Wikipedia&language=en&search=%s&language=en&go=Go'>Wikipedia</th>" % (
            snakes[i]['common_name'],
            snakes[i]['species'],
            snakes[i]['venomous'],
            float(probabilities[i]),
            snakes[i]['species'].replace(' ', '+')
        )
        prediction += "</tr>"
        for k in range(len(probabilities)):
            if probabilities[k] > 0.25 and k != i:
                if snakes[k]['venomous'] == "V":
                    prediction += "<tr style='background-color: red'>"
                else:
                    prediction += "<tr style='background-color: green'>"

                prediction += "<td>%s</td><td>%s</td><td>%s</td><td>%.3f</td><td><a target='_blank' href='https://www.wikipedia.org/search-redirect.php?family=Wikipedia&language=en&search=%s&language=en&go=Go'>Wikipedia</td>" % (
                    snakes[k]['common_name'],
                    snakes[k]['species'],
                    snakes[k]['venomous'],
                    float(probabilities[k]),
                    snakes[k]['species'].replace(' ', '+')
                )
                prediction += "</tr>"

        prediction += "</table>"
        response = {"result": prediction}
        return jsonify(response)

#running app at localhost on port 8080
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)    
