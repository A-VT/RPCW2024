import requests
import json
import sys
from queries_films import empty_file

headers = {"Accept": "application/sparql-results+json"}
sparql_endpoint = "http://dbpedia.org/sparql"

def create_directorsjson():
    in_file = open("./TPC5/filmjsons/films.json", "r", encoding='utf-8')
    data = json.load(in_file)

    file_path = "./TPC5/filmjsons/directors.json"
    empty_file(file_path)

    for film in data:
        filmiri = film["iri"]
        print(filmiri)

        ##SPARQL query
        sparql_query_directors = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?personiri ?person_iri
        WHERE {{
        optional {{<{filmiri}> dbo:director ?personiri.}}
        optional {{<{filmiri}> dbp:director ?person_iri.}}
        }}
        """
        # Define the parameters
        params = {
            "query": sparql_query_directors,
            "format": "json"
        }
            
        response = requests.get(sparql_endpoint, params=params, headers=headers)
        if response.status_code == 200:
            directors = []
            results = response.json()
            for result in results["results"]["bindings"]:
                person_iri = result.get("personiri", {}).get("value")
                if person_iri is None:
                    person_iri = result.get("person_iri", {}).get("value")
                if person_iri:
                    directors.append({
                        "iri": filmiri,
                        "person_iri": person_iri
                    })
        else:
            print("Error:", response.status_code)
            print(response.text)
    

    out_file = open(file_path, "w") 
    json.dump(directors, out_file, ensure_ascii=True)
    out_file.close()
    print("Should've written to file")
