import json
from rdflib import Graph, Literal, RDF, URIRef, Namespace, OWL
from rdflib.namespace import XSD

# Load JSON data
with open('FichaAfericao/Ex1/aval-alunos.json', 'r') as json_file:
    data = json.load(json_file)

# Define RDF namespaces
avt = Namespace("http://www.semanticweb.org/avt/fichaAf/alunos/")
g = Graph()
g.parse("FichaAfericao/Ex1/fichaAf_alunos_OG.ttl")
#g.bind("avt", avt)

# Function to create unique URI for individual
def create_uri(entity_type, idAluno, additional_info=None):
    if additional_info:
        return URIRef(f"{avt}{entity_type}_{idAluno}_{additional_info}")
    return URIRef(f"{avt}{entity_type}_{idAluno}")

# Iterate over students
for student in data['alunos']:
    idAluno = student['idAluno']

    # Student URI
    student_uri = create_uri('Aluno', idAluno)

    # Add student details
    g.add((student_uri, RDF.type, OWL.NamedIndividual))  # Explicitly define as named individual
    g.add((student_uri, RDF.type, avt.Aluno))

    g.add((student_uri, avt.idAluno, Literal(idAluno)))
    g.add((student_uri, avt.nome, Literal(student['nome'])))
    g.add((student_uri, avt.curso, Literal(student['curso'])))

    # Iterate over TPCs
    for tpc in student['tpc']:
        tpc_uri = create_uri('TPC', idAluno, tpc['tp'])  # Unique URI for TPC
        g.add((tpc_uri, RDF.type, OWL.NamedIndividual))  # Explicitly define as named individual
        g.add((tpc_uri, RDF.type, avt.TPC))
        g.add((tpc_uri, avt.tpc_nome, Literal(tpc['tp'])))
        g.add((tpc_uri, avt.tpc_nota, Literal(tpc['nota'], datatype=XSD.float)))
        g.add((student_uri, avt.did_TPC, tpc_uri))
    # Add project
    project_uri = create_uri('Projeto', idAluno)
    g.add((project_uri, RDF.type, OWL.NamedIndividual))  # Explicitly define as named individual
    g.add((project_uri, RDF.type, avt.Projeto))
    g.add((student_uri, avt.did_Project, project_uri))
    g.add((project_uri, avt.projeto, Literal(student['projeto'])))
    # Add exams
    if 'normal' in student['exames']:
        exam_uri = create_uri('Exame', idAluno)
        g.add((exam_uri, RDF.type, OWL.NamedIndividual))  # Explicitly define as named individual
        g.add((exam_uri, RDF.type, avt.Exame))
        g.add((student_uri, avt.did_Exam, exam_uri))
        g.add((exam_uri, avt.normal, Literal(student['exames']['normal'], datatype=XSD.int)))
        
    if 'especial' in student['exames']:
        exam_uri = create_uri('Exame', idAluno)
        g.add((exam_uri, RDF.type, OWL.NamedIndividual))  # Explicitly define as named individual
        g.add((exam_uri, RDF.type, avt.Exame))
        g.add((student_uri, avt.did_Exam, exam_uri))
        g.add((exam_uri, avt.especial, Literal(student['exames']['especial'], datatype=XSD.int)))
    if 'recurso' in student['exames']:
        exam_uri = create_uri('Exame', idAluno)
        g.add((exam_uri, RDF.type, OWL.NamedIndividual))  # Explicitly define as named individual
        g.add((exam_uri, RDF.type, avt.Exame))
        g.add((student_uri, avt.did_Exam, exam_uri))
        g.add((exam_uri, avt.recurso, Literal(student['exames']['recurso'], datatype=XSD.int)))

# Serialize RDF graph to TTL file
g.serialize(destination='FichaAfericao/Ex1/fichaAf_alunos_populated.ttl', format='ttl')
