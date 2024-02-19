# Information
Project: TPC1 - TTL Introduction <br>
Author: Alice Teixeira <br>
Date: 17/02/2024 <br>

# Project Report
## Introduction
This succint report aims to describe the developed work regarding the analysis of a json file, which compiles registry entries of portuguese flora plantations, and the creation of an appropriate ontology for it, as well as creating a script for the automatic population of it, resulting in a final .ttl file.

## 1. JSON Analysis - Initial analysis
The first step was analysing the json file (namely, the file 'plantas.json' inside this directory) with the intent to detect classes, data properties and object properties.

The ontology defined can be seen ilutrated in the picture below. The correlation between the original plantas.json file and the ontology created is presented in the table beneath it.

<img title="Ontology Diagram" alt="Ontology Diagram" src="rpcw_tpc1.drawio.png">

| plantas.json           	| Ontology: Class 	| Ontology: Data Property    	|
|------------------------	|-----------------	|---------------------------	|
| Id                     	| Register        	| id                        	|
| Número de Registo      	| Register        	| reg_number                	|
| Código de rua          	| Location        	| street_id                 	|
| Rua                    	| Location        	| street_name               	|
| Local                  	| Location        	| local                     	|
| Freguesia              	| Location        	| parish                    	|
| Espécie                	| Species         	| species_name              	|
| Nome Científico       	| Species         	| scientific_name           	|
| Origem                 	| Company         	| company_name              	|
| Data de Plantação      	| Plantation      	| date_plantation           	|
| Estado                 	| State           	| name_state                	|
| Caldeira               	| Plantation      	| planter                   	|
| Tutor                  	| Plantation      	| tutor                     	|
| Implantação            	| Plantation      	| plantation_type           	|
| Gestor                 	| Company         	| company_name              	|
| Data de actualização   	| Register        	| date_update               	|
| Número de intervenções 	| Register        	| numb_interventions        	|

In a quick note, in the same way 'State' was deemed as a separate class, the same could have been done for the data property 'plantation_type', being as it could have been viewed as categorical. However, it was not defined so due to the added complexity it would bring to the ontology and the uncertainty it would be appropriate. State was an examplar class between cases alike and similarly a prior exercise made in class.

## 2. Ontology creation
From the conceptual ontology in the previous section mentioned, it was created in Protegé the appropriate entities for it, which resulted in the file 'ontology_original.owl' in this directory.

Considering the lentghy file, questions regarding the population of the ontology arose alongside doubts over the coherence of the instances we would create by populating it with the data in 'plantas.json'.

## 3. JSON Analysis - Errors and Coherence search
Regarding the consistency of the original json, there was an emerging need to evaluate the data available.

A small script 'script_stat_analysis.py' was created, which partially analysed the data available. From it, several inconsistencies became apparent, a few which could be mitigated but not resolved; for example, data values were defined as 'a_identificar' in a way it could not be identified its true value. It was clear there would be missing and erroneous data if directly inserted the register entries into the ontology.

After analysing a few of those entries, there was a choice to make between fidelity to the original data and coherence between individuals in the ontology. The approach taken in this resolution is the later option, making a preferrence between coherent data 

## 4. Automation of ontology population
The creation of individuals of the ontology was automated by use of a python script, defined in the file 'script_tp1.py' in this same directory. This file iterates over each register entry and creates indiviuals for each class defined of the ontology in a phased way, its order being: creation of companies, creation of locations, scpecies, states, plantations, and lastly registers.

For the creation of companies, unspecified companies in the 'Gestor' and 'Origem' keys did not generate any company. Spaces were substituded by underscores.

For the creation of locations, it was used the 'Código de rua' key from the json file as part of the name of the individuals. Entries which could not transform their value of 'Código de rua' into integer had a placeholder '0' as their data property 'street_id', which creates a 'local_0' indivual repeatedly for entries with faulty id. This affects 17 entries in 29617 in total; these will be different from the original file and not necessarily correct.

For the creation of the species, the 'Nome Científico' key is used as the name of the indivuals created, and the characters " and . are given extra care as they were breaking the ontology in order to still be included in the file. There is however, a small percentage of entries which may differ between the original file and the ontology, due to empty and non-specific values.  

For the creation of states, states without any name are not created.

For the creation of plantations, there is a link of 1-to-1 to between register individuals and platation individuals, thus the key 'Id' is used to name the plantation individuals. There is also only specified the object property 'planted_by' if there is a specified company. Similiarly to previously mentioned 

For the creation of registers, the 'id' is used in the name of the indivuals. The number of interventions, if it cannot be transformed into an integer, is given the default value of 0.

In the end, the file 'added_ontology.owl' is created as the final, populated, ontology.

## Conclusion
Inconsistent register entries in the original json file are partially processed correctly in the approach taken, incorrectly populating the database in some cases. The amount of different individuals compared to the original entries are minimal, however, thus this was considered an approapriate resolution to the problem proposed.