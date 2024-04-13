import json
import shutil

def main(ontologyFromFile, ontologyTtoFile, populateFile):
    
    f = open(populateFile)
    database = json.load(f)
    f.close()

    shutil.copyfile(ontologyFromFile, ontologyTtoFile)
    out_f = open(ontologyTtoFile, "a")

    ttl = ""

    for register in database:
        idALuno = str(register['idAluno'])
        nomeAluno = str(register['nome'])
        cursoAluno = str(register['curso'])

        list_tpc = register['tpc']

        for tpc in list_tpc:
            pass

        projetoAluno = register['projeto']

        list_exames = register['exames']
        for exame in list_exames:
            pass

        


if __name__ == "__main__":
    fromFile = "FichaAfericao/Ex1/fichaAf_alunos_OG.ttl"
    toFile = "FichaAfericao/Ex1/fichaAf_alunos.ttl"
    populateFile = "FichaAfericao/Ex1/aval-alunos.json"
    main(fromFile, toFile, populateFile)