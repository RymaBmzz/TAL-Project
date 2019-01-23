# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
import nltk
from string import punctuation
import re
from snowballstemmer import stemmer
import subprocess
import xml.etree.cElementTree as ET
punctuation = punctuation + '0123456789؛؟.'

#Tokenization du texte
def tokenization(txt):
    tokens = nltk.word_tokenize(txt)
    return tokens

#Suppression des stop words et des ponctuations
def removingStopWords(text):
    texteCleaned = ''.join(c for c in text if c not in punctuation)
    texteCleanedS = texteCleaned.split()
    stopWords = open('stopWords.txt','r',encoding='utf-8').read().splitlines()
    # print("Stop words :")
    # print(stopWords)
    cleaned = []
    for word in texteCleanedS:
        if word not in stopWords:
            cleaned.append(word)
    return ' '.join(cleaned)


#Stemming sur le texte tokenizé
def stemming1(txt):
    stemmer = nltk.stem.isri.ISRIStemmer()
    stems = str([stemmer.stem(w) for w in tokenization(txt)])
    return stems

def stemming2(txt):
    ar_stemmer = stemmer("arabic")
    stems = str([ar_stemmer.stemWord(w) for w in tokenization(txt)])
    return stems

#def stemming3(txt):
#    farasaSegmenterJar = 'C:/Users/USER/Documents/Master2/TAL/FarasaSegmenterJar/FarasaSegmenterJar.jar'
#    input = 'input.txt'
#
#    open(input, 'w', encoding='windows-1256').write(txt)
#    output = 'output.txt'
#
#    jarFarasaPos = 'C:/Users/USER/Documents/Master2/TAL/FarasaPOSJar/FarasaPOSJar.jar'
#    subprocess.call('java -Dfile.encoding=WINDOWS-1256 -jar ' + farasaSegmenterJar + ' -i ' + input + ' -o ' + output,shell=True)
#    result = open(output, 'r',encoding="windows-1256")
#
#    return result.read()


def removingTachkil(text):
    noise = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida


                         """, re.VERBOSE)
    text = re.sub(noise, '', text)
    return text

def createCorpus(text):
    root = ET.Element("root")
    doc = ET.SubElement(root, "doc")
    ET.SubElement(doc, "field1", name="blah").text = "some value1"
    ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"

    tree = ET.ElementTree(root)
    tree.write("filename.xml")

'''
filepath = "texteBrute.txt"
with open(filepath,encoding='utf-8') as fp:
   line = fp.readline()
   cnt = 1
   lignes = []
   while line:

       # print("Line {}: {}".format(cnt, line.strip()))
       ligneTmp = removingTachkil(line.strip())
       lignes.append(ligneTmp)
       line = fp.readline()

       cnt += 1

texte = ''.join(lignes)

# print(lignes)
# print("**************")
print(texte)
texteCleaned = removingStopWords(texte)
print("Le texte cleaned:")
print(texteCleaned)
texteTokenized = tokenization(texteCleaned)
print("Texte tokenizé")
print(texteTokenized)
#Partie du stemming
stems = stemming2(texteTokenized)
#Partie de al maany


print("STEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEM")
# print(stemming2(textCleaned))
# print(len(texteTokenized))
# print("*************************************************")
# textCleaned = removingStopWords(texteTokenized)
# print(textCleaned)
# print(len(textCleaned))
'''