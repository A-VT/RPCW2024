import json
import sys

def perc_affected(total,affected):
    return (affected*100)/total

def main():
    #json reading
    f = open("./TPC1/plantas.json")
    bd = json.load(f)
    f.close()

    state_lst, caldeira_lst, tutor_lst, reg_n, lst_code_street = [], [], [], [], []
    species_dic  = {}
    rept_reg_n = 0

    stat_f = open("./TPC1/stat_analysis_file.txt", "w")
    stat_f.write(f"The json file has {len(bd)} registry entries.")

    for reg in bd:

        # 1. Analysis of repetition of 'Número de registo'
        if (reg["Número de Registo"] not in reg_n):
            reg_n.append(reg["Número de Registo"])
        else:
            rept_reg_n += 1
        
        # 2. Analysis of 'Estado'
        if(reg["Estado"] not in state_lst):
            state_lst.append(reg["Estado"])

        # 3. Analysis of 'Caldeira'
        if(reg["Caldeira"] not in caldeira_lst):
            caldeira_lst.append(reg["Caldeira"])
        
        # 4. Analysis of 'Tutor'
        if(reg["Tutor"] not in tutor_lst):
            tutor_lst.append(reg["Tutor"])

        # 5. Analysis of 'Código de rua' -> non integer values
        try:
            int(reg["Código de rua"])
            if (int(reg["Código de rua"]) == 0):
                print("There is a streetcode equal to 0.")
        except:
            lst_code_street.append((reg["Código de rua"], type(reg["Código de rua"])))


        # 6. Analysis of 'Nome Científico' e 'Espécie'
        species = str(reg['Nome Científico']).replace(' ', '_')
        species_name = str(reg['Espécie']).replace(' ', '_')
        # {species1: [{species_name1: 1, {species_name2: 3}; species2: {species_name1: 7}}
        if(species not in species_dic):
            species_dic[species] = { species_name : 1 }
        else: #species already registered
            names = species_dic[species]
            if species_name not in species_dic[species]:
                names[species_name] = 1
            else:
                names[species_name] += 1

    
    stat_f.write(f"The json file has {len(bd)} registry entries.")
    stat_f.write("Now the file has more content!\n")
    stat_f.write(f"Register number repeats {rept_reg_n} times!\n") if rept_reg_n>0 else next
    stat_f.write(f"Number of States: {len(state_lst)} | States: {state_lst}\n")
    stat_f.write(f"Number of Caldeira: {len(caldeira_lst)} | Caldeira: {caldeira_lst}\n")
    stat_f.write(f"Number of Tutor: {len(tutor_lst)} | Tutor: {tutor_lst}\n")
    stat_f.write(f"Number of Species: {len(species_dic)}\n")
    stat_f.write(f"{len(lst_code_street)} Annormal code_streets: {lst_code_street}\n")
    stat_f.write(f"Species: {species_dic}\n")

    i = 0
    for s in species_dic.values():
        if len(s) > 1:
            i+= 1

    stat_f.write(f"Number of species with more than 1 name: {i}\n")
    stat_f.close()

if __name__ == "__main__":
    main()