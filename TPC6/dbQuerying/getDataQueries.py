import requests
import json
import os
import concurrent.futures
import random
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

def query_actors(movie_iri):

    rel = ["dbo:starring", "dbp:starring"]
    i = 0
    actors = []
    
    success = False
    while not success:
        sparql_query = f"""
            SELECT DISTINCT ?actor ?actorName ?abstract WHERE {{
                <{movie_iri}> {rel[i]} ?actor .
                optional {{?actor rdfs:label ?actorName .
                        filter(lang(?actorName)='en') . }}
                optional {{?actor dbo:abstract ?abstract .
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
            #print("Results Actors:", results_)  # Print the entire results_actors dictionary for debugging

            if "results" in results_ and "bindings" in results_["results"] and results_["results"]["bindings"]:
                for result in results_["results"]["bindings"]:
                    actor = {}
                    actor['iri'] = translate_unicode(result.get('actor', {}).get('value', ''))
                    actor['name'] = translate_unicode(result.get('actorName', {}).get('value', ''))
                    actor['abstract'] = translate_unicode(result.get('abstract', {}).get('value', ''))
                    actors.append(actor)
                    success = True

                    print("Got actors.")
            #else:
            #    print("Error:", response_.status_code)
            #    print(response_.text)

            else:
                if i == 0:
                    i+=1
                    print("Actors++")
                else:
                    print("Error:", response_.status_code)
                    print(response_.text)
                    print("No actors.")
                    break

        return actors

def query_music_composer(movie_iri):

    rel = ["dbo:musicComposer", "dbp:musicComposer"]
    i = 0
    composers = []
    success = False
    while not success:
        sparql_query = f"""
            SELECT DISTINCT ?musicComposer ?musicComposerName ?abstract WHERE {{
                <{movie_iri}> {rel[i]} ?musicComposer .
                optional {{?musicComposer rdfs:label ?musicComposerName .
                        filter(lang(?musicComposerName)='en') . }}
                optional {{?musicComposer dbo:abstract ?abstract .
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
            #print("Results Actors:", results_)  # Print the entire results_actors dictionary for debugging

            if "results" in results_ and "bindings" in results_["results"] and results_["results"]["bindings"]:
                for result in results_["results"]["bindings"]:
                    composer = {}
                    
                    composer['iri'] = translate_unicode(result.get('musicComposer', {}).get('value', ''))
                    composer['name'] = translate_unicode(result.get('musicComposerName', {}).get('value', ''))
                    composer['abstract'] = translate_unicode(result.get('abstract', {}).get('value', ''))
                    composers.append(composer)
                    print("Got composer.")
                    success = True
            else:
                if i == 0:
                    i+=1
                    print("Composer++")
                else:
                    print("Error:", response_.status_code)
                    print(response_.text)
                    print("No composer.")
                    break
                
        return composers


def query_producer(movie_iri):

    rel = ["dbo:producer", "dbp:producer"]
    i = 0
    producers = []
    success = False
    while not success:
        sparql_query = f"""
            SELECT DISTINCT ?producer ?producerName ?abstract WHERE {{
                <{movie_iri}> {rel[i]} ?producer .
                optional {{?producer rdfs:label ?producerName .
                        filter(lang(?producerName)='en') . }}
                optional {{?producer dbo:abstract ?abstract .
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
            #print("Results Actors:", results_)  # Print the entire results_actors dictionary for debugging

            if "results" in results_ and "bindings" in results_["results"] and results_["results"]["bindings"]:
                for result in results_["results"]["bindings"]:
                    producer = {}
                    producer['iri'] = translate_unicode(result.get('producer', {}).get('value', ''))
                    producer['name'] = translate_unicode(result.get('producerName', {}).get('value', ''))
                    producer['abstract'] = translate_unicode(result.get('abstract', {}).get('value', ''))
                    producers.append(producer)
                    print("Got producer.")
                    success = True
            else:
                if i == 0:
                    i+=1
                    print("Producer++")
                else:
                    print("Error:", response_.status_code)
                    print(response_.text)
                    print("No producer.")
                    break
                
        return producers



def query_director(movie_iri):

    rel = ["dbo:director", "dbp:director"]
    i = 0
    directors = []
    success = False
    while not success:
        sparql_query = f"""
            SELECT DISTINCT ?director ?directorName ?abstract WHERE {{
                <{movie_iri}> {rel[i]} ?director .
                optional {{?director rdfs:label ?directorName .
                        filter(lang(?directorName)='en') . }}
                optional {{?director dbo:abstract ?abstract .
                        filter(lang(?abstract)='en') . }}
            }}
        """
        params = {
            "query": sparql_query,
            "format": "json"
        }

        response_directors = requests.get(sparql_endpoint, params=params, headers=headers)
        if response_directors.status_code == 200:
            results_directors = response_directors.json()
            #print("Results Directors:", results_directors)  # Print the entire results_directors dictionary for debugging

            if "results" in results_directors and "bindings" in results_directors["results"] and results_directors["results"]["bindings"]:
                for result in results_directors["results"]["bindings"]:
                    director = {}
                    director['iri'] = translate_unicode(result.get('director', {}).get('value', ''))
                    director['name'] = translate_unicode(result.get('directorName', {}).get('value', ''))
                    director['abstract'] = translate_unicode(result.get('abstract', {}).get('value', ''))
                    directors.append(director)
                    print("Got director.")
                    success = True
            else:
                if i == 0:
                    i+=1
                    print("Director++")
                else:
                    print("Error:", response_directors.status_code)
                    print(response_directors.text)
                    print("No director.")
                    break


        return directors


def fetch_data(offset, limit):
    filmsss = []
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
                    film["year"] = translate_unicode(result["year"]["value"]) if "year" in result else ""  # Handle case where year is not present
                    film["abstract"] = result["filmAbstract"]["value"]
                    filmsss.append(film)

                success = True
                print(f"Got data for offset: {offset}")
            else:
                print(f"No data found for offset: {offset}")
                break
                #time.sleep(1)  # Adding a delay before retrying
        else:
            print(f"Failed to fetch data for offset {offset}, status code: {response.status_code}")
            time.sleep(1)  # Adding a delay before retrying

    for film in filmsss:
        #print(film)
        film["directors"] = query_director(film["iri"])
        film["producers"] = query_producer(film["iri"])
        film["composers"] = query_music_composer(film["iri"])
        film["actors"] = query_actors(film["iri"])

    return filmsss, offset  # Return films list and offset

def write_to_file(films, file_path, offset, processed_offsets):
    if offset not in processed_offsets:
        with open(file_path, "a") as out_file:
            for film in films:
                json.dump(film, out_file, ensure_ascii=True)
                out_file.write(',\n')
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
    num_sets = 2 #200
    num_threads_per_set = 10 #10
    limit = 10 #100
    create_filmsjson(file_path, num_sets, num_threads_per_set, limit)
