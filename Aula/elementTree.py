import xml.etree.ElementTree as etree

tree = etree.parse('agenda.xml')
root = tree.getroot()
#root = tree.fromstring(country_data_as_string)

print(root.tag) #next element following the root, in the case of agenda.xml : element "agenda"
print(root.attrib) # attributes of the root
print(root.text) # textual component of the root; concacts text nodes of child elements

for child in root:   #access next branches
    print(child.text)

for entrada in root.iter('iter'):  #it is recursive through all the tree and gets all nodes 'iter'
    print(entrada.text)

for entrada in root.findall('iter'): # direct children; find('iter') returns only the first node it finds
    print(entrada.text)


# XPATH -> queries with component xml
for n in root.findall(".//node"):
    print(n.text)

#test 1
for entry in root.iter("entrada"):
    for camp in entry:
        print(camp.tag, camp.text)

#test 2
for entry in root.findall("entrada"):
    for camp in entry:
        print(camp.tag, camp.text)
    