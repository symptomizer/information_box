from flask import Flask, jsonify, request
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from flask_cors import CORS
import wptools
import re
import json

cleanr = re.compile('\[[^\]]*\||\[\[|\]\]')
# removing_pipes = re.compile('\[[^\]]*\||')

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

with open('fields.txt') as f:
    fields_list = [x.rstrip() for x in f] # remove line breaks


def clean_info_string(string):
    cleantext = re.sub(cleanr, '', string)
    # cleantext = re.sub(removing_pipes, ' ', cleantext)
    if("{{" in cleantext):
        return ""
    return cleantext


def process_info_box(infobox):
    returned_infobox = {}
    for key in infobox.keys():
        if key in fields_list:
            clean_text = clean_info_string(infobox[key])
            if (len(clean_text) > 0):
                returned_infobox[key] = clean_text 
    return returned_infobox

def responsify(data, status, error):
    return {'data': data, 'status': status, 'error': error}

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/info')
def info():
    try:
        title = request.args.get('search')
        page = wptools.page(title)
        page.get_query()
        return_obj = {}
        extext = ""
        aliases = []
        images = page.images(['url'])
        if 'extext' in page.data:
            extext = page.data['extext']
        if 'aliases' in page.data:
            aliases = page.data['aliases']
        return_obj['images'] = [img['url'] for img in images]
        return_obj['extext'] = extext
        return_obj['aliases'] = aliases
        wikidata = wptools.page(title).get_parse()
        infobox = wikidata.data['infobox']
        return_obj['infobox'] = process_info_box(infobox)
        return jsonify(responsify(return_obj, 200, ""))
    except Exception as e:
        print("Incorrect")
        return jsonify(responsify({}, 400, str(e)))
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8889)