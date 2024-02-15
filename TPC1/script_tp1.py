import json


def main():
    #json reading
    f = open("plantas.json")
    bd = json.load(f)
    f.close()

    #ttl creation
    ttl = ""

    companies_set, locations_set, species_set, state_set = {}, {}, {}, {}


    for reg in bd:

        ### verify and possibly create companies (by 'Origem')
        if reg['Origem'] not in companies_set and reg['Origem'] != "":
            company_creation = f"""
            :{reg['Origem']} rdf:type owl:NamedIndividual ,
                            :Company ;
                    :company_name "{reg['Origem']}"^^xsd:string .
            """
            companies_set.add(reg['Origem'])
            ttl += company_creation


        ### verify and possibly create companies (by 'Gestor')
        if reg['Gestor'] not in companies_set and reg['Gestor'] != "":
            company_creation = f"""
            :{reg['Gestor']} rdf:type owl:NamedIndividual ,
                            :Company ;
                    :company_name "{reg['Gestor']}"^^xsd:string .
            """
            companies_set.add(reg['Gestor'])
            ttl += company_creation
        

        ### verify and possibly create locations (by 'Código de rua')
        if reg['Código de rua'] not in locations_set and reg['Código de rua'] != "":
            location_creation = f"""
            :{reg['Código de rua']} rdf:type owl:NamedIndividual ,
                        :Location ;
            :street_id "{reg['Código de rua']}"^^xsd:int ;
            :parish "{reg['Freguesia']}"^^xsd:string ;
            :local "{reg['Local']}"^^xsd:string ;
            :street_name "{reg['Rua']}"^^xsd:string .
            """
            locations_set.add(reg['Código de rua'])
            ttl += location_creation
        

        ### verify and possibly create species (by 'Nome Científico')
        if reg['Nome Científico'] not in species_set and reg['Nome Científico'] != "":
            plant_creation = f"""
            :{reg['Nome Científico']} rdf:type owl:NamedIndividual ,
                            :Species ;
                    :species_name "{reg['Espécie']}"^^xsd:string ;
                    :scientific_name "{reg['Nome Científico']}"^^xsd:string .
            """
            species_set.add(reg['Nome Científico'])
            ttl += plant_creation

        ### verify and possibly create states (by 'Estado')
        if reg['Estado'] not in state_set and reg['Estado'] != "":
            company_creation = f"""
            :{reg['Estado']} rdf:type owl:NamedIndividual ,
                    :Estado ;
            :name_state "{reg['Estado']}"^^xsd:string .
            """
            state_set.add(reg['Estado'])
            ttl += plant_creation
        
        ### verify and possibly create plantations (by 'Origem')
        if reg['Origem'] not in companies_set and reg['Origem'] != "":
            company_creation = f"""
            :{reg['Origem']} rdf:type owl:NamedIndividual ,
                            :Company ;
                    :company_name "{reg['Origem']}"^^xsd:string .
            """
            companies_set.add(reg['Origem'])
            ttl += company_creation


        ### supposing each register has a single unique plantation
        ### aka always a creation of a plantation for a register
        plantation_creation = f"""
        :plantation_{reg['Id']} rdf:type owl:NamedIndividual ,
                     :Plantation ;
            :planted_by :{reg['Origem']} ;
            :is_state :{reg['Estado']} ;
            :made_of :{reg['Nome Científico']} ;
            :planter "{reg['Caldeira']}"^^xsd:string ;
            :date_plantation "{reg['Data de Plantação']}"^^xsd:dateTime ;
            :plantation "{reg['Implantação']}"^^xsd:string ;
            :tutor "{reg['Tutor']}"^^xsd:string .
        """
        ttl += plantation_creation

        ### creation of the register
        regist_creation = f"""
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


    print(ttl)

if __name__ == "__main__":
    main()