from flask import Flask, jsonify, request
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from fast_autocomplete import AutoComplete
from flask_cors import CORS
import wptools
import pandas as pd



app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/info')
def info():
    title = request.args.get('search')
    page = wptools.page(title)
    page.get_query()
    return_obj = {}
    images = page.images(['url'])
    extext = page.data['extext']
    aliases = page.data['aliases']
    return_obj['images'] = [img['url'] for img in images]
    return_obj['extext'] = extext
    return_obj['aliases'] = aliases
    wikidata = wptools.page(title).get_parse()
    infobox = wikidata.data['infobox']
    return_obj['infobox'] = infobox

    return jsonify(return_obj)

if __name__ == '__main__':
    app.run(debug=True, port=8889)