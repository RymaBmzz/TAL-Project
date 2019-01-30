import os
import pickle
import threading
import unicodedata
from threading import Thread
from time import sleep
from bs4 import BeautifulSoup
import subprocess
import sqlite3
from collections import defaultdict
from sqlite3 import Error
from  xml.etree.cElementTree import parse
import cleaning as cl
from exemplesRetrieval import initializingJar,lemmatize
import xml.etree.cElementTree as et
from cleaning import removingTachkil

def get_description(tree):
    desc = ['author','asr','title']
    temp=[]
    for info in desc:
        for item in tree.findall('.//'+info):
            #print(item.text)
            temp.append(item.text)
    #print ("*********************")
    return temp

def getContextIslamic(wordLemme):
    path = "corpusXml/islamic"
    #wordLemme = lemmatize(object, word)
    global data2
    global metadata2
    data2 = []
    metadata2=[]
    for cat in os.listdir(path):
        for subdir in os.listdir(path + "/" + cat):
            for file in os.listdir(path + "/" + cat + "/" + subdir):
                try:
                    tree = parse(path + "/" + cat + "/" + subdir + "/" + file)
                except BaseException as Exception:
                    continue
                metadata2.append(get_description(tree))
                for item in tree.findall('.//phrase'):
                    phrase = item.text
                    li = lemmatize(object, phrase)
                    for w in li:
                        if unicodedata.normalize('NFKD', w).casefold() == unicodedata.normalize('NFKD', wordLemme[0]):
                            data2.append(phrase)
                            if len(data2) > 6:
                                return
    print ("islamic done")
    return


def getContextUmayyad(wordLemme):
    path = "corpusXml/umayyad"
    # wordLemme = lemmatize(object, word)
    global data3
    global metadata3
    metadata3=[]
    data3 = []
    for cat in os.listdir(path):
        for subdir in os.listdir(path + "/" + cat):
            for file in os.listdir(path + "/" + cat + "/" + subdir):
                try:
                    tree = parse(path + "/" + cat + "/" + subdir + "/" + file)
                except BaseException as Exception:
                    continue
                metadata3.append(get_description(tree))
                for item in tree.findall('.//phrase'):
                    phrase = item.text
                    li = lemmatize(object, phrase)
                    for w in li:
                        if unicodedata.normalize('NFKD', w).casefold() == unicodedata.normalize('NFKD', wordLemme[0]):
                            data3.append(phrase)
                            if len(data3) > 6:
                                return
    print ("umayyad")
    return


def getContextAbbasid(wordLemme):
    path = "corpusXml/abbasid"
    # wordLemme = lemmatize(object, word)
    global data4
    global metadata4
    data4 = []
    metadata4=[]
    for cat in os.listdir(path):
        for subdir in os.listdir(path + "/" + cat):
            for file in os.listdir(path + "/" + cat + "/" + subdir):
                try:
                    tree = parse(path + "/" + cat + "/" + subdir + "/" + file)
                except BaseException as Exception:
                    continue
                metadata4.append(get_description(tree))
                for item in tree.findall('.//phrase'):
                    phrase = item.text
                    li = lemmatize(object, phrase)
                    for w in li:
                        if unicodedata.normalize('NFKD', w).casefold() == unicodedata.normalize('NFKD', wordLemme[0]):
                            data4.append(phrase)
                            if len(data4) > 6:
                                return
    print ("abassid done")
    return


def getContextMiddleAges(wordLemme):
    path = "corpusXml/middle-ages"
    # wordLemme = lemmatize(object, word)
    global data5
    global metadata5
    data5 = []
    metadata5=[]
    for cat in os.listdir(path):
        for subdir in os.listdir(path + "/" + cat):
            for file in os.listdir(path + "/" + cat + "/" + subdir):
                try:
                    tree = parse(path + "/" + cat + "/" + subdir + "/" + file)
                except BaseException as Exception:
                    continue
                metadata5.append(get_description(tree))
                for item in tree.findall('.//phrase'):
                    phrase = item.text
                    li = lemmatize(object, phrase)
                    for w in li:
                        if unicodedata.normalize('NFKD', w).casefold() == unicodedata.normalize('NFKD', wordLemme[0]):
                            data5.append(phrase)
                            if len(data5) > 6:
                                return
    print ("middle ages done")
    return


def getContextQuran(wordLemme):
    path = "corpusXml/quran"
    # wordLemme = lemmatize(object, word)
    global data7
    global metadata7
    data7 = []
    metadata7=[]
    for sourat in os.listdir(path):
        try:
            tree = parse(path + "/" + sourat)
        except BaseException as Exception:
            continue
        metadata7.append(get_description(tree))
        for item in tree.findall('.//aya'):
            phrase = item.text
            li = lemmatize(object, phrase)
            for w in li:
                if unicodedata.normalize('NFKD', w).casefold() == unicodedata.normalize('NFKD', wordLemme[0]):
                    data7.append(phrase)
                    if len(data7) > 6:
                        return
    print ("quran done")
    return


def getContextModern(wordLemme):
    path = "corpusXml/modern"
    # wordLemme = lemmatize(object, word)
    global data6
    global metadata6
    data6 = []
    metadata6=[]
    for cat in os.listdir(path):
        for subdir in os.listdir(path+ "/" + cat):
            # if subdir in ["culture","economy","international","local","politic","sport"]:
            #     continue
            for journ in os.listdir(path+"/" + cat + "/" + subdir):
                # print(os.path.abspath(journ.split('.')[0]))
                if (os.path.isdir(path+ "/" + cat + "/" + subdir + "/" + journ) == False):
                    try:
                        tree = parse(path+ "/" + cat + "/" + subdir + "/" + journ)
                    except BaseException as Exception:
                        continue
                    metadata6.append(get_description(tree))
                    for item in tree.findall('.//phrase'):
                        phrase = item.text
                        li = lemmatize(object, phrase)
                        for w in li:
                            if unicodedata.normalize('NFKD', w).casefold() == unicodedata.normalize('NFKD', wordLemme[0]):
                                data6.append(phrase)
                                if len(data6) > 6:
                                    return
                else:
                    for file in os.listdir(path+ "/" + cat + "/" + subdir + "/" + journ):
                        tree =parse(path+ "/" + cat + "/" + subdir + "/" + journ + "/" + file)
                        metadata6.append(get_description(tree))
                        for item in tree.findall('.//phrase'):
                            phrase = item.text
                            li = lemmatize(object, phrase)
                            for w in li:
                                if unicodedata.normalize('NFKD', w).casefold() == unicodedata.normalize('NFKD',wordLemme[0]):
                                    data6.append(phrase)
                                    if len(data6) > 6:
                                        return
    print ("modern done")
    return


def getContextPreIslamic(wordLemme):
    path = "corpusXml/pre-islamic"
    # wordLemme=lemmatize(object,word)
    global data1
    global metadata1
    data1 = []
    metadata1= []
    for cat in os.listdir(path):
        for subdir in os.listdir(path+"/"+cat):
            for file in os.listdir(path+"/"+cat+"/"+subdir):
                try:
                    tree = parse(path+"/"+cat+"/"+subdir+"/"+file)
                except BaseException as Exception:
                    continue
                metadata1.append(get_description(tree))
                for item in tree.findall('.//phrase'):
                    phrase = item.text
                    li = lemmatize(object, phrase)
                    for w in li:
                        if unicodedata.normalize('NFKD',w).casefold() == unicodedata.normalize('NFKD',wordLemme[0]):
                            data1.append(phrase)
                            if len(data1) > 6:
                                return
    print ("pre islamic done")
    return


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_all_dicts(conn):
    cur = conn.cursor()
    cur.execute("select  explination from WordsTable")
    rows = cur.fetchall()
    for row in rows:
        print(row)


def get_definition(w,conn):
    cur = conn.cursor()
    requete = "SELECT word,meaning FROM WordsTable WHERE word = ?"
    value=(w,)
    print(requete)
    cur.execute(requete,value)
    rows = cur.fetchall()
    listDef =[]
    dict={}

    for row in rows:
        continue
    return dict

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
    for e in numdict:
        print (e)
    return numdict


def getDistinctWords(conn):
    global dict_1, dict_2, dict_3, dict_4, dict_5, dict_6, dict_7, dict_8, dict_9, dict_10, dict_11, dict_12, dict_13, dict_14, dict_15, dict_16, dict_17, dict_18, dict_19, dict_20, dict_21, dict_22, dict_23, dict_24, dict_25, dict_26, dict_27, dict_28
    dict_1, dict_2, dict_3, dict_4, dict_5, dict_6, dict_7, dict_8, dict_9, dict_10, \
    dict_11, dict_12, dict_13, dict_14, dict_15, dict_16, dict_17, dict_18, dict_19, dict_20, dict_21, dict_22, dict_23, \
    dict_24, dict_25, dict_26, dict_27, dict_28 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
    global listdict
    listdict = {1: dict_1, 2: dict_2, 3: dict_3, 4: dict_4, 5: dict_5, 6: dict_6, 7: dict_7, 8: dict_8, 9: dict_9,
                10: dict_10, 11: dict_11, 12: dict_12,
                13: dict_13, 14: dict_14, 15: dict_15, 16: dict_16, 17: dict_17, 18: dict_18, 19: dict_19, 20: dict_20,
                21: dict_21, 22: dict_22,
                23: dict_23, 24: dict_24, 25: dict_25, 26: dict_26, 27: dict_27, 28: dict_28
                }
    print("in getDisctincWords")
    cur = conn.cursor()
    requete = "SELECT word,meaning,explination FROM WordsTable"
    cur.execute(requete)
    rows = cur.fetchall()
    for row in rows: #for each word from almaany
        clean_word=removingTachkil(row[0])
        numdict= get_numL_dictXML(clean_word) #get indice of the dict corresponding to the letter that starts with
        if numdict[0] not in range(1,29):
            print("num dict erroné= ",numdict[0])
            continue
        dictword = listdict[numdict[0]] #get the appropriate dict
        print("num dict= ",numdict[0])
        if row[0] in dictword:
            if row[2] in dictword[row[0]]:
                dictword[row[0]][row[2]].append(row[1])
            else:
                dictword[row[0]][row[2]]=[row[1]]
        else:
            dictword[row[0]]=dict({row[2]:[row[1]]})
    return

def save_dictionary():
    #object = initializingJar()
    conn = create_connection("./AlmaanyArArFinal_NEW.db")
    getDistinctWords(conn) # remplir les dicts
    for c in range(1,29):
        di = listdict[c]
        name='dictionary_'+str(c)+'.pkl'
        with open(name, 'wb') as f:
            pickle.dump(di, f)

def load_dictionary():
    for c in range(1,29):
        name = 'dictionary_' + str(c) + '.pkl'
        with open(name, 'rb') as f2:
            listdict[c] = pickle.load(f2)
            print ("dict ",c)
            # for el in listdict[c] :
            #     print (listdict[c][el],"  key= ",el)


# object = initializingJar()
# save_dictionary()
# print("Saving dictionnaries ends!")
global dict_1, dict_2, dict_3, dict_4, dict_5, dict_6, dict_7, dict_8, dict_9, dict_10, dict_11, dict_12, dict_13, dict_14, dict_15, dict_16, dict_17, dict_18, dict_19, dict_20, dict_21, dict_22, dict_23, dict_24, dict_25, dict_26, dict_27, dict_28
dict_1, dict_2, dict_3, dict_4, dict_5, dict_6, dict_7, dict_8, dict_9, dict_10, \
dict_11, dict_12, dict_13, dict_14, dict_15, dict_16, dict_17, dict_18, dict_19, dict_20, dict_21, dict_22, dict_23, \
dict_24, dict_25, dict_26, dict_27, dict_28 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
global listdict
listdict = {1: dict_1, 2: dict_2, 3: dict_3, 4: dict_4, 5: dict_5, 6: dict_6, 7: dict_7, 8: dict_8, 9: dict_9,
            10: dict_10, 11: dict_11, 12: dict_12,
            13: dict_13, 14: dict_14, 15: dict_15, 16: dict_16, 17: dict_17, 18: dict_18, 19: dict_19, 20: dict_20,
            21: dict_21, 22: dict_22,
            23: dict_23, 24: dict_24, 25: dict_25, 26: dict_26, 27: dict_27, 28: dict_28
            }
load_dictionary()
object = initializingJar()
root = et.Element("Dictionnary")
coo=1
for c in range(1, 29):
    di = listdict[c]
    for el in di:
        print(el)
        coo+=1
        functionsDict = {
            1: getContextPreIslamic,
            2: getContextIslamic,
            3: getContextUmayyad,
            4: getContextAbbasid,
            5: getContextMiddleAges,
            6: getContextModern,
            7: getContextQuran
        }
        print("not starting the functions")
        word = et.SubElement(root, "word",name =lemmatize(object,el)[0],value="not validated")
        definition = et.SubElement(word,"Definitions")
        cpt=0
        for de in di[el]:
            cpt+=1
            definitionDict = et.SubElement(definition,"Dict"+str(cpt),name =de)
            cpt2=0
            for defElement in di[el][de]:
                cpt2+=1
                subEl=defElement.split('|')
                for subsubEl in subEl:
                    definitionNum = et.SubElement(definitionDict, "def"+ str(cpt2))
                    definitionNum.text=subsubEl
        context = et.SubElement(word,"Exemples")
        pre_islamic = et.SubElement(context,"pre-islamic")
        islamic = et.SubElement(context,"islamic")
        umayyad = et.SubElement(context,"umayyad")
        abbasid = et.SubElement(context,"abbasid")
        middle_ages = et.SubElement(context,"middle_ages")
        modern = et.SubElement(context,"modern")
        quran = et.SubElement(context,"quran")
        c = 1
        cleanword= removingTachkil(el)
        wordLemme= lemmatize(object,cleanword)
        threads = []
        for count in range(1,8):
            t = threading.Thread(target = functionsDict[count](wordLemme))
            threads.append(t)
            t.start()
            t.join()

        for co ,md in data1,metadata1:
            subCon =et.SubElement(pre_islamic,"Exemple"+str(c))
            subCon.text = co
            c+=1
            disc = et.SubElement(subCon, "Reference"+str(c))
            disc.text = "|".join(md)

        c=1
        for co,md2 in data2,metadata2:
            subCon = et.SubElement(islamic, "Exemple" + str(c))
            subCon.text = co
            c += 1
            disc = et.SubElement(subCon, "Reference" + str(c))
            disc.text = "|".join(md2)

        c = 1
        for co ,md3 in data3,metadata3:
            subCon = et.SubElement(umayyad, "Exemple" + str(c))
            subCon.text = co
            c += 1
            disc = et.SubElement(subCon, "Reference" + str(c))
            disc.text = "|".join(md3)

        c = 1
        for co,md4 in data4,metadata4:
            subCon = et.SubElement(abbasid, "Exemple" + str(c))
            subCon.text = co
            c += 1
            disc = et.SubElement(subCon, "Reference" + str(c))
            disc.text = "|".join(md4)

        c = 1
        for co,md5 in data5,metadata5:
            subCon = et.SubElement(middle_ages, "Exemple" + str(c))
            subCon.text = co
            c += 1
            disc = et.SubElement(subCon, "Reference" + str(c))
            disc.text = "|".join(md5)

        c = 1
        for co,md6 in data6,metadata6:
            subCon = et.SubElement(modern, "Exemple" + str(c))
            subCon.text = co
            c += 1
            disc = et.SubElement(subCon, "Reference" + str(c))
            disc.text = "|".join(md6)

        c = 1
        for co,md7 in data7,metadata7:
            subCon = et.SubElement(quran, "Exemple" + str(c))
            subCon.text = co
            c += 1
            disc = et.SubElement(subCon, "Reference" + str(c))
            disc.text = "|".join(md7)

    tree = et.ElementTree(root)
    tree.write("HistDictionary_letter"+str(c)+".xml", encoding="UTF-8", xml_declaration=True)
    print("END OF XML HISTORIEN DICT NUM: ",c)

print ("END OF ALL THE 28 XML HISTORIEN DICT")



