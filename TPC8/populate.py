import json
from rdflib import Graph, Literal, RDF, URIRef, Namespace, OWL
import xml.etree.ElementTree as etree

tree = etree.parse('agenda.xml')
root = tree.getroot()

# Load JSON data
with open('TPC8/royal.xml', 'r') as json_file:
    data = json.load(json_file)

nm = Namespace("http://rpcw.di.uminho.pt/2024/familia")
g = Graph()
g.parse("TPC8/familia-base.ttl")

def create_uri(entity_type, idPessoa, additional_info=None):
    if additional_info:
        return URIRef(f"{nm}{entity_type}_{idPessoa}_{additional_info}")
    return URIRef(f"{nm}{entity_type}_{idPessoa}")
