from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from requests.auth import HTTPBasicAuth

import random
from dotenv import load_dotenv
import os

"""
to run go to 
pwd
/Users/ethanharrington/Documents/coding_practice/python/portfolio_backend
then source venv/bin/activate
then when you do flask run go to:
http://127.0.0.1:5000/get-genre
to get a random genre of music
"""
load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route('/get-genre', methods=['GET'])
def get_genre():
    api_endpoint = "https://binaryjazz.us/wp-json/genrenator/v1/genre/"
    response = requests.get(api_endpoint)
    
    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code


@app.route('/get-random-plant', methods=['GET'])
def get_random_plant():
    api_key = 'sk-tNg6654a89a4bda6b2865'  # Replace with your actual API key
    api_endpoint = f"https://perenual.com/api/species-list?key={api_key}"

    try:
        response = requests.get(api_endpoint)
        response.raise_for_status()

        plants = response.json()['data']
        if not plants:
            return jsonify({"error": "No plants found"}), 404

        # Select a random plant
        random_plant = random.choice(plants)

        # Simplify the data of the random plant
        simplified_plant = {
            'common_name': random_plant.get('common_name', 'N/A'),
            'scientific_name': random_plant.get('scientific_name', ['N/A'])[0],
            'sunlight': random_plant.get('sunlight', ['N/A']),
            'watering': random_plant.get('watering', 'N/A')
        }

        return jsonify(simplified_plant)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)

