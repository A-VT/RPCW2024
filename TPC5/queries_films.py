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
    while i < 10:
        
        sparql_query_films = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT *
        WHERE
        {{
        ?film a dbo:Film.
        ?film dbp:name ?filmName.
        ?film dbo:abstract ?filmAbstract.

        ?film dbo:director ?dir.
        ?film dbo:producer ?prod.
        ?film dbo:musicComposer ?mu.
        ?film dbo:starring ?st.

        ?film rdfs:label ?label.
        FILTER(langMatches(lang(?filmAbstract), "en") && langMatches(lang(?label), "en")).
        }}
        GROUP BY ?film
        OFFSET {i*10000}
        LIMIT {10000}
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
            filmsss = []
            for result in results["results"]["bindings"]:
                if result != []:
                    film_IRI = result["film"]["value"]
                    film_name = result["filmName"]["value"]
                    film_abstract = result["filmAbstract"]["value"]

                    dir_iri = result.get("dir", {}).get("value")
                    #if dir_iri is None:
                    #    dir_iri = result.get("director", {}).get("value")

                    prod_iri = result.get("prod", {}).get("value")
                    #if prod_iri is None:
                    #    prod_iri = result.get("producer", {}).get("value")

                    mus_iri = result.get("mu", {}).get("value")
                    #if mus_iri is None:
                    #    mus_iri = result.get("musicComp", {}).get("value")

                    st_iri = result.get("st", {}).get("value")
                    #if st_iri is None:
                    #    st_iri = result.get("starring", {}).get("value")

                    filmsss.append({
                        "iri":film_IRI,
                        "nome": film_name,
                        "abstract": film_abstract,
                        "director":dir_iri,
                        "producer":prod_iri,
                        "music_composer": mus_iri,
                        "starring": st_iri,
                    })

        else:
            print("Error:", response.status_code)
            print(response.text)

        i+=1

    out_file = open(file_path, "w") 
    json.dump(filmsss, out_file, ensure_ascii=True)
    out_file.close()

    print("\n\nDONE: FILMS.JSON\n\n")
