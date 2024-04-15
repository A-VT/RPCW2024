from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Set up GraphDB endpoint details
base_url = "http://localhost:7200"  # Assuming GraphDB runs on localhost
repository_id = "Alunos"  # The name of your repository in GraphDB

# Function to execute a SPARQL query against the repository
def execute_sparql_query(query):
    try:
        # Construct the SPARQL query endpoint URL
        query_url = f"{base_url}/repositories/{repository_id}"
        
        # Set the SPARQL query headers
        headers = {
            "Content-Type": "application/sparql-query",
            "Accept": "application/sparql-results+json"
        }
        
        # Send the SPARQL query request
        response = requests.post(query_url, data=query, headers=headers)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Return the JSON response
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error executing SPARQL query: {e}")
        return None

# Route for getting the list of students
@app.route('/api/alunos', methods=['GET'])
def get_students():
    # Example SPARQL query to get all students
    sparql_query = """
    PREFIX : <http://www.semanticweb.org/avt/fichaAf/alunos/>

SELECT ?aluno ?idAluno ?nome ?curso
    WHERE {
      ?aluno a :Aluno.
      ?aluno :idAluno ?idAluno.
      ?aluno :nome ?nome.
      ?aluno :curso ?curso .
    } ORDER BY ASC(?nome)
    """

    # Execute the SPARQL query
    result = execute_sparql_query(sparql_query)
    
    # Parse the results and return as JSON

    students = []
    if result != [] and result != None:
        for binding in result['results']['bindings']:
            a = binding.get('idAluno')
            b = binding.get('nome')
            c = binding.get('curso')

            if a :
                a = a['value']
            if b :
                b = b['value']
            if c :
                c = c['value']

            student = {"studentId":a,"studentName":b,"studentCourse":c}
            students.append(student)
    return jsonify({"students": students})



# Route for getting the information of a student by ID
@app.route('/api/alunos/<id>', methods=['GET'])
def get_student_by_id(id):
    # Example SPARQL query to get the information of a student by ID
    sparql_query = f"""
    PREFIX ex: <http://www.semanticweb.org/avt/fichaAf/alunos/>

    SELECT ?nome ?curso
    WHERE {{
      ?aluno a ex:Aluno ;
             ex:idAluno "{id}" ;
             ex:nome ?nome ;
             ex:curso ?curso .
    }}
    """

    # Execute the SPARQL query
    result = execute_sparql_query(sparql_query)
    
    # Parse the results and return as JSON
    if result and 'results' in result and 'bindings' in result['results'] and len(result['results']['bindings']) > 0:
        student_info = {
            "studentId": id,
            "studentName": result['results']['bindings'][0]['nome']['value'],
            "studentCourse": result['results']['bindings'][0]['curso']['value']
        }
        return jsonify(student_info)
    else:
        return jsonify({"error": "Student not found"}), 404



# Route for getting the information of a student by Course
@app.route('/api/alunos?curso=<cursoId>', methods=['GET'])
def get_student_by_curso(cursoId):
    # Example SPARQL query to get the information of a student by ID
    sparql_query = f"""
    PREFIX ex: <http://www.semanticweb.org/avt/fichaAf/alunos/>

    SELECT ?nome ?id
    WHERE {{
      ?aluno a ex:Aluno ;
             ex:idAluno ?id ;
             ex:nome ?nome ;
             ex:curso "{cursoId}" .
    }} ORDER BY ASC(?nome)
    """

    # Execute the SPARQL query
    result = execute_sparql_query(sparql_query)
    
    # Parse the results and return as JSON
    if result and 'results' in result and 'bindings' in result['results'] and len(result['results']['bindings']) > 0:
        student_info = {
            "studentId": result['results']['bindings'][0]['id']['value'],
            "studentName": result['results']['bindings'][0]['nome']['value'],
            "studentCourse": cursoId
        }
        return jsonify(student_info)
    else:
        return jsonify({"error": "Student not found"}), 404



# Route for getting the information of a student by Course
@app.route('/api/alunos/tpc', methods=['GET'])
def get_student_and_tpc():
    # Example SPARQL query to get all students
    sparql_query = """
    PREFIX : <http://www.semanticweb.org/avt/fichaAf/alunos/>

SELECT ?aluno ?idAluno ?nome ?curso
    WHERE {
      ?aluno a :Aluno.
      ?aluno :idAluno ?idAluno.
      ?aluno :nome ?nome.
      ?aluno :curso ?curso .
    } ORDER BY ASC(?nome)
    """

    # Execute the SPARQL query
    result = execute_sparql_query(sparql_query)
    
    # Parse the results and return as JSON

    students = []
    if result != [] and result != None:
        for binding in result['results']['bindings']:
            idAluno = binding.get('idAluno')
            nome = binding.get('nome')
            curso = binding.get('curso')

            if idAluno :
                idAluno = idAluno['value']
            if nome :
                nome = nome['value']
            if curso :
                curso = curso['value']

            student = {"studentId":idAluno,"studentName":nome,"studentCourse":curso, "tpc":{}}

            sparql_subquery = f"""
    PREFIX ex: <http://www.semanticweb.org/avt/fichaAf/alunos/>

    SELECT ?tpcNota ?tpcNome
    WHERE {{
        ?aluno a ex:Aluno ;
            ex:idAluno "{idAluno}".
        ?aluno ex:did_TPC ?tpc.
            ?tpc ex:tpc_nome ?tpcNome.
            ?tpc ex:tpc_nota ?tpcNota.
    }} ORDER BY ASC(?nome)
    """
            result_sub = execute_sparql_query(sparql_subquery)
            if result_sub != [] and result_sub != None:
                for sub in result_sub['results']['bindings']:
                    print(sub)
                    tpcNome = sub.get('tpcNome')
                    tpcNota = sub.get('tpcNota')

                    if tpcNome :
                        tpcNome = tpcNome['value']
                    if tpcNota :
                        tpcNota = tpcNota['value']
                    
                    if tpcNota and tpcNome:
                        tpc_key = f"tpc_{idAluno}_{tpcNome}"
                        tpc_info = {"tpcNome":tpcNome,"tpcNota":tpcNota}
                        student["tpc"][tpc_key] = tpc_info
                
            
            students.append(student)

    #print({"students": students})
    return jsonify({"students": students})

# Route for getting the information of a student by Course
@app.route('/api/alunos?groupBy=curso', methods=['GET'])
def get_students_in_course ():
    # Example SPARQL query to get the information of a student by ID
    sparql_query = f"""
    PREFIX ex: <http://www.semanticweb.org/avt/fichaAf/alunos/>
    
    select (count(?aluno) as ?count) ?curso where {{
        ?aluno a :Aluno .
        ?aluno :curso ?curso
    }} group by (?curso)

    """

    # Execute the SPARQL query
    result = execute_sparql_query(sparql_query)
    
    results = {}

    if result != [] and result != None:
        for binding in result['results']['bindings']:
            nAlunos = binding.get('count')
            curso = binding.get('curso')
        results.append( {"curso":curso, "nAlunos": nAlunos})
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run()


