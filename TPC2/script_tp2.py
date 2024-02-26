import json
import sys
import shutil
from collections import defaultdict

def main():
    #json reading
    f = open("./TPC2/db2.json")
    bd = json.load(f)
    f.close()

    shutil.copyfile("./TPC2/ontology_original.owl", "./TPC2/populated_ontology.owl")
    out_f = open("./TPC2/populated_ontology.owl", "a",encoding='utf-8')

    students = bd["alunos"]
    courses = bd["cursos"]
    instruments = bd["instrumentos"]


    #ttl creation
    ttl = ""
    ttl += """
    #################################################################
    #    Individuals
    #################################################################
    """
    dic_al_c = {}
    for s in students:
        dic_al_c[s['id']] = s['curso']
        line_instrument =f"""
        ###  http://rpcw.di.uminho.pt/2024/music_school#{s['id']}
        :{s['id']} rdf:type owl:NamedIndividual ,
                   :Student ;
          :enrolled_in :{s['curso']} ;
          :studentId "{s['id']}" ;
          :name "{s['nome']}"^^xsd:string;
          :courseYear "{s['anoCurso']}"^^xsd:int ;
          :dateBirth "{s['dataNasc']}"^^xsd:dateTime;
        """
        ttl += line_instrument
    

    inverted_dict = defaultdict(list)
    for key, value in dic_al_c.items():
        inverted_dict[value].append(key)
    print(inverted_dict)

    str_courses = ":has_student : ;"
    
    for c in courses:
        str_courses = ""
        students = inverted_dict[c['id']]
        for s in students:
            str_courses += f":has_student : {s} ;\n\t\t"
        line_instrument =f"""
        ###  http://rpcw.di.uminho.pt/2024/music_school#{c['id']}
        :{c['id']} rdf:type owl:NamedIndividual ,
                  :Course ;
         {str_courses}
         :teaches : {c['instrumento']['id']};
         :courseId "{c['id']}"^^xsd:string .
        """
        ttl += line_instrument



##    str_instruments = ":taught_in : ;"
##
##    for i in instruments:
##        print(i)
##        line_instrument =f"""
##        ###  http://rpcw.di.uminho.pt/2024/music_school#{i['#text']}
##        :{i['#text']} rdf:type owl:NamedIndividual ,
##                      :Instrument ;
##             {str_instruments}
##             :instrumentId "{i['id']}" ;
##             :text "{i['#text']}" .
##        """
##        ttl += line_instrument
##
    out_f.write(ttl)

if __name__ == "__main__":
    main()