import json

f = open("./TPC2/db.json")
bd = json.load(f)
f.close()


f = open("db2.json", "w",encoding='utf-8')

alunos = bd["alunos"]
cursos = bd["cursos"]
instrumentos = bd["instrumentos"]

print(f"Number regs of alunos: {len(alunos)}")
print(f"Number regs of cursos: {len(cursos)}")
print(f"Number regs of instrumentos: {len(instrumentos)}")

dic_og_instrumentos = {}

#### Instrumento & Cursos
#{'I1': 'Clarinete',...}
dic_inst = {instrumento['id']: instrumento['#text'] for instrumento in instrumentos}
print(f"dic_inst: {dic_inst}")
print('\n')

dic_og_cursos = {}
for curso in cursos:
    instrumento_id = curso['instrumento']['id']
    instrumento_text = curso['instrumento']['#text']
    
    if instrumento_id not in dic_og_cursos:
        dic_og_cursos[instrumento_id] = instrumento_text
print(f"dic_og_cursos: {dic_og_cursos}")

if dic_inst == dic_og_cursos:
    print("\nNo inconsistencies between Cursos and Instrumentos.")
else:
    print("\nThe are inconsistencies.")

print('\n')
print(cursos)



#### Cursos & Alunos
dic_cursos_2 = {}
for curso in cursos:
    curso_id = curso['id']
    instrumento_id = curso['instrumento']['id']
    instrumento_text = curso['instrumento']['#text']
    #dic_cursos_2[curso_id] = {instrumento_id: instrumento_text}
    dic_cursos_2[curso_id] = instrumento_text
#print(dic_cursos_2)

#print("\n")
#print(alunos)
print("\n")
dic_alunos = {}
for aluno in alunos:
    dic_alunos[aluno['curso']] = aluno['instrumento']
#print(dic_alunos)

in_alunos = {}
for curso in dic_alunos:
    if curso not in dic_cursos_2:
        in_alunos[curso] = dic_alunos[curso]
print(f"\nEntries in dic_alunos but not in dic_cursos_2: {in_alunos}")


### CORRECTION:
for aluno in alunos:
    instrumento = aluno["instrumento"]
    curso = aluno["curso"]
    for cur in cursos:
        if(instrumento == cur["instrumento"]["#text"]):
            if curso[:2]== cur["id"][:2] and curso[2:]!= cur["id"][2:]:
                aluno["curso"] = cur["id"]


jsonDump = {
    "alunos":alunos,
    "cursos": cursos,
    "instrumentos": instrumentos
}

json.dump(jsonDump,f,indent=4,ensure_ascii=False)
f.close()