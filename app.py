from bs4 import BeautifulSoup
import requests
import re
from flask import Flask, request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def extractIngredients(soup):
    found = False
    try:
        tags = soup.find(text=re.compile('Ingredients')).parent
        lists = []
        while not found:
            if(tags.findAll('li')):
                found = True
                for tag in tags.findAll('li'):
                    lists.append(tag.text.strip())
            else:
                tags = tags.parent
        return lists
    except AttributeError:
        return ['Ingredients could not be found']

def extractDirections(soup):
    found = False
    try:
        tags = soup.find(text=re.compile('Directions')).parent
        lists = []
        while not found:
            if(tags.findAll('li')):
                found = True
                for tag in tags.findAll('li'):
                    lists.append(tag.text.strip())
            else:
                tags = tags.parent
        return lists
    except AttributeError:
        return ['Directions could not be found']

@app.route('/recipe', methods=['POST'])
def home():
    data = request.get_json()
    response = requests.get(data['url'])
    soup = BeautifulSoup(response.text, "html.parser")
    recipe =  {
        'ingeredients': extractIngredients(soup),
        'directions': extractDirections(soup)
    }
    return jsonify(recipe)

if __name__=="__main__":
    app.run()

