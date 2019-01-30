# coding=utf-8
#-*-coding:utf-8-*-
import re,os,nltk
from snowballstemmer import stemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

#retourne stem d'un mot
def stemmer_word(word):
    ar_stemmer = stemmer("arabic")
    return ar_stemmer.stemWord(u+word)


def deNoise(text):
    noise = re.compile(r""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ 
                                     #tatwil/Kashida 

                         """, re.VERBOSE)
    text = re.sub(noise, '', text)
    text= re.sub("\s+", ' ',text)
    return text

#nettoyage du code source d'une page, using reg expers and beautifulsoup
def clear_content_txt(texte,lang):
    page = re.sub(r"<.*?>", " ", texte)
    '''
    page = re.sub(r'<div(.+?)\">', ' ', page)
    page = re.sub(r'<(?:.|\n)*?>', ' ', page)
    page = re.sub(r'<!--(.*?)-->', ' ', page)
    page = re.sub(r'\w&#[a-z0-9]*', ' ', page)
    page = re.sub(r'<span .*? >(.*?)</span>', '', page)
    page = re.sub(r'&nbsp', '', page)
    '''
    page = re.sub(r'[,=:;\.;()_-]',' ',page) #\[\]\*\+\\
    page = re.sub(r'(//.-./.\\)|//|--|///\\|\'{1,5}|\[|\]|\}|\{|>|<|#|\\|///|/|\|\||\*|\+',' ',page)
    page = re.sub(r'(×.*×)?','',page)
    page= re.sub(r'<<  < .* >  >>?','',page)
    page = re.sub(r'[0-9A-Za-z]*','',page)
    page= re.sub(r'_[a-z]{1,4}_id = \'\d+\'','',page)
    page = re.sub(r'[\u0621-\u064A\u0660-\u0669]\\n','',page)
    page =re.sub(r'حول المشروع |المكتبة الشاملة الحديثة| البحث في محتوى الكتاب الحالي| كامل المكتبة| المكتبة الشاملة الحديثة| الرئيسية| أقسام المكتبة| فهرس المؤلفين| حول المشروع| تنزيل المكتبة| اتصل بنا| المكتبة الشاملة الحديثة |أقسام الكتب| التاريخ|الشاملة للحاسوب للأندرويد للآيفون إغلاق|اتصل بنا|البحث في محتوى الكتاب الحالي| تنزيل المكتبة ','',page)

    page = re.sub("\s+", ' ', page)
    '''
    list = word_tokenize(text=page, language=lang, preserve_line="true")
    stopWords = set(stopwords.words(lang))
    wordsFiltered=[]

    for w in list:
        if w not in stopWords:
            wordsFiltered.append(w)
            #s=re.match("[A-Za-zèùçà']+",w)
            # arabic character in UNICODE
            s = re.match("[\u0621-\u064A\u0660-\u0669]+", w)
            if s:
                print("word ", w)
                
    return wordsFiltered
    '''
    return page

def process_cleaning_corpus():
    #customize to your path girls !!!!
    directory = "D:\\Etudes\\Master SII 2017_2019\\M2 SII\\M2 2018_2019\\TAL\TP\\tal_project\\corpus_almaktaba\\"
    #customize to your types of folder
    types=['abasside\\','djahili\\','modernes\\','oustta\\','amawi\\']
    for dossier in types:
        for element in os.listdir(directory+dossier+"brute\\"):
            if os.path.isdir(element):
                print ("dossier:    ",element)
            else:
                if element.endswith('.txt'):
                    print("fichier: ",element)
                    pathsrc=directory+dossier+"brute\\"+element
                    f = open(pathsrc,"r", encoding='utf-8')
                    texte=f.readlines()
                    #print (texte)
                    pathdst=directory+dossier+"\\cleaned\\"
                    file= open(pathdst+"cleaned_"+element,'w',encoding='utf-8')
                    #text=deNoise(str(texte))
                    result=clear_content_txt(str(texte),'arabic')
                    #call stemmer
                    #for word in result:
                     #   file.write(str(word)+"\n")
                    file.write(str(result))
                    file.close()


#process_cleaning_corpus()
'''
pathdst="D:\\Etudes\\corpus_almaktaba\\abbasid\\أبو يعلى ابن الفراء\\أمالي أبي يعلى الفراء"
file=open("D:\\Etudes\\corpus_almaktaba\\abbasid\\أبو يعلى ابن الفراء\\أمالي أبي يعلى الفراء.txt",'r',encoding="utf-8")
text=file.readlines()
result=deNoise(str(text))
filer = open(pathdst + "cleaned.txt", 'w', encoding='utf-8')
filer.write(str(result))
filer.close()
'''
def clean_header(texte):
    t="بطاقة الكتاب^"
    f="$:عدد الأجزاء"
    expr=t+".*"+f
    page = re.sub(expr," ", texte)
    page = re.sub("\s+", ' ', page)
    return page

def remove_noise():
    directory = "D:\\Etudes\\corpus_almaktaba\\"
    # customize to your types of folder
    #types = ['abbasid\\', 'modern\\', 'islamic\\', 'middle_ages\\', 'pre_islamic\\','umayyad\\','non_classified\\']
    types = ['non_classified\\']
    for dossier in types:
        for auteur in os.listdir(directory + dossier + "brute\\"):
                    print("auteur: ", auteur)
                    pathsrc = directory + dossier + "brute\\" + auteur #dossier d'un auteur
                    for textefile in os.listdir(pathsrc):
                        print ("file: ",textefile)
                        f = open(pathsrc+"\\"+textefile, "r", encoding='utf-8')
                        texte = f.readlines()
                        # print (texte)
                        pathdst = directory + dossier + "\\cleaned\\"+auteur
                        if not os.path.exists(pathdst):
                            os.makedirs(pathdst)
                        file = open(pathdst+"\\"+ textefile, 'w', encoding='utf-8')
                        text=clean_header(str(texte))
                        result = clear_content_txt(str(text), 'arabic')
                        file.write(str(result))
                        file.close()

remove_noise()
