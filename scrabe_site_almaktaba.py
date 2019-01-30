import  os
import nltk,re
from urllib.request import Request, urlopen
from nltk.tokenize import sent_tokenize, word_tokenize
from bs4 import BeautifulSoup #u may need to do : pip install bs4
from nltk.corpus import stopwords
import urllib
import requests
import webbrowser
from snowballstemmer import stemmer


'''
another way to define url_open(webpage):
class AppURLopener(urllib.request.FancyURLopener):
version = "Mozilla/5.0"

opener = AppURLopener()
response = opener.open('http://httpbin.org/user-agent')
'''
#retourne stem d'un mot
def stemmer_word(word):
    ar_stemmer = stemmer("arabic")
    return ar_stemmer.stemWord(u+word)

#lire l'url , meme d'un site protégé
def url_open(webpage):
    req = Request(webpage, headers={'User-Agent': 'Mozilla/5.0'}) #only urlopen caused an error car site protected :3
    webpage = urlopen(req).read()
    return webpage

#nettoyage du code source d'une page, using reg expers and beautifulsoup
def clear_content(webpage,encodage,lang):
    page =url_open(webpage)
    page= page.decode(encodage)
    page = re.sub(r"<.*?>", " ", page)
    page = re.sub("\s+", " ", page)
    page = re.sub(r'<div(.+?)\">', '', page)
    page = re.sub(r'<(?:.|\n)*?>', '', page)
    page = re.sub(r'<!--(.*?)-->', '', page)
    page = re.sub(r'\w&#[a-z0-9]*', '', page)
    page = re.sub(r'<span .*? >(.*?)</span>', '', page)
    page = re.sub(r'&nbsp', '', page)
    page = re.sub("\s+", " ", page)
    soup = BeautifulSoup(page, "lxml") #u may need to do : pip install lxml // il existe aussi html.parser
    list=soup.get_text().lower()

    list = word_tokenize(text=list, language=lang, preserve_line="true")
    stopWords = set(stopwords.words(lang))
    wordsFiltered=[]

    for w in list:
        if w not in stopWords:
            wordsFiltered.append(w)
            #s=re.match("[A-Za-zèùçà']+",w)
            # arabic character in UNICODE
            s = re.match("[\u0621-\u064A\u0660-\u0669 ]+", w)
            if s:
                print("word ", w)

    return wordsFiltered

# récupérer définition d'un mot de la balise < def > du site Alamany
#récupérer la définition en faisant appel au site directly
def grap_def_from_site(word):
    #r = requests.get("https://www.almaany.com/ar/dict/ar-ar/معجم/")
    r = requests.get("https://www.almaany.com/ar/dict/ar-ar/"+word+"/")
    soup = BeautifulSoup(r.content, "lxml")
    res = soup.find_all("ol")
    all_def=""
    for maana in soup.find_all("ol"):
        print(maana.text)
        all_def+= maana.text+"/"
    list_def=all_def.split("/")
    return list_def

#retourne dictionnaire {author: link, author2:link, ...}
def get_from_url(url,balise):
    dict={}
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")
    #récupérer tt les balises des auteurs avec le lien vers leur page
    print("\n\nAUTHORS' LINKS\n\n")
    lien=re.compile(r"^https://al-maktaba.org/author/[0-9]+")
    for author in soup.find_all('a', attrs={'href': re.compile(lien)}):
        if author.contents[0] != "-":
            print(author.get('href'))
            print(author.contents[0])
            dict[author.contents[0]]=author.get('href')
    return dict

def find_autobiog(soup,balise):
    tags = soup.find_all(balise,attrs={'class': re.compile("alert")})
    for element in tags:
        try:
            print(element.content[0])
        except TypeError:
            print(element.content[0])
            raise




def author_biographie(url):
    r = requests.get(url)
    soup=BeautifulSoup(r.content,"lxml")
    tags = soup.find_all('h4')
    for names in tags:
        if names.contents[0] =="تعريف بالمؤلف ":
            print (tags[00].text)
            #find_autobiog
            tags = soup.find("div", attrs={'class': re.compile("alert")})
            print(tags.contents)



def download_corpus(dict):
    for (name, link) in dict.items():
        author_biographie(link)

#télécharge les livres from maktaba, for chaque author for chaque book, for chaque partie , print dans fich
def retrieve_texte(dict_authors):
    directory="D:\\Etudes\\Master SII 2017_2019\\M2 SII\\M2 2018_2019\\TAL\\TP\\tal_project\\corpus_almaktaba\\"
    for(name,link) in dict_authors.items():
        print (name,link)
        r = url_open(link)
        soup = BeautifulSoup(r,"lxml")
        for link in soup.findAll('a', attrs={'href': re.compile("^https://al-maktaba.org/book/")}): #de l'auteur accéder au book
            link_sommaire = link.get('href') #récupérer lien vers sommaire d'un book
            r2 = url_open(link_sommaire)
            soup2 = BeautifulSoup(r2,"lxml")
            f = open(directory+name+"_"+link.text + ".txt", "w+",encoding='utf-8') #text : nom du book
            for link2 in soup2.findAll('a', attrs={'href': re.compile(link_sommaire)}): #récupérer link des parties du book à télécharger
                print(link2.get('href'))
                next2 = link2.get('href') #lien vers les composantes du book
                r3 = requests.get(next2) #accéder à la partie à récupérer
                soup3 = BeautifulSoup(r3.content, "lxml")
                text_page = soup3.text
                print (text_page)
                '''
                lines = text_page.split('\n')
                txt = ""
                for line in lines:
                    f.write(line[::-1].encode('utf-8') + b'\n')
                '''
                #clear text_page
                f.write(text_page)
            f.close() #fini d'écrire tt les parties






#--------------------------    MAIN --------------------------------------
#------------------------------------------------------------------
'''
webpage = 'https://al-maktaba.org/author/2296'
result = clear_content(webpage, 'utf-8', 'arabic')
print(result)
list_def= grap_def_from_site("معجم")
print ("here"+list_def)
'''
print ("début\n")

dict_authors=get_from_url("https://al-maktaba.org/authors/?sort=alpha","a")
print (dict_authors)
#for (name,link) in links_authors.items():
#author_biographie(link) #récuperer ta3rif et savoir on enregistrer le texte
'''
author_biographie("https://al-maktaba.org/author/6")
'''
#presentation_author=find_balise(,"تعريف بالمؤلف ")
retrieve_texte(dict_authors)
print ("\nfin")