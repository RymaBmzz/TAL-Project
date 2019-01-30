import xml.etree.cElementTree as et
import os
from os.path import isfile
import codecs
import cleaning as cl
import re
def validXml(text):
    text = re.sub("<","&lt;",text)
    text = re.sub(">", "&gt;", text)
    text = re.sub('"', "&quot;", text)
    text = re.sub("'", "&apos;", text)
    text = re.sub("&", "&amp;", text)
    #text = re.sub("\\" , "" ,text)
    return text

def sents(text):
    import nltk.data
    import re
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    punctuation = '؛؟.'
    #print(punctuation)
    texteCleaned = re.sub(punctuation, ".", text)
    list = tokenizer.tokenize(texteCleaned)
    sents=[]
    for li in list:
        if (len(li) < 5):
            continue
        #if ("»" in li):
         #   continue
        if(len(li.split())>20):
            n = li.split("\n")
            for line in n:
                sents.append(line)
        else:
            sents.append(li)
    return sents
import re
#listTimes = ['quran','modern','abbasid','middle-ages','umayyad','pre-islamic', 'islamic']
listTimes = ['modern','abbasid','middle-ages','umayyad','pre-islamic', 'islamic']

count = 0
for time in listTimes:
        for cat in os.listdir("corpus/finalCorpus/"+time):
            for author in os.listdir("corpus/finalCorpus/"+time+"/"+cat):
                for file in os.listdir("corpus/finalCorpus/"+time+"/"+cat+"/"+author):
                    print(file)
                    root = et.Element("Begin")
                    disc = et.SubElement(root,"Description")
                    asr=et.SubElement(disc,"asr")
                    asr.text=time
                    cate=et.SubElement(disc,"categorie")
                    cate.text = cat
                    au=et.SubElement(disc,"author")
                    au.text = author
                    titre=et.SubElement(disc,"title")
                    titre.text = file.split(".")[0]
                    #type=et.SubElement(disc,"type")
                    txt = et.SubElement(root,"text")
                    f = codecs.open("corpus/finalCorpus/"+time+"/"+cat+"/"+author+"/"+file,"r","utf-8")
                    #txt.text = f.read()
                    if cat=="poetry":
                        for line in f.readlines():
                            line1 = et.SubElement(txt, 'phrase')
                            line1.text = cl.removingTachkil(validXml(line))
                    else:
                        listSents = sents(f.read())
                        for line in listSents:
                            if len(line)<=2:
                                continue
                            line1 = et.SubElement(txt,'phrase')
                            line1.text=cl.removingTachkil(validXml(line))
                    if not os.path.exists("corpusXml/"+time+"/"+cat+"/"+author):
                        os.makedirs("corpusXml/"+time+"/"+cat+"/"+author)
                    print("corpusXml/"+time+"/"+cat+"/"+author)
                    tree = et.ElementTree(root)
                    tree.write("corpusXml/"+time+"/"+cat+"/"+author+"/"+file.split(".")[0]+".xml",encoding="UTF-8",xml_declaration=True)
