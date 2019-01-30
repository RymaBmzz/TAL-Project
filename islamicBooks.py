from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import webbrowser
import re
import os
import sys
headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
def get_authorNames(url):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
    soup = BeautifulSoup(r.content)
    soup.encode("utf-8")
    listAuthors = []
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        listAuthors.append(''.join(row.findAll('td')[2].contents))
    listAuthors = listAuthors[1:]
    return listAuthors
def google(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q +' wiki'+ '&ie=utf-8&oe=utf-8'
    r = s.get(url, headers=headers_Get)
    soup = BeautifulSoup(r.content)
    output = []
    for searchWrapper in soup.findAll('a'): #this line may change in future based on google's web page structure
        li = searchWrapper.get('href')
        try:
            if "ar.wikipedia" in li:
                return li
        except (TypeError, AttributeError):
            continue
    return output
def get_period(author):
    try:
        r = requests.get("" + google(author))
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
    soup = BeautifulSoup(r.content, "lxml")
    soup.encode("utf-8")
    for posts in soup.findAll('table', {'class': re.compile("^infobox")}):
        for tr in posts.findAll('tr'):
            info = [td for td in tr.stripped_strings]
            if len(info) == 0:
                continue
            elif "الوفاة" in info[0]:
                print(info)
                break
            else:
                continue
    if len(info)<=1:
        for posts in soup.findAll('table', {'class': re.compile("^infobox")}):
            for tr in posts.findAll('tr'):
                info = [td for td in tr.stripped_strings]
                if len(info) == 0:
                    continue
                elif "الميلاد" in info[0]:
                    break
                else:
                    continue

    print(info)
    dates = " ".join(info)
    d = re.findall("[0-9]+[\s]*هـ", dates)
    print(d)
    if len(d) == 0:
        d=re.findall("[0-9]{3,4}",dates)
        print(d)
        d1="".join(d)
        if(d1.isdigit()):
            date = int(d[0])
        else:
            date=int(d[0][:-1])
        if(date):
            if date<610:
                return "pre-islamic"
            if 610<=date < 661:
                return "isalmic"

            if date >= 661 and date <= 749:
                return "umayyad"

            if date > 749 and date <=  1258:
                return "abbasid"

            if date >  1258 and date <=  1798:
                return "middle-ages"
            if date>1798:
                return "hadith"
    else:
        date = int(d[0][:-2])
        if (date):
            if date < 41:
                return "isalmic"

            if date >= 41 and date <= 132:
                return "umayyad"

            if date > 132 and date <= 656:
                return "abbasid"

            if date > 656 and date <= 1213:
                return "middle-ages"
            if date > 1213:
                return "hadith"
if not os.path.exists("islamicBooks"):
    os.makedirs("islamicBooks")
if not os.path.exists("islamicBooks/pre-islamic"):
    os.makedirs("islamicBooks/pre-islamic")
if not os.path.exists("islamicBooks/umayyad"):
    os.makedirs("islamicBooks/umayyad")
if not os.path.exists("islamicBooks/abbasid"):
    os.makedirs("islamicBooks/abbasid")
if not os.path.exists("islamicBooks/middle-ages"):
    os.makedirs("islamicBooks/middle-ages")
listCat = ['qbook','hadeth','ageda','asol','tarekh','adab','amma']
for cat in listCat:
    print(cat)
    try:
        r= requests.get("http://www.islamicbook.ws/"+cat+"/")
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
    soup = BeautifulSoup(r.content)
    soup.encode("utf-8")
    nextPages = []
    count = 0
    k=0
    for link2 in soup.findAll('a', attrs={'href': re.compile("(.+?)\.html$")}):
        count+=1
        li=link2.get('href')
        print(li)
        if(li.startswith(cat)):
            nextPages.append(li)
            print(li)
        elif li.startswith('..'):
            continue
        else:
            try:
                r2= requests.get("http://www.islamicbook.ws/"+cat+"/"+li)
            except requests.exceptions.ConnectionError:
                r2.status_code = "Connection refused"
            soup3 = BeautifulSoup(r2.content, "lxml")
            soup3.encode("utf-8")
            theAuthor = get_authorNames("http://www.islamicbook.ws/"+cat)
            print(theAuthor)
            print("le k ya djma3a",k)
            print(theAuthor[k])
            try:
                period = get_period(theAuthor[k])
            except BaseException as Exception:
                k+=1
                continue
            k+=1
            if(k>=len(theAuthor)):
                break
            if not os.path.exists("islamicBooks/"+period+"/"+li):
                os.makedirs("islamicBooks/"+period+"/"+li)
            f = open("islamicBooks/"+period+"/"+li+str(count)+".txt","w+")
            for rows in soup3.find_all('div',attrs={'id': "content"}):
                s4=rows.text
                f.write(s4)
            i=0
            for links4 in soup3.find_all('a',attrs={'href': re.compile("(.+?)\.html$")}):
                if i ==0:
                    continue
                try:
                    r2 = requests.get("http://www.islamicbook.ws/" + cat + "/" + links4)
                except requests.exceptions.ConnectionError:
                    r2.status_code = "Connection refused"
                soup3 = BeautifulSoup(r2.content, "lxml")
                soup3.encode("utf-8")
                for rows in soup3.find_all('div',attrs={'id': "content"}):
                    s4 = rows.text
                    f.write(s4)
                i+=1
            f.close()
    for page in nextPages:
        try:
            r3= requests.get("http://www.islamicbook.ws/"+cat+"/"+page)
        except requests.exceptions.ConnectionError:
            r3.status_code = "Connection refused"
        soup3 = BeautifulSoup(r.content)
        soup3.encode("utf-8")
        c=0
        for link2 in soup3.findAll('a', attrs={'href': re.compile("(.+?)+\.html")}):
            next = link2.get("href")
            count+=1
            try:
                r2 = requests.get("http://www.islamicbook.ws/" + cat + "/" + next)
            except requests.exceptions.ConnectionError:
                r2.status_code = "Connection refused"
            soup3 = BeautifulSoup(r2.content, "lxml")
            soup3.encode("utf-8")
            theAuthor = get_authorNames(next)
            try:
                period = get_period(theAuthor[c])
            except BaseException as Exception:
                c+=1
                continue
            c+=1
            if (c >= len(theAuthor)):
                break
            if not os.path.exists("islamicBooks/" + period + "/" + next):
                os.makedirs("islamicBooks/" + period + "/" + next)
            f = open("islamicBooks/" + period + "/" + next + str(count) + ".txt", "w+")
            for rows in soup3.find_all('div',attrs={'id': "content"}):
                s4 = rows.text
                f.write(s4)
            i = 0
            for links4 in soup3.find_all('a', attrs={'href': re.compile("(.+?)\.html$")}):
                if i == 0:
                    continue
                try:
                    r2 = requests.get("http://www.islamicbook.ws/" + cat + "/" + links4)
                except requests.exceptions.ConnectionError:
                    r2.status_code = "Connection refused"
                soup3 = BeautifulSoup(r2.content, "lxml")
                soup3.encode("utf-8")
                for rows in soup3.find_all('div', attrs={'id': "content"}):
                    s4 = rows.text
                    f.write(s4)
                i += 1
            f.close()