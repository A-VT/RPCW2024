import xml.etree.ElementTree as etree
from rdflib import Graph, Literal, RDF, URIRef, Namespace, OWL
from rdflib import XSD


# Parse the XML file
tree = etree.parse('TPC8/royal.xml')
root = tree.getroot()

nmp = Namespace("http://rpcw.di.uminho.pt/2024/familia/")
g = Graph()
g.parse("TPC8/familia-base-OG.ttl")

# Iterate over each person element

def create_lst_persons():
    lst_persons = []

    for person in root.findall('person'):
        # Extract relevant information
        person_id = person.find('id').text.replace('/', '')
        name = person.find('name').text.replace('/', '')
        title = person.find('titl').text.replace('/', '') if person.find('titl') is not None else None

        sex_element = person.find('sex')
        sex = sex_element.text.replace('/', '') if sex_element is not None else None

        birthdate_element = person.find('birthdate')
        deathdate_element = person.find('deathdate')

        birthplace_element = person.find('birthplace')
        deathplace_element = person.find('deathplace')
        burialplace_element = person.find('burialplace')

        birthdate = birthdate_element.text.replace('/', '') if birthdate_element is not None else None
        deathdate = deathdate_element.text.replace('/', '') if deathdate_element is not None else None

        birthplace = birthplace_element.text.replace('/', '') if birthplace_element is not None else None
        deathplace = deathplace_element.text.replace('/', '') if deathplace_element is not None else None
        burialplace = burialplace_element.text.replace('/', '') if burialplace_element is not None else None
        
        spouse_element = person.find('spouse')
        spouse = spouse_element.text.replace('/', '') if spouse_element is not None else None
        
        # Extract parents information
        parent_elements = person.findall('parent')
        parents = []
        if parent_elements:
            for parent in parent_elements:
                #parents.append(parent.text.replace('/', ''))
                ref = parent.attrib.get("ref")
                parents.append(ref)
        else:
            parents = None

        # Extract children information
        children = []
        children_elements = person.findall('child')
        if children_elements:
            for child in children_elements:
                ref = child.attrib.get("ref")
                children.append(ref)
                #children.append(child.text.replace('/', ''))
        else:
            children = None
        
        person_info = {
            "id": person_id,
            "name": name,
            "title": title,
            "sex": sex,
            "birthdate": birthdate,
            "birthplace": birthplace,
            "deathdate": deathdate,
            "deathplace": deathplace,
            "burialplace": burialplace,
            "spouse": spouse,
            "parents": parents,
            "children": children
        }

        print(person_info)

        lst_persons.append(person_info)
    
    #print(lst_persons[0])
    return lst_persons

def create_uri(entity_type, idAluno, additional_info=None):
    if additional_info:
        return URIRef(f"{nmp}{entity_type}_{additional_info.replace(' ', '_').replace('/', '')}")
    return URIRef(f"{nmp}{entity_type}_{idAluno}")

def add_to_ontology(lst_persons):
    person_sex = {}
    for ind in lst_persons:
        # Create individual URI
        
        print(f"ind['id']:  {ind['id']}")
        if ind["id"]:
            individual_uri = create_uri('Pessoa', ind["id"])
        else:
            str_identifier = ind["name"].replace(" ", "_")
            individual_uri = create_uri('Pessoa', str_identifier)

        person_sex[individual_uri] = ind["sex"]

        # Add individual type
        g.add((individual_uri, RDF.type, nmp["Pessoa"]))
        
        # Add data properties
        g.add((individual_uri, nmp.nome, Literal(ind["name"])))
        g.add((individual_uri, nmp.title, Literal(ind["title"])))
        g.add((individual_uri, nmp.sex, Literal(ind["sex"])))
        
        # Format date correctly
        if ind["birthdate"]:
            birthdate_literal = Literal(ind["birthdate"], datatype=XSD.string) #XSD.date
            g.add((individual_uri, nmp.birthdate, birthdate_literal))
        if ind["deathdate"]:
            deathdate_literal = Literal(ind["deathdate"], datatype=XSD.string)
            g.add((individual_uri, nmp.deathdate, deathdate_literal))
        
        g.add((individual_uri, nmp.birthplace, Literal(ind["birthplace"])))
        g.add((individual_uri, nmp.deathplace, Literal(ind["deathplace"])))
        g.add((individual_uri, nmp.burialplace, Literal(ind["burialplace"])))


        # Add parent information if available
        if ind["parents"] is not None:
            for parent_id in ind["parents"]:
                parent_uri = create_uri('Pessoa', parent_id)

                if parent_uri in person_sex:
                    if person_sex[parent_uri] == "F":
                        g.add((individual_uri, nmp.temMae, parent_uri))
                    else:

                        g.add((individual_uri, nmp.temPai, parent_uri))

    # Serialize the graph to Turtle format
    g.serialize(destination='TPC8/familia-base.ttl', format='ttl')


population = create_lst_persons()
add_to_ontology(population)


