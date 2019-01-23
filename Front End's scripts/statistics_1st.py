import cleaning as cl
import os
import codecs
import nltk as n
import numpy as np
import matplotlib.pyplot as plt
from nltk import bigrams
from operator import itemgetter

def compare_diversity(period1,period2):
    return most_common(period1).N() /most_common(period2).N()

def graph(period,number):
    fd = most_common(period)
    fd.plot(number,cumulative=False)

def most_common(period):
    listWords=[]
    listWords2=[]
    path = "finalCorpus"
    if period == 'pre-islamic':
        for cat in os.listdir(path+"/pre-islamic"):
            for subdir in os.listdir(path+"/"+"pre-islamic"+ "/" + cat):
                print(subdir)
                for file in os.listdir(path +"/pre-islamic"+ "/" + cat + "/" + subdir):
                    print(file)
                    print(subdir)
                    print(cat)
                    f= codecs.open(path +"/pre-islamic"+ "/" + cat + "/" + subdir+"/"+file,"r",encoding="utf-8")
                    text = cl.removingStopWords(f.read())
                    listWords .extend(cl.tokenization(text))
        fq = n.FreqDist(listWords)
        sortedFD = sorted(fq.items(), key=itemgetter(1), reverse=True)
        return sortedFD
    if period=="islamic":
        for cat in os.listdir(path + "/islamic"):
            for subdir in os.listdir(path + "/" + "islamic" + "/" + cat):
                for file in os.listdir(path + "/islamic" + "/" + cat + "/" + subdir):
                    f = codecs.open(path + "/islamic" + "/" + cat + "/" + subdir + "/" + file, "r",
                                    encoding="utf-8")
                    text = cl.removingStopWords(f.read())
                    listWords .extend(cl.tokenization(text))
        fq = n.FreqDist(listWords)
        sortedFD = sorted(fq.items(), key=itemgetter(1), reverse=True)
        return sortedFD
    if period == "umayyad":
        for cat in os.listdir(path + "/umayyad"):
            for subdir in os.listdir(path + "/" + "umayyad" + "/" + cat):
                print(subdir)
                for file in os.listdir(path + "/umayyad" + "/" + cat + "/" + subdir):
                    print(file)
                    print(subdir)
                    print(cat)
                    f = codecs.open(path + "/umayyad" + "/" + cat + "/" + subdir + "/" + file, "r",
                                    encoding="utf-8")
                    text = cl.removingStopWords(f.read())
                    listWords.extend(cl.tokenization(text))
        fq = n.FreqDist(listWords)
        sortedFD = sorted(fq.items(), key=itemgetter(1), reverse=True)
        return sortedFD
    if period =="abbasid":
        for cat in os.listdir(path + "/abbasid"):
            for subdir in os.listdir(path + "/" + "abbasid" + "/" + cat):
                print(subdir)
                for file in os.listdir(path + "/abbasid" + "/" + cat + "/" + subdir):
                    print(file)
                    print(subdir)
                    print(cat)
                    f = codecs.open(path + "/abbasid" + "/" + cat + "/" + subdir + "/" + file, "r",
                                    encoding="utf-8")
                    text = cl.removingStopWords(f.read())
                    listWords.extend(cl.tokenization(text))
        fq = n.FreqDist(listWords)
        sortedFD = sorted(fq.items(), key=itemgetter(1), reverse=True)
        return sortedFD
    if period == "middle-ages":
        for cat in os.listdir(path + "/middle-ages"):
            for subdir in os.listdir(path + "/" + "middle-ages" + "/" + cat):
                print(subdir)
                for file in os.listdir(path + "/middle-ages" + "/" + cat + "/" + subdir):
                    print(file)
                    print(subdir)
                    print(cat)
                    f = codecs.open(path + "/middle-ages" + "/" + cat + "/" + subdir + "/" + file, "r",
                                    encoding="utf-8")
                    text = cl.removingStopWords(f.read())
                    listWords.extend(cl.tokenization(text))
        fq = n.FreqDist(listWords)
        sortedFD = sorted(fq.items(), key=itemgetter(1), reverse=True)
        return sortedFD
    if period == "modern":
        for cat in os.listdir(path+"/modern"):
            for subdir in os.listdir(path+"/modern" + "/" + cat):
                for journ in os.listdir(path +"/modern"+ "/" + cat + "/" + subdir):
                    if (os.path.isdir(path+"/modern" + "/" + cat + "/" + subdir + "/" + journ) == False):
                        f = open(path +"/modern"+ "/" + cat + "/" + subdir + "/" + journ,"r")
                        text = cl.removingStopWords(f.read())
                        listWords.extend(cl.tokenization(text))
                    else:
                        for file in os.listdir(path+"/modern" + "/" + cat + "/" + subdir + "/" + journ):
                            f = open(path+"/modern" + "/" + cat + "/" + subdir + "/" + journ + "/" + file,"r")
                            text = cl.removingStopWords(f.read())
                            listWords2.extend(cl.tokenization(text))
        listWords.extend(listWords2)
        fq = n.FreqDist(listWords)
        sortedFD = sorted(fq.items(), key=itemgetter(1), reverse=True)
        return sortedFD
    if period == "quran":
        for sourat in os.listdir(path+"/quran"):
            f = codecs.open(path+"/quran"+ "/" + sourat,"r",encoding="utf-8")
            text = cl.removingStopWords(f.read())
            listWords.extend(cl.tokenization(text))
        fq = n.FreqDist(listWords)
        sortedFD = sorted(fq.items(), key=itemgetter(1), reverse=True)
        return sortedFD

def longeurMoyenneWord(text):
    listText = text.split()
    longeur_moyenne = sum([len(w) for w in listText]) / len(listText)
    return longeur_moyenne

def frequenceDist(text):
    listText = text.split()
    fq = n.FreqDist(listText)
    sortedFD = sorted(fq.items(), key=itemgetter(1), reverse=True)
    return sortedFD

def frequenWordPerPeriod(word, period):
    fd= most_common(period)
    return fd[word]

def most_common_bigram(text):
    bigr= bigrams(text.split())
    fd= n.FreqDist(bigr)
    sortedFD= sorted(fd.items(), key=itemgetter(1), reverse=True)
    return sortedFD

def frequence_lessThen(text,nb):
    fd = n.FreqDist(text.split())
    return [(w,fd[w]) for w in fd if fd[w]<=nb]
