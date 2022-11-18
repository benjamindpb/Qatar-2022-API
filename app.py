from flask import Flask
import requests
from settings import *

app = Flask(__name__)

WDQS_ENDPOINT = 'https://query.wikidata.org/sparql'
WD_API_ENNPOINT = 'https://www.wikidata.org/w/api.php'

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/id/<search>')
def get_entity_info(search): # función auxiliar
    """
    Dado el nombre de una propiedad P31 de Wikidata, esta función devuelve el 
    identificador unico (UID) de la entidad usando la API de Wikidata.

    Args:
        search (str): etiqueta de la entidad a buscar

    Returns:
        str: identificador único de una entidad de Wikidata.
            ej: si se busca "gato", esta función devuelve Q146.
            (https://www.wikidata.org/wiki/Q146)

    """
    res = requests.get(
        WD_API_ENNPOINT, 
        params={
            'action': 'wbsearchentities',
            'search': search, 
            'language': ['en'],
            'format': 'json'
    }).json()
    for entity in res['search']:
        if search == entity['match']['text']:
            return {
                'search': search,
                'results': entity,
                'status': 200
            }
    return {
        'search': search,
        'status': 500
    }

@app.route('/data/<search>')
def get_data(search: str):
    entity = get_entity_info(search)
    qid = entity["results"]["id"]
    """
    Esta función se enc
    """
    response = requests.get(
        WDQS_ENDPOINT, 
        params={
            'format': 'json',
            'query': SPARQL_QUERY.format(qid)}
    )
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
