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
          :dateBirth "{s['dataNasc']}"^^xsd:dateTime.
        """
        ttl += line_instrument
    

    inverted_dict = defaultdict(list)
    for key, value in dic_al_c.items():
        inverted_dict[value].append(key)

    #dic_instruments = {instrument['#text']: instrument['id'] for instrument in instruments}
    #print(dic_instruments)
        
    dic_ins_c = {}
    for c in courses:
        str_courses = ""
        students = inverted_dict[c['id']]
        for s in students:
            str_courses += f":{s}, "
        str_courses = str_courses[:-2]
        
        if c['instrumento']['id'] not in dic_ins_c:
            dic_ins_c[c['instrumento']['id']] = [c['id']]
        else:
            dic_ins_c[c['instrumento']['id']].append(c['id'])

        line_instrument =f"""
        ###  http://rpcw.di.uminho.pt/2024/music_school#{c['id']}
        :{c['id']} rdf:type owl:NamedIndividual ,
                  :Course ;
         :has_student {str_courses};
         :teaches :{c['instrumento']['id']} ;
         :courseId "{c['id']}"^^xsd:string .
        """
        ttl += line_instrument

    print(f"dic_ins_c: {dic_ins_c}")
    for i in instruments:
        str_courses = ""
        vals = dic_ins_c[i['id']]
        for val in vals:
            str_courses += f":{val}, "
        str_courses = str_courses[:-2]

        line_instrument =f"""
        ###  http://rpcw.di.uminho.pt/2024/music_school#{i['id']}
        :{i['id']} rdf:type owl:NamedIndividual ,
                      :Instrument ;
             :taught_in {str_courses};
             :instrumentId "{i['id']}" .
        """
        ttl += line_instrument

    out_f.write(ttl)

if __name__ == "__main__":
    main()