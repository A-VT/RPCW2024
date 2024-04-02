import requests
import json
import os
import concurrent.futures
import re
import time

headers = {"Accept": "application/sparql-results+json"}
sparql_endpoint = "http://dbpedia.org/sparql"

data = []

def empty_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.truncate(0)
            print(f"Contents of {file_path} have been emptied.")
    else:
        print(f"File {file_path} does not exist.")

def translate_unicode(text):
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), text)

def query_resource(movie_iri, relation):
    rel = ["dbo:" + relation, "dbp:" + relation]
    i = 0
    resources = []
    success = False
    while not success:
        sparql_query = f"""
            SELECT DISTINCT ?{relation} ?{relation}Name ?abstract WHERE {{
                <{movie_iri}> {rel[i]} ?{relation} .
                optional {{?{relation} rdfs:label ?{relation}Name .
                        filter(lang(?{relation}Name)='en') . }}
                optional {{?{relation} dbo:abstract ?abstract .
                        filter(lang(?abstract)='en') . }}
            }}
        """
        params = {
            "query": sparql_query,
            "format": "json"
        }

        response_ = requests.get(sparql_endpoint, params=params, headers=headers)

        if response_.status_code == 200:
            results_ = response_.json()

            if "results" in results_ and "bindings" in results_["results"] and results_["results"]["bindings"]:
                for result in results_["results"]["bindings"]:
                    resource = {}
                    resource['iri'] = translate_unicode(result.get(relation, {}).get('value', ''))
                    resource['name'] = translate_unicode(result.get(f'{relation}Name', {}).get('value', ''))
                    resource['abstract'] = translate_unicode(result.get('abstract', {}).get('value', ''))
                    resources.append(resource)
                    success = True
            else:
                if i == 0:
                    i+=1
                else:
                    print("Error:", response_.status_code)
                    print(response_.text)
                    break
        return resources

def fetch_data(offset, limit):
    films = []
    success = False
    print(f"offset {offset} | limit {limit}")

    query_films = f"""
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT DISTINCT ?film ?filmName ?filmAbstract ?year ?label
            WHERE
            {{
            ?film a dbo:Film.
            ?film dbp:name ?filmName.
            ?film dbo:abstract ?filmAbstract.

            OPTIONAL {{
                ?film dbp:released ?year.
            }}

            ?film rdfs:label ?label.
            FILTER (LANG(?filmAbstract) = "en" && LANG(?label) = "en")
            }}
            OFFSET {offset}
            LIMIT {limit}
            """
        
    while not success:
        params = {
            "query": query_films,
            "format": "json"
        }

        response = requests.get(sparql_endpoint, params=params, headers=headers)
        if response.status_code == 200:
            results = response.json()

            if "results" in results and "bindings" in results["results"] and results["results"]["bindings"]:
                for result in results["results"]["bindings"]:
                    film = {}
                    film["iri"] = translate_unicode(result["film"]["value"])
                    film["name"] = translate_unicode(result["filmName"]["value"])
                    film["year"] = translate_unicode(result["year"]["value"]) if "year" in result else ""
                    film["abstract"] = result["filmAbstract"]["value"]
                    films.append(film)

                success = True
                print(f"Got data for offset: {offset}")
            else:
                print(f"No data found for offset: {offset}")
                break
        else:
            print(f"Failed to fetch data for offset {offset}, status code: {response.status_code}")
            time.sleep(1)

    for film in films:
        film["directors"] = query_resource(film["iri"], "director")
        film["producers"] = query_resource(film["iri"], "producer")
        film["composers"] = query_resource(film["iri"], "musicComposer")
        film["actors"] = query_resource(film["iri"], "starring")

    return films, offset

def write_to_file(films, file_path, offset, processed_offsets):
    if offset not in processed_offsets:
        with open(file_path, "a") as out_file:
            for film in films:
                json.dump(film, out_file, ensure_ascii=True)
                out_file.write(',\n')
            print(f"Data appended to file for offset: {offset}")
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
            
            concurrent.futures.wait(futures)
            
            for future in futures:
                films, offset = future.result()
                write_to_file(films, file_path, offset, processed_offsets)

    print("\n\nDONE: FILMS.JSON\n\n")

if __name__ == "__main__":
    file_path = "./TPC6/data/data.json"
    num_sets = 2
    num_threads_per_set = 10
    limit = 1000
    create_filmsjson(file_path, num_sets, num_threads_per_set, limit)
