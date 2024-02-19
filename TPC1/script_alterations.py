import json
import sys
import shutil

def main():
    #json reading
    f = open("./TPC1/plantas.json")
    bd = json.load(f)
    f.close()

    f = open("./TPC1/alterations.json")

    #ttl creation
    ttl = ""

    companies_set, locations_set, species_set, state_set = set(), set(), set(), set()


    ttl += """
    #################################################################
    #    Individuals
    #################################################################
    """

    for reg in bd:

        ### verify and possibly create companies (by 'Origem')
        new_origin = str(reg['Origem']).replace(' ', '_')
        if new_origin not in companies_set and new_origin != "":
            company_creation = f"""
            ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#{new_origin}
            :{new_origin} rdf:type owl:NamedIndividual ,
                            :Company ;
                    :company_name "{new_origin}"^^xsd:string .
            """
            companies_set.add(new_origin)
            ttl += company_creation

        ### verify and possibly create companies (by 'Gestor')
        new_gestor = str(reg['Gestor']).replace(' ', '_')
        if new_gestor not in companies_set and new_gestor != "":
            company_creation = f"""
            ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#{new_gestor}
            :{new_gestor} rdf:type owl:NamedIndividual ,
                            :Company ;
                    :company_name "{new_gestor}"^^xsd:string .
            """
            companies_set.add(new_gestor)
            ttl += company_creation
        
        
        ### verify and possibly create locations (by 'Código de rua')
        try:
            new_code = int(reg['Código de rua'])
        except:
            new_code = 0

        new_freguesia = str(reg['Freguesia']).replace(' ', '_')
        new_local = str(reg['Local']).replace(' ', '_')
        new_street_name = str(reg['Rua']).replace(' ', '_').replace('"','\\"')

        if new_code not in locations_set and new_code != 0:
            location_creation = f"""
            ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#local_{new_code}
            :local_{new_code} rdf:type owl:NamedIndividual ,
                        :Location ;
            :street_id "{new_code}"^^xsd:int ;
            :parish "{new_freguesia}"^^xsd:string ;
            :local "{new_local}"^^xsd:string ;
            :street_name "{new_street_name}"^^xsd:string .
            """
            locations_set.add(f"local_{new_code}")
            ttl += location_creation
        

        
        ### verify and possibly create species (by 'Nome Científico')
        new_name = str(reg['Nome Científico']).replace(' ', '_')
        new_species = str(reg['Espécie']).replace(' ', '_')

        if new_name not in species_set and new_name != "":
            plant_creation = f"""
            ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#{new_name}
            :{new_name} rdf:type owl:NamedIndividual ,
                            :Species ;
                    :species_name "{new_species}"^^xsd:string ;
                    :scientific_name "{new_name}"^^xsd:string .
            """
            species_set.add(new_name)
            ttl += plant_creation
        

        
        ### verify and possibly create states (by 'Estado')
        if reg['Estado'] not in state_set and reg['Estado'] != "":
            state_creation = f"""
            ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#{reg['Estado']}
            :{reg['Estado']} rdf:type owl:NamedIndividual ,
                    :Estado ;
            :name_state "{reg['Estado']}"^^xsd:string .
            """
            state_set.add(reg['Estado'])
            ttl += state_creation

        '''
        ### supposing each register has a single unique plantation
        ### aka always a creation of a plantation for a register
        plantation_creation = f"""
        ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#plantation_{reg['Id']}
        :plantation_{reg['Id']} rdf:type owl:NamedIndividual ,
                     :Plantation ;
            :planted_by :{new_origin} ;
            :is_state :{reg['Estado']} ;
            :made_of :{new_name} ;
            :planter "{reg['Caldeira']}"^^xsd:string ;
            :date_plantation "{reg['Data de Plantação']}"^^xsd:dateTime ;
            :plantation "{reg['Implantação']}"^^xsd:string ;
            :tutor "{reg['Tutor']}"^^xsd:string .
        """
        ttl += plantation_creation

        
        ### creation of the register
        regist_creation = f"""
        ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#regist_{reg['Gestor']}
        :regist_{reg['Gestor']} rdf:type owl:NamedIndividual ,
                   :Register ;
          :managed_by :{reg['Gestor']} ;
          :located_in :{reg['Código de rua']} ;
          :has_a :plantation_{reg['Id']} ;
          :date_update "{reg['Data de actualização']}"^^xsd:dateTime ;
          :numb_interventions "{reg['Número de intervenções']}"^^xsd:int ;
          :reg_number "{reg['Número de Registo']}"^^xsd:int ;
          :id "{reg['Id']}"^^xsd:int .
        """
        ttl += regist_creation
        '''

    out_f.write(ttl)

if __name__ == "__main__":
    main()