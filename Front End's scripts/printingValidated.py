from  xml.etree.cElementTree import parse

# words only

#for nb in range(1,29):
#    xmlfile = "Dicts/HistDictionary" + str(nb)
#    print("xml file => ",xmlfile)
#    tree = parse(xmlfile + ".xml")
#    w = tree.findall("./word[@value='validated']")
#    validated_entry=[el.get("name") for el in w if len(w)>0]
#    print(validated_entry)


# with def

for nb in range(1,29):
    xmlfile = "Dicts/HistDictionary" + str(nb)
    print("xml file => ",xmlfile)
    tree = parse(xmlfile + ".xml")
    w = tree.findall("./word[@value='validated']")
    validated_entry=[(el.get("name"),el.getchildren()[0].getchildren()[0].getchildren()[0].text) for el in w if len(w)>0]
    print(validated_entry)