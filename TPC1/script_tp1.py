import json
import sys
import shutil

def main():
    #json reading
    f = open("./TPC1/plantas.json")
    bd = json.load(f)
    f.close()

    shutil.copyfile("./TPC1/ontology_original.owl", "./TPC1/added_ontology.owl")
    out_f = open("./TPC1/added_ontology.owl", "a")

    #ttl creation
    ttl = ""

    companies_set, locations_set, species_set, state_set = set(), set(), set(), set()
    loc_id = set()


    ttl += """
    #################################################################
    #    Individuals
    #################################################################
    """

    for reg in bd:
        
        ### verify and possibly create companies (by 'Origem')
        new_origin = str(reg['Origem']).replace(' ', '_')
        # ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#{new_origin}
        if new_origin not in companies_set and new_origin != "":
            company_creation = f"""
            :{new_origin} rdf:type owl:NamedIndividual ,
                            :Company ;
                    :company_name "{new_origin}"^^xsd:string .
            """
            companies_set.add(new_origin)
            ttl += company_creation

        ### verify and possibly create companies (by 'Gestor')
        new_gestor = str(reg['Gestor']).replace(' ', '_')
        # ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#{new_gestor}
        if new_gestor not in companies_set and new_gestor != "":
            company_creation = f"""
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

        new_freguesia = str(reg['Freguesia']).replace(' ', '_').replace('"','\\"')
        new_local = str(reg['Local']).replace(' ', '_').replace('"','\\"')
        new_street_name = str(reg['Rua']).replace(' ', '_').replace('"','\\"')
        # ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#local_{new_code}

        if f"local_{new_code}" not in locations_set and new_code != "local_0":
            location_creation = f"""
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
        new_name = str(reg['Nome Científico']).replace(' ', '_').replace('"','\\"').replace('.','\\.')
        new_species = str(reg['Espécie']).replace(' ', '_').replace('"','\\"').replace('.','\\.')

        #  ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#{new_name}
        if new_name not in species_set and new_name != "":
            plant_creation = f"""
            :{new_name} rdf:type owl:NamedIndividual ,
                            :Species ;
                    :species_name "{new_species}"^^xsd:string ;
                    :scientific_name "{new_name}"^^xsd:string .
            """
            species_set.add(new_name)
            ttl += plant_creation
        
        
        
        ### verify and possibly create states (by 'Estado')
        # ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#{reg['Estado']}
        if reg['Estado'] not in state_set and reg['Estado'] != "":
            state_creation = f"""
            :{reg['Estado']} rdf:type owl:NamedIndividual ,
                    :State ;
            :name_state "{reg['Estado']}"^^xsd:string .
            """
            state_set.add(reg['Estado'])
            ttl += state_creation


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

        '''
        ### creation of the register
        regist_creation = f"""
        ###  http://www.semanticweb.org/avt/ontologies/2024/1/untitled-ontology-3#regist_{reg['Gestor']}
        :regist_{reg['Gestor']} rdf:type owl:NamedIndividual ,
                   :Register ;
          :managed_by :{new_gestor} ;
          :located_in :local_{new_code} ;
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