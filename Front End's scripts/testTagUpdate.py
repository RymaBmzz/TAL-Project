import xml.etree.cElementTree as et
from xml.etree.cElementTree import parse
from bs4 import BeautifulSoup
import re
from cleaning import removingTachkil
from exemplesRetrieval import initializingJar,lemmatize
import unicodedata
import pickle


def get_phrase(phrase,lemmedlist,word):
    taille = len(lemmedlist)-1
    ideb=ifin=0
    index=lemmedlist.index(word)
    if index > 4 :
        ideb= index - 4
        if taille - index > 6:
            ifin=index+6
            newPhrase = phrase[ideb:ifin]
        else:
            newPhrase = phrase[ideb:]
    else:
        ideb=0
        if taille - index > 6:
            ifin=index+6
            newPhrase = phrase[ideb:ifin]
        else:
            newPhrase = phrase[ideb:]
    return " ".join(newPhrase)

def load_dictionary(name):
    dit = {}
    with open(name, 'rb') as f2:
        dit = pickle.load(f2)
    return dit

def get_numL_dictXML(word):
    numdict=[]
    dict_letters = {1: ['أ', 'إ', 'ئ', 'ؤ', 'ء', 'ا','أَ','آ'], 2: ['ﺏ', 'ﺑـ'], 3: ['ﺗـ', 'ﺕ'], 4: ['ﺛـ', 'ﺙ'], 5: ['ﺝ', 'ﺟـ'],
                    6: ['ﺣـ', 'ﺡ'], 7: ['ﺧـ', 'ﺥ'], 8: ['ﺩ', 'ﺩـ'], 9: ['ﺫ', 'ﺫـ'],
                    10: ['ﺭ'], 11: ['ﺯ'], 12: ['ﺳـ', 'ﺱ'], 13: ['ﺵ', 'ﺷـ'], 14: ['ﺻـ', 'ﺹ'], 15: ['ﺽ', 'ﺿـ'],
                    16: ['ﻁ', 'ﻃـ'], 17: ['ﻇـ', 'ﻅ'], 18: ['ﻉ', 'ﻋـ'],
                    19: ['ﻍ', 'ﻏـ'], 20: ['ﻓـ', 'ﻑ'], 21: ['ﻕ', 'ﻗـ'], 22: ['ﻙ', 'ﻛـ'], 23: ['ﻝ', 'ﻟـ'],
                    24: ['ﻡ', 'ﻣـ'], 25: ['ﻥ', 'ﻧـ'], 26: ['ﻩ', 'ﻫـ'], 27: ['ﻭ', 'ﻭـ'], 28: ['ﻱ', 'ﻳـ']}

    numdict = ([k for k in dict_letters.keys() for c in dict_letters[k] if
                unicodedata.normalize('NFKD', c).casefold() == unicodedata.normalize('NFKD', word[0]).casefold()])
    if len(numdict) <1 or numdict[0] not in range(1,29):
        return -1
    print(numdict)
    return numdict

#add an entry to the dict MODE MANUEL
#textdef est une liste des definitions entrées par le lexicographe
#dictExemple: dictionnaire keys= {1 à 7 } représentant el asr, et dictExemple[key]=exemple associé à el Asr key
#namebalise: word ajouté par lexicographe
 
def add_entryToDict(textdef,namebalise,dictExemple):

    object = initializingJar() #de préférence mettre cette instruction une seule fois fel main hors de cette fonctin

    namebalise = removingTachkil(namebalise)
    namebal = lemmatize(object, namebalise)
    numdict = get_numL_dictXML(namebal[0])  # get indice of the dict corresponding to the letter that starts with
    nb=numdict[0]
    xmlfile="Dicts/HistDictionary"+str(nb)
    tree = parse(xmlfile + ".xml")
    namebalise = namebal[0]
    w = tree.findall("./word[@name='"+namebalise+"']")
    asr_name = {'1': 'pre-islamic', '2': 'islamic', '3': 'umayyad', '4': 'abbasid',
                    '5': 'middle_ages','6': 'modern', '7': 'quran'}
    root = tree.getroot()
    if(len(w)==0):
        word = et.SubElement(root,"word",name=namebalise,value="valid")
        definition = et.SubElement(word, "Definitions")
        co=0
        for i in textdef:
            co+=1
            defi = et.SubElement(definition,"def"+str(co),name="lexicographe")
            defi.text = i
        context = et.SubElement(word, "Exemples")
        for el in dictExemple.keys():
            asr=asr_name[el]
            balise_sample = et.SubElement(context, asr)
            balise_sample.text = dictExemple[el]

    else:
#        print("wwww ",w[0])
        root.remove(w[0]) #supprimer <word > de notre dict
        word = et.SubElement(root, "word", name=namebalise, value="valid")
        definition = et.SubElement(word, "Definitions")
        co = 0
        for i in textdef:
            co += 1
            defi = et.SubElement(definition, "def" + str(co), name="lexicographe")
            defi.text = i
        context = et.SubElement(word, "Exemples")
        for el in dictExemple.keys():
            asr = asr_name[el]
            balise_sample = et.SubElement(context, asr)
            balise_sample.text = dictExemple[el]


    tree.write(xmlfile+".xml", encoding="UTF-8", xml_declaration=True)
    print ("saving done")

#for updating state of the word in the dict MODE AUTOMATIQUE
#Handler du bouton VALIDER l'entrée du dict
def validate_word(namebalise):
    object = initializingJar()  # de préférence mettre cette instruction une seule fois fel main hors de cette fonctin

    namebalise = removingTachkil(namebalise)
    namebal = lemmatize(object, namebalise)
    numdict = get_numL_dictXML(namebal[0])  # get indice of the dict corresponding to the letter that starts with
    nb = numdict[0]
    xmlfile = "Dicts/HistDictionary" + str(nb)
    tree = parse(xmlfile + ".xml")
    w = tree.findall("./word[@name='"+namebal[0]+"']")
    w[0].set("value","valid")
    tree.write(xmlfile+".xml", encoding="UTF-8", xml_declaration=True)

    # listElement = w[0].getchildren()
    # w[0].remove(listElement[0])
    # root=tree.getroot()
    # root.remove(w[0])
    # tree.write("xmlTrial.xml", encoding="UTF-8", xml_declaration=True)

#update def automatique ou contexte
def update_wordXml(namebalise,):
    object = initializingJar()  # de préférence mettre cette instruction une seule fois fel main hors de cette fonctin

    namebalise = removingTachkil(namebalise)
    namebal = lemmatize(object, namebalise)
    numdict = get_numL_dictXML(namebal[0])  # get indice of the dict corresponding to the letter that starts with
    nb = numdict[0]
    xmlfile = "Dicts/HistDictionary" + str(nb)
    tree = parse(xmlfile + ".xml")
    w = tree.findall("./word[@name='" + namebal[0] + "']")

    listElement = w[0].getchildren()
    w[0].remove(listElement[0])

# textdef=['def1 this','def 2 this','3def this']
# namebalise="طاب"
# dictExemple={'6':"exemple de assr modern",'2':"exemple de assr islamic"}
# add_entryToDict(textdef,namebalise,dictExemple)
#validate_word(namebalise)


def get_definition_from_dict(w):
    object = initializingJar()
    namebalise = removingTachkil(w)
    namebal = lemmatize(object, w)
    keyword=namebal[0]
    numdict = get_numL_dictXML(keyword)  # get indice of the dict corresponding to the letter that starts with
    nb = numdict[0]
    xmlfile = "Dicts/HistDictionary" + str(nb)
    tree = parse(xmlfile + ".xml")
    w = tree.findall("./word[@name='"+keyword+"']") #trouver la balise correspondante au mot cherché
    #get_examples_from_dict(w)
    examples={}
    children = w[0].getchildren()
    Definitions = children[0]
    Defs = []
    Dicts = Definitions.getchildren()
    print(len(Dicts))  # nbr de dictionnaire pour ce mot
    for defdict in Dicts:  # on boucle sur les dictionnaires de cette entrée
        print("\n****Nom du Dictionnaire****\n", defdict.get("name"))
        defi = defdict.getchildren()
        for c in defi:  # on boucle sur nombre de definition pour ce dictionnaire
            Defs.append(c.text)
            print(c.text)
    return Defs
def get_examples_from_dict(w):
    # namebalise = removingTachkil(w)
    # namebal = lemmatize(object, w)
    # keyword = namebal[0]
    numdict = get_numL_dictXML(w)  # get indice of the dict corresponding to the letter that starts with
    nb = numdict[0]
    children = w[0].getchildren()
    Exemples = children[1]
    contextes = Exemples.getchildren()
    for asr in contextes:  # on boucle sur les périodes (3ossor)
        print ("\n**** Asr ****\n",asr.tag)
        asrsamples = asr.getchildren()
        for c in asrsamples:  # on boucle sur les exemples de ce asr
            print (c.text) #affiche None si y a pas d'exemples pour ce Asr

def get_examples_from_contexte(keyword,object,dictPreIslamic,dictIslamic,dictUmayyad,dictMiddleAges,dictAbbasid,dictModern,dictQuran):
    # dictPreIslamic = load_dictionary("Contexts/contextPreIslamic.pkl")
    # print("one loaded")
    # dictIslamic = load_dictionary("Contexts/contextIslamic.pkl")
    # print("two loaded")
    # dictUmayyad = load_dictionary("Contexts/contextUmayyad.pkl")
    # print("three loaded")
    # dictAbbasid = load_dictionary("Contexts/contextAbbasid.pkl")
    # print("four loaded")
    # dictMiddleAges = load_dictionary("Contexts/contextMiddleAges.pkl")
    # print("five loaded")
    # dictModern = load_dictionary("Contexts/contextModern.pkl")
    # print("six loaded")
    # dictQuran = load_dictionary("Contexts/contextQuran.pkl")
    # print("quran loaded")

    asr1=dictPreIslamic[keyword]
    asr2=dictIslamic[keyword]
    asr3=dictUmayyad[keyword]
    asr4=dictMiddleAges[keyword]
    asr5=dictAbbasid[keyword]
    asr6=dictModern[keyword]
    asr7=dictQuran[keyword]
    #avant d'afficher les examples qui sont les elements de chaque liste de asr, tester si la longueur exemple<20 afficher sinon ignorer
    dict_exemples={1:asr1,2:asr2,3:asr3,4:asr4,5:asr5,6:asr6,7:asr7}

    for i in range(1,8):
        c=0
        temp=[]
        for exp in dict_exemples[i]:
            if c >3:
                break
            c+=1
            if len(exp) < 20:
                temp.append(exp)
            else:
                lemphrase = lemmatize(object, exp)
                ph = get_phrase(exp.split(), lemphrase, keyword)
                temp.append(ph)
        dict_exemples[i]=temp

    return dict_exemples #ou faire l'affichage dans cette boucle si tu veux pas recuperer dict

# def affiche_word(namebalise):
    # object = initializingJar()  # de préférence mettre cette instruction une seule fois fel main hors de cette fonctin
    #
    # namebalise = removingTachkil(namebalise)
    # namebal = lemmatize(object, namebalise)
    # keyword=namebal[0]
    # numdict = get_numL_dictXML(keyword)  # get indice of the dict corresponding to the letter that starts with
    # nb = numdict[0]
    # xmlfile = "Dicts/HistDictionary" + str(nb)
    # tree = parse(xmlfile + ".xml")
    # w = tree.findall("./word[@name='"+keyword+"']") #trouver la balise correspondante au mot cherché
    # get_definition_from_dict(w)
    # #get_examples_from_dict(w)
    # examples={}
    # examples=get_examples_from_contexte(keyword,object)
    # for (k,v) in examples.items():
    #     print ("asr= ",k,"value: ",v)
    # return examples

# namebalise="طاب"
# affiche_word(namebalise)
# object = initializingJar()
#
# mot="طاب"
#
# defs = get_definition_from_dict(mot)
