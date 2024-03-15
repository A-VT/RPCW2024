import requests
import json
import sys

def create_filmsjson():
    # Define the DBpedia SPARQL endpoint
    sparql_endpoint = "http://dbpedia.org/sparql"

    # Define the SPARQL query
    sparql_query_films = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT *
    WHERE
    {
    ?film a dbo:Film.
    ?film dbp:name ?filmName.
    ?film dbo:abstract ?filmAbstract.
    ?film rdfs:label  ?label.
    filter(lang(?label)="en").
    }
    """

    # Define the headers
    headers = {
        "Accept": "application/sparql-results+json"
    }

    # Define the parameters
    params = {
        "query": sparql_query_films,
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
            print(result)
            film_IRI = result["film"]["value"]
            film_name = result["filmName"]["value"]
            film_abstract = result["filmAbstract"]["value"]

            desport.append({
                "iri":film_IRI,
                "nome": film_name,
                "abstract": film_abstract,
            })


        out_file = open("./TPC5/filmjsons/films.json", "w") 
        json.dump(desport, out_file, ensure_ascii=False)
        out_file.close()

    else:
        print("Error:", response.status_code)
        print(response.text)

def create_directorsjson():
    in_file = open("./TPC5/filmjsons/films.json", "r")
    data = json.load(in_file)

    for film in data:
        filmiri = film["iri"]




def main():
    create_filmsjson()
    create_directorsjson()


if __name__ == '__main__':
    main()