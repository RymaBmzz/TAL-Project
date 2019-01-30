def inverse_reading(filename):

        handler= open(filename,"r").read()
        list=handler.split("\n")
        list.reverse()
        for e in list:
         print(e)

def find_whwords(text):
    import nltk
    austen=nltk.corpus.gutenberg.words(text)
#    austen=nltk.word_tokenize(text)

    for i in austen:
        if i.startswith("wh"):
            print("find:",i)
def clear_content(webpage,encodage):
    from bs4 import  BeautifulSoup

    from urllib.request import urlopen
    from nltk.corpus import stopwords
    page = urlopen(webpage).read()
    page=page.decode(encodage)
    result = BeautifulSoup(page, "lxml")

    #print(result.get_text())
    list=result.get_text().lower()
    from nltk.tokenize import sent_tokenize, word_tokenize
    list = word_tokenize(text=list, language='french', preserve_line="true")
    stopWords = set(stopwords.words('french'))
    wordsFiltered=[]
    import re
    for w in list:
        if w not in stopWords:
            wordsFiltered.append(w)
            s=re.match("[A-Za-zèùçà']+",w)
            if  s:
                 print("french:",w)

    #print(list)
def clear_content2(webpage, encodage):
        from bs4 import BeautifulSoup
        from urllib.request import urlopen
        from nltk.corpus import stopwords
        from nltk.tokenize import sent_tokenize, word_tokenize
        page = urlopen(webpage).read()
        page = page.decode(encodage)

        result = BeautifulSoup(page, "lxml")

        # print(result.get_text())
        list = result.get_text().lower()
        list=word_tokenize(text=list,language='arabic',preserve_line="true")
        #stopwords of any language
        stopWords = set(stopwords.words('arabic'))
        import re
        wordsFiltered = []

        for w in list:
            if w not in stopWords:
                wordsFiltered.append(w)
                #arabic character in UNICODE
                s = re.match("[\u0621-\u064A\u0660-\u0669 ]+", w)
                if s:
                    print("arabe:", w)





def readarabic():

    from nltk.tokenize import sent_tokenize,word_tokenize

    text = u'انا حامل'
    print(word_tokenize(text))


import nltk
nltk.download('punkt')
#inverse_reading("hello.txt")
#find_whwords("austen-emma.txt")
#clear_content("http://www.usthb.dz/","utf-8")

readarabic()
clear_content2("https://ar.wikipedia.org/wiki/%D9%81%D9%84%D8%B3%D9%81%D8%A9_%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA","utf")
#import nltk
#print(nltk.corpus.gutenberg.raw("austen-emma.txt").read())

