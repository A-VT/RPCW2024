import requests
import json
import sys


headers = {"Accept": "application/sparql-results+json"}
sparql_endpoint = "http://dbpedia.org/sparql"


def create_directorsjson():
    in_file = open("./TPC5/filmjsons/films.json", "r")
    data = json.load(in_file)

    for film in data:
        filmiri = film["iri"]

        #SPARQL query
        sparql_query_directors = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT *
        WHERE {{
        #?film dbo:Film <{filmiri}>.
        <{filmiri}> dbp:name ?filmName.
        }}
        """

        #Define parameters
        params = {
            "query": sparql_query_directors,
            "format": "json"
        }

        # Send the SPARQL query using requests
        response2 = requests.get(sparql_query_directors, params=params, headers=headers)
        if response2.status_code == 200:
            directors = []

            results = response2.json()
            for result in results["results"]["bindings"]:
                athlete_nome = result["name"]["value"]

                directors.append({
                "iri":filmiri,
                "nome":athlete_nome
                })

            out_file = open("./TPC5/filmjsons/directors.json", "w") 
            json.dump(directors, out_file, ensure_ascii=False)
            out_file.close()
        else:
            print("Error:", response2.status_code)
            print(response2.text)

