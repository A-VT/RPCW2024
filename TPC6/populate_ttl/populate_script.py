from rdflib import Namespace, URIRef, Graph, Literal
from rdflib.namespace import RDF, OWL, FOAF
import json

g = Graph()
g.parse("TPC6/populate_ttl/ontology_turtle.ttl")

nmp = Namespace("http://rpcw.di.uminho.pt/2024/cinema/")

with open("TPC6/data/data.json", 'r') as f:
    data = json.load(f)

persons = set()  # Set to store unique persons
films = set()    # Set to store unique films

i = 0

for index_film, film in enumerate(data):
    film_uri = URIRef(film['iri'])

    # Adding film as an individual of class Film
    g.add((film_uri, RDF.type, OWL.NamedIndividual))  
    g.add((film_uri, RDF.type, nmp.Film))  

    # Adding properties for the film
    g.add((film_uri, nmp.name, Literal(film['name'])))
    g.add((film_uri, nmp.year, Literal(film['year'])))
    g.add((film_uri, nmp.abstract, Literal(film['abstract'])))

    # Adding directors
    for director in film.get('directors', []):
        director_uri = URIRef(director['iri'])

        if director_uri not in persons:
            # Adding director as an individual of class Person
            g.add((director_uri, RDF.type, OWL.NamedIndividual))
            g.add((director_uri, RDF.type, nmp.Person))  
            persons.add(director_uri)

        # Adding relationship between director and film using object property
        g.add((film_uri, nmp.directed_by, director_uri))

    # Adding producers
    for producer in film.get('producers', []):
        producer_uri = URIRef(producer['iri'])

        if producer_uri not in persons:
            # Adding producer as an individual of class Person
            g.add((producer_uri, RDF.type, OWL.NamedIndividual))
            g.add((producer_uri, RDF.type, nmp.Person))  
            persons.add(producer_uri)

        # Adding relationship between producer and film using object property
        g.add((film_uri, nmp.produced_by, producer_uri))

    # Adding composers
    for composer in film.get('composers', []):
        composer_uri = URIRef(composer['iri'])

        if composer_uri not in persons:
            # Adding composer as an individual of class Person
            g.add((composer_uri, RDF.type, OWL.NamedIndividual))
            g.add((composer_uri, RDF.type, nmp.Person))  
            persons.add(composer_uri)

        # Adding relationship between composer and film using object property
        g.add((film_uri, nmp.composed_by, composer_uri))

    # Adding actors
    for actor in film.get('actors', []):
        actor_uri = URIRef(actor['iri'])

        if actor_uri not in persons:
            # Adding actor as an individual of class Person
            g.add((actor_uri, RDF.type, OWL.NamedIndividual))
            g.add((actor_uri, RDF.type, nmp.Person))  
            persons.add(actor_uri)

        # Adding relationship between actor and film using object property
        g.add((film_uri, nmp.acted_in, actor_uri))

    print(f"Done film {index_film}")
    i += 1
    if i == 10:
        break

# Serialize the graph to a file
with open("./TPC6/populate_ttl/populated.ttl", "w") as f_out:
    f_out.write(g.serialize(format="turtle"))