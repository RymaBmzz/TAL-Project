import pickle
import os
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
object = initializingJar()
def getContextIslamic():
    path = "corpusXml/islamic"
    global data2
    data2 = {}
    for cat in os.listdir(path):
        for subdir in os.listdir(path + "/" + cat):
            for file in os.listdir(path + "/" + cat + "/" + subdir):
                tree = parse(path + "/" + cat + "/" + subdir + "/" + file)
                for item in tree.findall('.//phrase'):
                    phrase = item.text
                    li = set(lemmatize(object, phrase))
                    for w in li:
                       if w not in data2:
                           data2.update({w:[phrase]})
                       else:
                            data2[w].append(phrase)
    with open('contextIslamic.pkl','wb') as f:
        pickle.dump(data2, f)
    return data2
def getContextModern():
    path = "corpusXml/modern"
    global data6
    data6 = {}
    for cat in os.listdir(path):
        for subdir in os.listdir(path+ "/" + cat):
            print(subdir)
            for journ in os.listdir(path+"/" + cat + "/" + subdir):
                if (os.path.isdir(path+ "/" + cat + "/" + subdir + "/" + journ) == False):
                    try:
                        tree = parse(path+ "/" + cat + "/" + subdir + "/" + journ)
                    except BaseException as Exception:
                        continue
                    for item in tree.findall('.//phrase'):
                        phrase = item.text
                        li = set(lemmatize(object, phrase))
                        for w in li:
                            if w not in data6:
                                data6.update({w: [phrase]})
                            else:
                                data6[w].append(phrase)
                else:
                    for file in os.listdir(path+ "/" + cat + "/" + subdir + "/" + journ):

                        try:
                            tree =parse(path+ "/" + cat + "/" + subdir + "/" + journ + "/" + file)
                        except BaseException as Exception:
                            continue
                        for item in tree.findall('.//phrase'):
                            phrase = item.text
                            li = set(lemmatize(object, phrase))
                            for w in li:
                                if w not in data6:
                                    data6.update({w: [phrase]})
                                else:
                                    data6[w].append(phrase)
    with open('contextModern.pkl','wb') as f:
        pickle.dump(data6, f)
    return

def getContextQuran():
    path = "corpusXml/quran"
    global data7
    data7 = {}
    for sourat in os.listdir(path):
        tree = parse(path + "/" + sourat)
        for item in tree.findall('.//aya'):
            phrase = item.text
            li = set(lemmatize(object, phrase))
            for w in li:
                if w not in data7:
                    data7.update({w: [phrase]})
                else:
                    data7[w].append(phrase)
    with open('contextQuran.pkl','wb') as f:
        pickle.dump(data7, f)
    return
def getContextPreIslamic():
    path = "corpusXml/pre-islamic"
    global data1
    data1 = {}
    for cat in os.listdir(path):
        for subdir in os.listdir(path+"/"+cat):
            for file in os.listdir(path+"/"+cat+"/"+subdir):
                tree = parse(path+"/"+cat+"/"+subdir+"/"+file)
                for item in tree.findall('.//phrase'):
                    phrase = item.text
                    li = set(lemmatize(object, phrase))
                    for w in li:
                        if w not in data1:
                            data1.update({w: [phrase]})
                        else:
                            data1[w].append(phrase)
    with open('contextPreIslamic.pkl', 'wb') as f:
        pickle.dump(data1, f)
    return
def getContextMiddleAges():
    path = "corpusXml/middle-ages"
    global data5
    data5 = {}
    for cat in os.listdir(path):
        for subdir in os.listdir(path + "/" + cat):
            for file in os.listdir(path + "/" + cat + "/" + subdir):
                tree = parse(path + "/" + cat + "/" + subdir + "/" + file)
                for item in tree.findall('.//phrase'):
                    phrase = item.text
                    li = set(lemmatize(object, phrase))
                    for w in li:
                        if w not in data5:
                            data5.update({w: [phrase]})
                        else:
                            data5[w].append(phrase)
    with open('contextMiddleAges.pkl', 'wb') as f:
        pickle.dump(data5, f)
    return
def getContextAbbasid():
    path = "corpusXml/abbasid"
    global data4
    data4 = {}
    for cat in os.listdir(path):
        for subdir in os.listdir(path + "/" + cat):
            for file in os.listdir(path + "/" + cat + "/" + subdir):
                tree = parse(path + "/" + cat + "/" + subdir + "/" + file)
                for item in tree.findall('.//phrase'):
                    phrase = item.text
                    li = set(lemmatize(object, phrase))
                    for w in li:
                        if w not in data4:
                            data4.update({w: [phrase]})
                        else:
                            data4[w].append(phrase)
    with open('contextAbbasid.pkl', 'wb') as f:
        pickle.dump(data4, f)
    return
def getContextUmayyad():
    path = "corpusXml/umayyad"
    global data3
    data3 = {}
    for cat in os.listdir(path):
        for subdir in os.listdir(path + "/" + cat):
            for file in os.listdir(path + "/" + cat + "/" + subdir):
                tree = parse(path + "/" + cat + "/" + subdir + "/" + file)
                for item in tree.findall('.//phrase'):
                    phrase = item.text
                    li = set(lemmatize(object, phrase))
                    for w in li:
                        if w not in data3:
                            data3.update({w: [phrase]})
                        else:
                            data3[w].append(phrase)
    with open('contextUmayyad.pkl', 'wb') as f:
        pickle.dump(data3, f)
    return

getContextPreIslamic()
getContextIslamic()
getContextUmayyad()
getContextAbbasid()
getContextMiddleAges()
getContextModern()
getContextQuran()