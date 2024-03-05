import json
import shutil

def main():
    f = open("./TPC3/mapa-virtual.json")
    data = json.load(f)
    f.close()

    shutil.copyfile("./TPC3/ontology.ttl", "./TPC3/populated_ontology.ttl")
    out_f = open("./TPC3/populated_ontology.ttl", "a",encoding='utf-8')
    ttl = ""

    cities = data["cidades"]
    connections = data["ligacoes"]
    
    dicOr = {}
    dicDe = {} #city : [ligname1, ligname2, ...]
    for index, con in enumerate(connections):
        
        Or = con["origem"]
        De = con["destino"]
        if Or not in dicOr:
            dicOr[Or] = [f"lig{index}"]
        else:
            dicOr[Or].append(f"lig{index}")
        if De not in dicDe:
            dicDe[De] = [f"lig{index}"]
        else:
            dicDe[De].append(f"lig{index}")

        
###  http://rpcw.di.uminho.pt/2024/mapa-virtual#lig{index}
        line = f"""
:lig{index} rdf:type owl:NamedIndividual ,
               :Ligacao ;
      :idLigacao "lig{index}"^^xsd:string ;
      :distancia "{con["distância"]}"^^xsd:float.
        """
        ttl += line
    
    #^^xsd:string
    #^^xsd:float


    print(dicOr)
    print("\n")
    print(dicDe.keys())
    for index, cit in enumerate(cities):
        str = f"{cit['id']}"
        strOr = ""
        strDe = ""

        if str in dicOr:
            temOrig = dicOr[str]
            for o in temOrig:
                strOr += f":tem_origem :{o};\n\t"

        if str in dicDe:
            temDest = dicDe[str]
            for o in temDest:
                strDe+= f":tem_destino :{o};\n\t"
        
        cid = cit["id"]

###  http://rpcw.di.uminho.pt/2024/mapa-virtual#{cid}
        line = f"""
:{cid} rdf:type owl:NamedIndividual ,
               :Cidade ;
      {strOr}
      {strDe}
      :nome "{cit["nome"]}"^^xsd:string ;
      :populacao "{cit["população"]}"^^xsd:int ;
      :descrição "{cit["descrição"]}"^^xsd:string ;
      :distrito "{cit["distrito"]}"^^xsd:string .
        """
        ttl += line

    #^^xsd:string
    #^^xsd:int
    #^^xsd:string
    #^^xsd:string

    out_f.write(ttl)


if __name__ == "__main__":
    main()