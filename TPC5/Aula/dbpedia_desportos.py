import requests
import json
import sys

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"

# Define the SPARQL query
sparql_query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?desporto ?label ?abstract
WHERE {
    ?desporto a dbo:Sport ;
              rdfs:label ?label ;
              dbo:abstract ?abstract .
    FILTER (LANG(?label) = 'en' && LANG(?abstract) = 'en') .
}
"""

# Define the headers
headers = {
    "Accept": "application/sparql-results+json"
}

# Define the parameters
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
    desport = []
    for result in results["results"]["bindings"]:
        sport_uri = result["desporto"]["value"]
        sport_label = result["label"]["value"]
        sport_abstract = result["abstract"]["value"]

        desport.append({
            "iri":sport_uri,
            "designacao": sport_label,
            "descricao" : sport_abstract
        })

    out_file = open("./TPC5/desport.json", "w") 
    json.dump(desport, out_file, ensure_ascii=False)
    out_file.close()
        #print(f"Sport URI: {sport_uri}")
        #print(f"Label: {sport_label}")
        #print(f"Abstract: {sport_abstract}")
        #print("---------------------------------------")

else:
    print("Error:", response.status_code)
    print(response.text)

