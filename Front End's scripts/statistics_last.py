import cleaning as cl
import os
import codecs
import nltk as n
import nltk
import numpy as np
import matplotlib.pyplot as plt
from nltk import bigrams
from operator import itemgetter

def compare_diversity(period1,period2):
    return most_common(period1).N() /most_common(period2).N()

def graph(period,number):
    fd = most_common(period)
    fd.plot(number,title='Frequency plot',cumulative=False)

def most_common(period):
    listWords=[]
    listWords2=[]
    path = "finalCorpus"
    if period == 'pre-islamic':
        for cat in os.listdir(path+"/pre-islamic"):
            for subdir in os.listdir(path+"/"+"pre-islamic"+ "/" + cat):
#                print(subdir)
                for file in os.listdir(path +"/pre-islamic"+ "/" + cat + "/" + subdir):
#                    print(file)
#                    print(subdir)
#                    print(cat)
                    f= codecs.open(path +"/pre-islamic"+ "/" + cat + "/" + subdir+"/"+file,"r",encoding="utf-8")
                    text = cl.removingStopWords(f.read())
                    listWords .extend(cl.tokenization(text))
        fq = nltk.FreqDist(listWords)
        return fq
    if period=="islamic":
        for cat in os.listdir(path + "/islamic"):
            for subdir in os.listdir(path + "/" + "islamic" + "/" + cat):
                for file in os.listdir(path + "/islamic" + "/" + cat + "/" + subdir):
                    f = codecs.open(path + "/islamic" + "/" + cat + "/" + subdir + "/" + file, "r",
                                    encoding="utf-8")
                    text = cl.removingStopWords(f.read())
                    listWords .extend(cl.tokenization(text))
        fq = nltk.FreqDist(listWords)
        return fq
    if period == "umayyad":
        for cat in os.listdir(path + "/umayyad"):
            for subdir in os.listdir(path + "/" + "umayyad" + "/" + cat):
#                print(subdir)
                for file in os.listdir(path + "/umayyad" + "/" + cat + "/" + subdir):
#                    print(file)
#                    print(subdir)
#                    print(cat)
                    f = codecs.open(path + "/umayyad" + "/" + cat + "/" + subdir + "/" + file, "r",
                                    encoding="utf-8")
                    text = cl.removingStopWords(f.read())
                    listWords.extend(cl.tokenization(text))
        fq = nltk.FreqDist(listWords)
        return fq
    if period =="abbasid":
        for cat in os.listdir(path + "/abbasid"):
            for subdir in os.listdir(path + "/" + "abbasid" + "/" + cat):
#                print(subdir)
                for file in os.listdir(path + "/abbasid" + "/" + cat + "/" + subdir):
#                    print(file)
#                    print(subdir)
#                    print(cat)
                    f = codecs.open(path + "/abbasid" + "/" + cat + "/" + subdir + "/" + file, "r",
                                    encoding="utf-8")
                    text = cl.removingStopWords(f.read())
                    listWords.extend(cl.tokenization(text))
        fq = nltk.FreqDist(listWords)
        return fq
    if period == "middle-ages":
        for cat in os.listdir(path + "/middle-ages"):
            for subdir in os.listdir(path + "/" + "middle-ages" + "/" + cat):
#                print(subdir)
                for file in os.listdir(path + "/middle-ages" + "/" + cat + "/" + subdir):
#                    print(file)
#                    print(subdir)
#                    print(cat)
                    f = codecs.open(path + "/middle-ages" + "/" + cat + "/" + subdir + "/" + file, "r",
                                    encoding="utf-8")
                    text = cl.removingStopWords(f.read())
                    listWords.extend(cl.tokenization(text))
        fq = nltk.FreqDist(listWords)
        return fq
    if period == "modern":
        for cat in os.listdir(path+"/modern"):
            for subdir in os.listdir(path+"/modern" + "/" + cat):
#                print(subdir)
                for journ in os.listdir(path +"/modern"+ "/" + cat + "/" + subdir):
#                    print(journ)
                    if (os.path.isdir(path+"/modern" + "/" + cat + "/" + subdir + "/" + journ) == False):
                        f = codecs.open(path +"/modern"+ "/" + cat + "/" + subdir + "/" + journ,"r",encoding='windows-1256')
                        t= f.read()
                        text = cl.removingStopWords(t)
                        listWords.extend(cl.tokenization(text))
                    else:
                        for file in os.listdir(path+"/modern" + "/" + cat + "/" + subdir + "/" + journ):
                            f = codecs.open(path+"/modern" + "/" + cat + "/" + subdir + "/" + journ + "/" + file,"r",encoding='windows-1256')
                            t= f.read()
                            text = cl.removingStopWords(t)
                            listWords2.extend(cl.tokenization(text))
        listWords.extend(listWords2)
        fq = nltk.FreqDist(listWords)
        return fq
    if period == "quran":
        for sourat in os.listdir(path+"/quran/books"):
            f = codecs.open(path+"/quran/books"+ "/" + sourat,"r",encoding="utf-8")
            text = cl.removingStopWords(f.read())
            listWords.extend(cl.tokenization(text))
        fq = nltk.FreqDist(listWords)
        return fq

def longeurMoyenneWord(text):
    listText = text.split()
    longeur_moyenne = sum([len(w) for w in listText]) / len(listText)
    return longeur_moyenne

def frequenceDist(text):
    listText = text.split()
    fq = nltk.FreqDist(listText)
    sortedFD = sorted(fq.items(), key=itemgetter(1), reverse=True)
    return sortedFD

def frequenWordPerPeriod(word, period):
    fd= most_common(period)
    return fd[word]

def most_common_bigram(text):
    bigr= bigrams(text.split())
    fd= nltk.FreqDist(bigr)
    sortedFD= sorted(fd.items(), key=itemgetter(1), reverse=True)
    return sortedFD

def frequence_lessThen(text,nb):
    fd = nltk.FreqDist(text.split())
    return [(w,fd[w]) for w in fd if fd[w]<=nb]




# =============================================================================
# import pickle
# from alphabet_detector import AlphabetDetector
# import re
# from nltk.corpus import stopwords
# stopwords_list = stopwords.words('arabic')
# eras = ['pre-islamic','middle-ages',  'umayyad',  'abbasid','modern','quran']
# # fqModern = most_common("modern")
# for e in eras:
#     print (e)
#     if os.path.getsize("Fq"+e+".pkl")>0:
#         with open("Fq"+e+".pkl","rb")  as f:
#             unpickler = pickle.Unpickler(f)
#             di=unpickler.load()
#         co =1
#         ad = AlphabetDetector()
#         for el in di:
#             if co >40:
#                 break
#             w = cl.removingTachkil(el[0])
#             w = re.sub(r'[\u0621-\u064A\u0660-\u0669]\\n', '', el[0])
#             li = '0123456789؛؟ۗ’‘،.«„»'
#             lis = [c for c in li]
#             if w in stopwords_list or w in li:
#                 continue
#             else:
#                 print(el)
#                 co+=1
#         print("******************************")
# =============================================================================
# import pickle
# di =  most_common("pre-islamic")
# with open('fqpre-islamic.pkl', 'wb') as f:
#     pickle.dump(di, f)
    

#def read_from_pickle(path):
#    with open(path, 'rb') as file:
#        try:
#            while True:
#                yield pickle.load(file)
#        except EOFError:
#            pass
    
#b = open("freq_dist/Fqabbasid.pkl", "rb")
#c = pickle.load(b)