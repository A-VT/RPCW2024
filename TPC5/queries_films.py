import requests
import json
import os

# Query headers + endpoint
headers = {"Accept": "application/sparql-results+json"}
sparql_endpoint = "http://dbpedia.org/sparql"

def empty_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.truncate(0)
            print(f"Contents of {file_path} have been emptied.")
    else:
        print(f"File {file_path} does not exist.")


def create_filmsjson():
    # empty the file of 
    file_path = "./TPC5/filmjsons/films.json"
    empty_file(file_path)

    i = 0
    while i < 60:
        
        sparql_query_films = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT *
        WHERE
        {{
        ?film a dbo:Film.
        ?film dbp:name ?filmName.
        ?film dbo:abstract ?filmAbstract.
        ?film rdfs:label ?label.
        FILTER(lang(?label)="en").
        }}
        OFFSET {i*10000}
        LIMIT {(i+1)*10000}
        """

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

            #append to outfile
            out_file = open(file_path, "a") 
            json.dump(desport, out_file, ensure_ascii=False)
            out_file.close()

        else:
            print("Error:", response.status_code)
            print(response.text)

        i+=1
    
    print("\n\nDONE: FILMS.JSON\n\n")
