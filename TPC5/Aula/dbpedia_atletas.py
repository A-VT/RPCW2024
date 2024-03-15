import requests
import json
import sys

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"

# Define the headers
headers = {
    "Accept": "application/sparql-results+json"
}


in_file = open("./TPC5/desport.json", "r")
data = json.load(in_file)

for d in data:
    sportiri = d["iri"]
    
    #SPARQL query
    sparql_query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    select distinct ?name ?name2  ?nat ?dob ?dod ?pob  where {{
    ?s dbp:sport <{sportiri}>.
    ?s dbp:name ?name. 
    ?s foaf:name ?name2.
    ?s dbp:nationality ?nat.
    optional{{?s dbo:birthDate ?dob.}}
    optional{{?s dbo:deathDate ?dod.}}
    optional{{?s dbo:birthPlace ?pob. ?pob rdfs:label ?locallabel. filter(lang(?pob) = "en").}}
    }}
    """

    #Define parameters
    params = {
        "query": sparql_query,
        "format": "json"
    }

    # Send the SPARQL query using requests
    response = requests.get(sparql_endpoint, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        
        # Print the results
        athletes = []
        for result in results["results"]["bindings"]:

            #sport_uri = result["athlete"]["value"]
            athlete_nome = result["name"]["value"]
            athlete_dob = result["dob"]["value"]
            athlete_dod = result["dod"]["value"]
            athlete_pob = result["pob"]["value"]

            athletes.append({
                "iri":sport_uri,
                "nome":athlete_nome,
                "dataNasc": athlete_dob,
                "dataObito" : athlete_dod,
                "localNasc" : athlete_pob
            })

        out_file = open("./TPC5/athlete.json", "w") 
        json.dump(athletes, out_file, ensure_ascii=False)
        out_file.close()
    else:
        print("Error:", response.status_code)
        print(response.text)

