from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import webbrowser
import re
import os

#url = "https://www.almaany.com/ar/dict/ar-ar/معجم/"
str="djahili"
ListTimes=['cat-poets-pre-islamic-period','cat-poets-abbasid-era','cat-poets-ottoman-era','cat-poets-umayyad-era','cat-poets-mamluk-era','cat-poets-Islamic-era','cat-poets-ayubi-era','cat-poets-veteran','cat-poets-andalusian-era']
for time in ListTimes:
                                                                                                                                                                                                                                                        os.mkdir(time)
    r = urlopen("https://www.aldiwan.net/"+time)
    soup = BeautifulSoup(r)
    for link in soup.findAll('a',attrs={'href': re.compile("^cat-")}):
        next=link.get('href')
        n = next.split()
        next="".join(n)
        str2=time + "/" +next
        os.mkdir(str2)
        r2=urlopen("https://www.aldiwan.net/"+next)
        soup2 = BeautifulSoup(r2)
        for link2 in soup2.findAll('a', attrs={'href': re.compile("poem[0-9]+\.html")}):
            print(link2.get('href'))
            next2=link2.get('href')
            f=open(str2+"/"+next2+".txt","w+")
            r3= requests.get("https://www.aldiwan.net/" + next2)
            soup3 = BeautifulSoup(r3.content, "lxml")
            for link3 in soup3.find_all('div',attrs={'class':"bet-1"}):
                s4=link3.text
                f.write(s4)
            f.close()