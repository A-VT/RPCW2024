def query_producer(movie_iri):

    rel = ["dbo:producer", "dbp:producer"]
    i = 0
    
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
            print("Results Actors:", results_)  # Print the entire results_actors dictionary for debugging

            producers = []

            if "results" in results_ and "bindings" in results_["results"] and results_["results"]["bindings"]:
                for result in results_["results"]["bindings"]:
                    producer = {}
                    producer['iri'] = result.get('producer', {}).get('value', '')
                    producer['name'] = result.get('producerName', {}).get('value', '')
                    producer['abstract'] = result.get('abstract', {}).get('value', '')
                    producers.append(producer)
                    success = True
            else:
                print("Error:", response_.status_code)
                print(response_.text)
                
        return producers
