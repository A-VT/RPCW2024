# READ ME

this is a temporaty README. It will be later revamped to its final form.

TO DO:
- [x] Get the original data from DBPedia (redo TPC5 work)
    - 30000 films, each with a list of directors, producers, music composers and actors associated. The resulting file is data.json in the directory data; the directory dbQuerying stores the scripting files which were used to create data.json. Threading was finally used.
- [x] Create ontology
    - file ontology_original_turtle.ttl is the original
- [ ] Populate the ontology
    - population using the file populate_script.py in the directory populate_ttl; output is populated.ttl.
- [ ] Put the populated ontology in a repository in the professor's given endpoint
- [ ] Do the couple of queries asked
- [ ] Webpages and server using flask to showcase the database's data
    - Flask server done;


