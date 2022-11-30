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
def get_uid(search): # función auxiliar
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

@app.route('/qatar2022/stadiums')
def stadiums():
    response = requests.get(
        WDQS_ENDPOINT, 
        params={
            'format': 'json',
            'query': STADIUMS_QUERY
        }
    )
    results = response.json()['results']['bindings']
    R = {}
    for r in results:
        qid = r['stadium']['value'].split('Q')[1]
        R[qid] = {
            'label': r['label']['value'],
            'uri': r['stadium']['value'],
            'image': r['image']['value'] if 'image' in r else 'undefined',
            'opening': r['opening']['value'] if 'opening' in r else 'undefined',
            'occupant': r['occupantLabel']['value'] if 'occupantLabel' in r else 'undefined',
            'capacity': r['cap']['value'],
            'coords': r['coords']['value'],
        }
    return R

@app.route('/qatar2022/group/<g>')
def groups_info(g: str):
    if g not in GROUPS_CONSTANT:
        return {
            'status': "ERROR",
            'msg': f'{g} is not a World Cup group. Try again with: A, B, C, D, E, F, G, H or I.'
        }
    qid = get_uid(f'2022 FIFA World Cup Group {g}')['results']['id']
    response = requests.get(
        WDQS_ENDPOINT,
        params={
            'format': 'json',
            'query': GROUPS_QUERY.format(qid)
        }
    )
    res_json = response.json()['results']['bindings']
    D = {}
    for r in res_json:
        D[r['countryLabel']['value']] = {
            'captain': r['captainLabel']['value'] if 'captainLabel' in r else 'undefined',
            'coach': r['coachLabel']['value'] if 'coachLabel' in r else 'undefined',
            'flag': r['flag']['value'],
            'uri': r['team']['value']
        }
    return {
        'group': g,
        'members': D
    }

@app.route('/qatar2022/group/<g>/results')
def groups_results(g: str):
    if g not in GROUPS_CONSTANT:
        return {
            'status': "ERROR",
            'msg': f'{g} is not a World Cup group. Try again with: A, B, C, D, E, F, G, H or I.'
        }
    qid = get_uid(f'2022 FIFA World Cup Group {g}')['results']['id']
    response = requests.get(
        WDQS_ENDPOINT,
        params={
            'format': 'json',
            'query': GR_MATCHES_QUERY.format(qid)
        }
    )
    res_json = response.json()['results']['bindings']
    D = {'group': g}
    results = {}
    for r in res_json:
        match_uri = r['match']['value'].split('Q')[1]
        if match_uri in results:
            results[match_uri] |= {
                r['teamLabel']['value']: r['goals']['value']
            }
        else:
            results[match_uri] = {
                r['teamLabel']['value']: r['goals']['value'],
                'location': r['locationLabel']['value'],
                'uri': r['match']['value']
                # 'winner': r['winnerLabel']['value'] if 'winnerLabel' in r else 'No winner,draw'
            }
    D['results'] = results
    return D

@app.route('/qatar2022/groups')
def groups():
    L = []
    for gl in GROUPS_CONSTANT:
        d = groups_info(gl)
        L.append(d)
    return {
        'groups': L
    }

@app.route('/qatar2022/participants')
def participants():
    response = requests.get(
        WDQS_ENDPOINT,
        params={
            'format': 'json',
            'query': PARTICIPANTS_QUERY
        }
    )
    res_json = response.json()
    results = res_json['results']['bindings']
    L = []
    for r in results:
        team_label = r['teamLabel']['value'].split(' at ')[0]
        print(team_label)
        L.append(team_label)
    return {
        'participants': L,
        'numberOfParticipants': 32,
        'missing': 32-len(L)
    }

if __name__ == '__main__':
    app.run(debug=True)
