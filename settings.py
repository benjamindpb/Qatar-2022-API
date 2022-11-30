WDQS_ENDPOINT = 'https://query.wikidata.org/sparql'
WD_API_ENNPOINT = 'https://www.wikidata.org/w/api.php'

GROUPS_CONSTANT = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

WCUPS = """
select distinct ?item ?label ?description ?countryLabel (year(?date) as ?year) ?mascotLabel
where {{
  ?item wdt:P3450 wd:Q19317 .
  ?item rdfs:label ?label .
  filter(lang(?label)='en') .
  ?item schema:description ?description .
  filter(lang(?description)='en') .
  ?item wdt:P17 ?country .
  ?country rdfs:label ?countryLabel .
  filter(lang(?countryLabel)='en') .
  ?item wdt:P585 ?date .
  filter(year(?date) <= 2022) .
  optional {{
    ?item wdt:P822 ?mascot .
    ?mascot rdfs:label ?mascotLabel .
    filter(lang(?mascotLabel)='en') .
  }}
}}
"""
STADIUMS_QUERY = """
select distinct ?stadium ?label ?image ?opening ?occupantLabel ?cap ?coords
where {{
  wd:Q284163 wdt:P276 ?stadium .
  ?stadium rdfs:label ?label .
  filter(lang(?label)='en') .
  optional {{?stadium wdt:P18 ?image .}}
  optional {{?stadium wdt:P1619 ?opening .}}
  optional {{
    ?stadium wdt:P466 ?occupant .
    ?occupant rdfs:label ?occupantLabel .
    filter(lang(?occupantLabel)='en') .
  }}
  ?stadium wdt:P1083 ?cap . 
  ?stadium wdt:P625 ?coords .
}}
"""

GROUPS_QUERY = """
select distinct ?team ?countryLabel ?flag ?coachLabel ?captainLabel
where {{
  wd:{} wdt:P1923 ?team .
  optional {{?team wdt:P286 ?coach . }}
  optional {{?team wdt:P634 ?captain .}}
  ?team wdt:P1532 ?country .
  ?team wdt:P41 ?flag .  
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}} order by ?group
"""

GR_MATCHES_QUERY = """
select ?match ?teamLabel ?goals ?locationLabel ?date ?winnerLabel
where {{
  wd:{} wdt:P527 ?match .
  ?match p:P1923 [
    ps:P1923 ?team ;
    pq:P1351 ?goals ;
  ] .
  ?match wdt:P276 ?location .
  ?match wdt:P585 ?date .
  optional {{?match wdt:P1346 ?winner .}}
  
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}
"""

PARTICIPANTS_QUERY = """
select distinct ?teamLabel
where {
  wd:Q284163 wdt:P710 ?team .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
} 
"""