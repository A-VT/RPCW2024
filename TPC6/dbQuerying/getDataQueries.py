import requests
import json
import os
import concurrent.futures
import random
import time

headers = {"Accept": "application/sparql-results+json"}
sparql_endpoint = "http://dbpedia.org/sparql"

def empty_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.truncate(0)
            print(f"Contents of {file_path} have been emptied.")
    else:
        print(f"File {file_path} does not exist.")

def fetch_data(offset, limit):
    filmsss = []
    success = False

    while not success:
        sparql_query_films = f"""
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT DISTINCT ?film ?filmName ?filmAbstract ?dir ?prod ?mu ?starring ?label
            WHERE
            {{
            ?film a dbo:Film.
            ?film dbp:name ?filmName.
            ?film dbo:abstract ?filmAbstract.

            OPTIONAL {{
                ?film dbo:director ?dir.
            }}
            OPTIONAL {{
                ?film dbo:producer ?prod.
            }}
            OPTIONAL {{
                ?film dbo:musicComposer ?mu.
            }}
            OPTIONAL {{
                ?film dbo:starring ?st.
            }}

            ?film rdfs:label ?label.
            FILTER (LANG(?filmAbstract) = "en" && LANG(?label) = "en")
            }}
            OFFSET {offset}
            LIMIT {limit}
            """

        params = {
            "query": sparql_query_films,
            "format": "json"
        }

        response = requests.get(sparql_endpoint, params=params, headers=headers)

        if response.status_code == 200:
            results = response.json()

            if "results" in results and "bindings" in results["results"] and results["results"]["bindings"]:
                for result in results["results"]["bindings"]:
                    film_IRI = result["film"]["value"]
                    film_name = result["filmName"]["value"]
                    film_abstract = result["filmAbstract"]["value"]

                    director = [r["dir"]["value"] for r in results["results"]["bindings"] if "dir" in r]
                    producer = [r["prod"]["value"] for r in results["results"]["bindings"] if "prod" in r]
                    music_composer = [r["mu"]["value"] for r in results["results"]["bindings"] if "mu" in r]
                    starring = [r["st"]["value"] for r in results["results"]["bindings"] if "st" in r]

                    filmsss.append({
                        "iri": film_IRI,
                        "nome": film_name,
                        "abstract": film_abstract,
                        "director": director,
                        "producer": producer,
                        "music_composer": music_composer,
                        "starring": starring,
                    })
                success = True
                print(f"Got data for offset: {offset}")
            else:
                print(f"No data found for offset: {offset}")
                break
                #time.sleep(1)  # Adding a delay before retrying
        else:
            print(f"Failed to fetch data for offset {offset}, status code: {response.status_code}")
            time.sleep(1)  # Adding a delay before retrying

    return filmsss, offset  # Return films list and offset

def write_to_file(films, file_path, offset, processed_offsets):
    if offset not in processed_offsets:
        with open(file_path, "a") as out_file:
            for film in films:
                json.dump(film, out_file, ensure_ascii=True)
                out_file.write('\n')
            print(f"Data appended to file for offset: {offset}")  # Print offset after appending to file
        processed_offsets.add(offset)

def create_filmsjson(file_path, num_sets, num_threads_per_set, limit):
    empty_file(file_path)
    processed_offsets = set()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads_per_set) as executor:
        for nSet in range(1, num_sets + 1):
            futures = []
            for indexThread in range(1, num_threads_per_set + 1):
                offset = (nSet - 1) * num_threads_per_set * limit + (indexThread - 1) * limit
                futures.append(executor.submit(fetch_data, offset, limit))
            
            # Wait for all threads in the current set to complete
            concurrent.futures.wait(futures)
            
            for future in futures:
                films, offset = future.result()  # Unpack the result tuple
                write_to_file(films, file_path, offset, processed_offsets)

    print("\n\nDONE: FILMS.JSON\n\n")

if __name__ == "__main__":
    file_path = "./TPC6/data/data.json"
    num_sets = 100
    num_threads_per_set = 10
    limit = 1000
    create_filmsjson(file_path, num_sets, num_threads_per_set, limit)
