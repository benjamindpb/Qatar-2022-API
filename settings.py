WDQS_ENDPOINT = 'https://query.wikidata.org/sparql'
WD_API_ENNPOINT = 'https://www.wikidata.org/w/api.php'

SPARQL_QUERY = """
SELECT ?item ?label ?image
WHERE 
{{
    # Items que son instancias o subclases de un tipo
    ?item wdt:P31/wdt:P279* wd:{}.
    ?item wdt:P18 ?image . # imagen/es
    ?item rdfs:label ?label . # etiqueta de la entidad
    FILTER(LANG(?label)='en') 
}}
"""