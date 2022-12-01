from flask import Flask
import requests
from settings import *

app = Flask(__name__)

WDQS_ENDPOINT = 'https://query.wikidata.org/sparql'
WD_API_ENNPOINT = 'https://www.wikidata.org/w/api.php'

@app.route('/')
def hello_world():
    return """
            <html>
            <head>
            <style>
                body {
                background-color: #A68A5C;
                }
                .header {
                    color:white;
                    text-align: center;
                    background: #C62347;
                }
                .consults{
                    color:white;
                    background: #DCC090;
                }
                .consults ul li {
                    color:white;
                    margin: 5px;
                }
            </style>
            </head>
            <body>
            <div class="header">
                <h1>Qatar 2022 API</h1>
                Este proyecto tiene por objetivo implementar una API para obtener 
                información sobre el mundial de fútbol de la FIFA de Qatar 2022
                usando el endpoint del servicio de consultas de Wikidata
            </div>
            <div class="consults">
                <h2>Consultas:</h2>
                <ul>
                    <li><a href=" http://localhost:5000/qatar2022/participants">Participantes</a></li>
                    <li><a href=" http://localhost:5000/qatar2022/stadiums">Estadios</a></li>
                    <li><a href=" http://localhost:5000/qatar2022/groups">Grupos(tarda un poco)</a></li>
                    <li>
                        Informacion de Grupos:
                        <a href=" http://localhost:5000/qatar2022/group/info/A">A</a>
                        <a href=" http://localhost:5000/qatar2022/group/info/B">B</a>
                        <a href=" http://localhost:5000/qatar2022/group/info/C">C</a>
                        <a href=" http://localhost:5000/qatar2022/group/info/D">D</a>
                        <a href=" http://localhost:5000/qatar2022/group/info/E">E</a>
                        <a href=" http://localhost:5000/qatar2022/group/info/F">F</a>
                        <a href=" http://localhost:5000/qatar2022/group/info/G">G</a>
                        <a href=" http://localhost:5000/qatar2022/group/info/H">H</a>
                    </li>
                    <li>
                        Resultados de Grupo:
                        <a href=" http://localhost:5000/qatar2022/group/results/A">A</a>
                        <a href=" http://localhost:5000/qatar2022/group/results/B">B</a>
                        <a href=" http://localhost:5000/qatar2022/group/results/C">C</a>
                        <a href=" http://localhost:5000/qatar2022/group/results/D">D</a>
                        <a href=" http://localhost:5000/qatar2022/group/results/E">E</a>
                        <a href=" http://localhost:5000/qatar2022/group/results/F">F</a>
                        <a href=" http://localhost:5000/qatar2022/group/results/G">G</a>
                        <a href=" http://localhost:5000/qatar2022/group/results/H">H</a>
                    </li>
                </ul>
            </div>
            </html>
            </body>
            """

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
    html ="""
        <html>
            <head>
                <style>
                body {
                background-color: #A68A5C;
                color: white;
                }
                .header {
                    color:white;
                    text-align: center;
                    background: #C62347;
                }
                .stadium{
                    color:white;
                    background: #DCC090;
                }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Estadios</h1>
                </div>
                <div class="stadium">
        """
    for stadium in R:
        html+=f"""
            <h2>Estadio:{R[stadium]["label"]}</h2>
            <p>Uri: {R[stadium]["uri"]}</p>
            <p>opening: {R[stadium]["opening"]}</p>
            <p>occupant: {R[stadium]["occupant"]}</p>
            <p>capacity: {R[stadium]["capacity"]}</p>
            <p>coords: {R[stadium]["coords"]}</p>
            <p>image: {R[stadium]["image"]}</p>
        """
        if R[stadium]["image"] != "undefined":
            html += f"""
            <img src="{R[stadium]["image"]}" width="200" height="200">
            """
    html+="""
            </div>
            <a href=" http://localhost:5000">Volver al inicio</a>
            </body>
        </html>
    """
    return html

@app.route('/qatar2022/group/info/<g>')
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

@app.route('/qatar2022/group/results/<g>/')
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
    html = """
        <html>
            <head>
                <style>
                body {
                background-color: #A68A5C;
                color: white;
                }
                .header {
                    color:white;
                    text-align: center;
                    background: #C62347;
                }
                .participants-list{
                    color:white;
                    background: #DCC090;
                }
                .participants-list ul li {
                    color:white;
                    margin: 5px;
                }
                </style>
            </head>
        """
    html +=f"""   
            <body>
            <div class="header">
                <h1>Participantes</h1>
                <h2>Numero de participantes: 32</h2>
                <h2>missing: {32-len(L)} </h2>
            </div>
            <div class="participants-list">
                <h2>Lista de participantes:</h2>
                <ul>
        """
    for team in L:
        html += f"<li>{team}</li>"    
    html +=   """
            </ul>
        </div>
        <a href=" http://localhost:5000">Volver al inicio</a>
        </body>
        </html>
        """
    return html

if __name__ == '__main__':
    app.run(debug=True)
