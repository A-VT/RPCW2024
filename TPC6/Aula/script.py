from rdflib import Namespace,URIRef,Graph, Literal
from rdflib.namespace import RDF, OWL
import pprint
import json


g = Graph()
g.parse("cinema.ttl")


f = open("film.json",'r')
data = f.read()
f.close()

nmp = Namespace("http://rpcw.di.uminho.pt/2024/cinema/") #

for film in data:
    #
    g.add(URIRef(f"{nmp}{film['iri']}", RDF.type, OWL.NamedIndividual))  #creating the individual (?)
    g.add(URIRef(f"{nmp}{film['iri']}", RDF.type, nmp.Film))  #creating the type (?)

    #g.add((donna, RDF.type, FOAF.Person))
    g.add((donna, FOAF.nick, Literal("donna", lang="en")))
    g.add((donna, FOAF.name, Literal("Donna Fales")))
    g.add((donna, FOAF.mbox, URIRef("mailto:donna@example.org")))
    

    
    #g.add(URIRef(f"{cinema}Twilight", RDF.type, OWL.NamedIndividual))
    #g.add(URIRef(f"{cinema}Twilight", RDF.type, cinema.Film))
    #g.add(URIRef(f"{cinema}CatherineHardwicke", RDF.type, OWL.NamedIndividual))
    #g.add(URIRef(f"{cinema}CatherineHardwicke", RDF.type, cinema.Director))
    #g.add(URIRef(f"{cinema}Twilight", cinema.has_director, cinema.CatherineHardwicke))


print(len(g))
print(g.serialize)

print("==========================================")

# for smt in g:
#     pprint.pprint(smt)