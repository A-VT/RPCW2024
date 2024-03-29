from rdflib import Graph, Literal, RDF, URIRef, Namespace


### DOCUMENTATION
#https://rdflib.readthedocs.io/en/stable/gettingstarted.html
#https://rdflib.readthedocs.io/en/stable/apidocs/examples.html



# Create a Graph
g = Graph()

# Parse in an RDF file hosted on the Internet
g.parse("http://www.w3.org/People/Berners-Lee/card")  #cinemas.ttl (might be the relative path to a local file)

nmspc = Namespace("ontology link")


print(len(g))
print(g.serialize)




#print("===============")
#for smth in g:
#   pprint.pprint(smth)








# Loop through each triple in the graph (subj, pred, obj)
for subj, pred, obj in g:
    # Check if there is at least one triple in the Graph
    if (subj, pred, obj) not in g:
       raise Exception("It better be!")

# Print the number of "triples" in the Graph
print(f"Graph g has {len(g)} statements.")
# Prints: Graph g has 86 statements.

# Print out the entire Graph in the RDF Turtle format
print(g.serialize(format="turtle"))