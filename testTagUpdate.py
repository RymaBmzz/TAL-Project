import xml.etree.cElementTree as et
from  xml.etree.cElementTree import parse
from bs4 import BeautifulSoup
import re
tree = parse("HistDictionary.xml")
#root = et.fromstring("HistDictionary.xml")
w = tree.findall("./word[@name='ryma']")
w[0].set("value","validated")
tree.write("HistDictionary.xml", encoding="UTF-8", xml_declaration=True)
