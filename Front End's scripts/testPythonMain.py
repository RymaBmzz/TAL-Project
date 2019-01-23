import math
import sys
import codecs
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from xml.dom import minidom

from exemplesRetrieval import initializingJar,lemmatize

from PyQt5.QtCore import  QDir, Qt
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog,
			     QLabel, QMainWindow, QMenu, QMessageBox,
			     QScrollArea, QSizePolicy, QPushButton,
                  QTableWidget,QTableWidgetItem,
                             QWidget, QDateTimeEdit, qApp)
import os
import xml.etree.cElementTree as ET
import testTagUpdate as tagUp
from xml.etree.cElementTree import parse
from exemplesRetrieval import initializingJar,lemmatize
import unicodedata
import pickle
from cleaning import removingTachkil
from statistics_last import *

from testPython import * #--importation du fichier de description GUI---

liste_paths = []
liste_length = []
length = 0

liste_defs = []

object = initializingJar()

# dictPreIslamic = tagUp.load_dictionary("Contexts/contextPreIslamic.pkl")
# print("one loaded")
# dictIslamic = tagUp.load_dictionary("Contexts/contextIslamic.pkl")
# print("two loaded")
# dictUmayyad = tagUp.load_dictionary("Contexts/contextUmayyad.pkl")
# print("three loaded")
# dictAbbasid = tagUp.load_dictionary("Contexts/contextAbbasid.pkl")
# print("four loaded")
# dictMiddleAges = tagUp.load_dictionary("Contexts/contextMiddleAges.pkl")
# print("five loaded")
# dictModern = tagUp.load_dictionary("Contexts/contextModern.pkl")
# print("six loaded")
# dictQuran = tagUp.load_dictionary("Contexts/contextQuran.pkl")
# print("quran loaded")
        
class TAL_Projet(QMainWindow, Ui_MainWindow):

    #self represente la classe qui est une portion fixe !
    def __init__(self, parent=None):
        super(TAL_Projet,self).__init__(parent)
        self.setupUi(parent) #obligatoire
        QMainWindow.setFixedSize(self,1141, 967)
        self.center

        # Fonction pour ajuster les tableau à la taille de leurs containers
        header = self.tableWidget_Corpus.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget_Corpus.selectionMode()  #setSelectionMode(QAbstractItemView.SingleSelection)

        self.textEditAsr6_2.setAlignment(Qt.AlignRight)
        self.textEditAsr1.setAlignment(Qt.AlignRight)
        self.textEditAsr3.setAlignment(Qt.AlignRight)
        self.textEditAsr6.setAlignment(Qt.AlignRight)
        self.textEditAsr2_2.setAlignment(Qt.AlignRight)
        self.textEditAsr4.setAlignment(Qt.AlignRight)
        self.textEditAsr7.setAlignment(Qt.AlignRight)
        self.textEditAsr5.setAlignment(Qt.AlignRight)

        self.pushButton_show.clicked.connect(self.fonction1)

        #yourTableWidget.itemClicked.connect(handle_item_clicked)
        self.tableWidget_Corpus.itemClicked.connect(self.handle_item_clicked)

        self.pushbutton.clicked.connect(self.chercher)

        self.button_visualisation1.clicked.connect(self.validerAutomatique)
        self.pushButton_3.clicked.connect(self.validerManuel)
        self.pushButton4.clicked.connect(self.getAllDefs)
#        self.pushButton.clicked.connect(self.stats_text)
#        self.textEdit_12.setText(str(1))
        
        # statistics
        self.pushButton_2.clicked.connect(self.compare_diversity)
        self.pushButton_4.clicked.connect(self.most_common_words)
        self.pushButton_8.clicked.connect(self.freqWordPerPeriod)
        self.pushButton_5.clicked.connect(self.chooseText)
        self.pushButton_6.clicked.connect(self.getLongMoy)
        self.pushButton_7.clicked.connect(self.freqDistWords)
        self.pushButton_9.clicked.connect(self.bigrams)
        
        self.button_visualisation1_2.clicked.connect(self.validated_words)
        
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
    def validated_words(self):
        self.textEditAsr6_2.clear()
        
        s = "الكلمات المؤكدة "
        self.textEditAsr6_2.append(str(s))
        
# =============================================================================
#         l1 = ["coucu", "cicijl", "ckjlk"]
#         l2 = ["1", "سلام", "أهلا"]
#         
#         for w in l1:
#             self.textEditAsr6_2.append(str(w))
#             
#         self.textEditAsr6_2.append(str(l2))
# =============================================================================
        nb_words = 0
        for nb in range(1,29):
            xmlfile = "Dicts/HistDictionary" + str(nb)
            print("xml file => ",xmlfile)
            tree = parse(xmlfile + ".xml")
            w = tree.findall("./word[@value='valid']")
            
            validated_entry=set([el.get("name") for el in w if len(w)>0])            
            if len(validated_entry) != 0:
                print(validated_entry)
                for word in validated_entry:
                    self.textEditAsr6_2.append(str(word))
                    nb_words += 1
        s2 = "لا يوجد كلمات مؤكدة"
        if nb_words == 0:
            self.textEditAsr6_2.append(str(s2))


    def bigrams(self):
        self.textEdit_21.clear()
        print("hlkj")
        # get number of common words
        n = self.spinBox_3.value()

        path = self.textEdit_13.toPlainText()
        
        if path == "":
            QMessageBox.warning(self,  "تحذير","الرجاء إختيار النص")
            return
        
        text = codecs.open(path, "r", encoding="utf-8").read()

        fd = most_common_bigram(text)
        for word,freq in fd[:n]:
            text = word, " => ", freq
            print(text)
            self.textEdit_21.append(str(text))


    def freqDistWords(self):
        self.textEdit_18.clear()
        print("hlkj")
        # get number of common words
        n = self.spinBox_2.value()

        path = self.textEdit_13.toPlainText()
        
        if path == "":
            QMessageBox.warning(self,  "تحذير","الرجاء إختيار النص")
            return
        
        text = codecs.open(path, "r", encoding="utf-8").read()

        fd = frequenceDist(text) # is ordered
        for word,freq in fd[:n]:
            text = word, " => ", freq
            print(text)
            self.textEdit_18.append(str(text))


    def getLongMoy(self):
        path = self.textEdit_13.toPlainText()
        
        if path == "":
            QMessageBox.warning(self,  "تحذير","الرجاء إختيار النص")
            return
        
        text = codecs.open(path, "r", encoding="utf-8").read()

        longMoy = longeurMoyenneWord(text)
        roundedLong = round(longMoy, 3)
        print("longeurMoyenneWord : ", roundedLong)

        self.textEdit_17.setText(str(roundedLong))


    def chooseText(self):
        print ("coucou")

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileNames(self,"OpenFile", "./finalCorpus/","Text Files (*.txt)")

        print("file is ", fileName)
        t = str(fileName) + ""
        l = len(t)
        a = l-2
        te = t[2:a]
        self.textEdit_13.setText(str(te))


    def freqWordPerPeriod(self):
        # get chosen asr
        if self.comboBox_5.currentText() == "العصر الجاهلي":
            period1 = "pre-islamic"
        if self.comboBox_5.currentText() == "عصر فجر الإسلام":
            period1 = "islamic"
        if self.comboBox_5.currentText() == "العصر الأموي":
            period1 = "umayyad"
        if self.comboBox_5.currentText() == "العصر العباسي":
            period1 = "abbasid"
        if self.comboBox_5.currentText() == "العصور الوسطى":
            period1 = "middle-ages"
        if self.comboBox_5.currentText() == "العصر الحديث":
            period1 = "modern"
        if self.comboBox_5.currentText() == "القرآن الكريم":
            period1 = "quran"
        
        # get the word
        word = self.textEdit_20.toPlainText()
        if word == "":
            QMessageBox.warning(self,  "تحذير","الرجاء إدخال الكلمة")
            return

        print("asr is ", period1, ", and word is ", word)
        freqWord = frequenWordPerPeriod(word, period1)
        print("freq of : ", word, " is : ", freqWord)
        self.textEdit_19.setText(str(freqWord))
        
        
    def most_common_words(self):
        self.textEdit_14.clear()
        # get chosen asr
        if self.comboBox_4.currentText() == "العصر الجاهلي":
            period1 = "pre-islamic"
        if self.comboBox_4.currentText() == "عصر فجر الإسلام":
            period1 = "islamic"
        if self.comboBox_4.currentText() == "العصر الأموي":
            period1 = "umayyad"
        if self.comboBox_4.currentText() == "العصر العباسي":
            period1 = "abbasid"
        if self.comboBox_4.currentText() == "العصور الوسطى":
            period1 = "middle-ages"
        if self.comboBox_4.currentText() == "العصر الحديث":
            period1 = "modern"
        if self.comboBox_4.currentText() == "القرآن الكريم":
            period1 = "quran"
            
        # get number of common words
        n = self.spinBox.value()
        
        print("asr is ", period1, " nb is ", n)
        t = ""
        fd = most_common(period1)
        sorted_fd = sorted(fd.items(), key=itemgetter(1), reverse=True)
        for word,freq in sorted_fd[:n]:
            text = word, " => ", freq
            print(text)
            self.textEdit_14.append(str(text))
            
        
        
    def compare_diversity(self):
        # choose the fisrt period
        if self.comboBox_2.currentText() == "العصر الجاهلي":
            period1 = "pre-islamic"
        if self.comboBox_2.currentText() == "عصر فجر الإسلام":
            period1 = "islamic"
        if self.comboBox_2.currentText() == "العصر الأموي":
            period1 = "umayyad"
        if self.comboBox_2.currentText() == "العصر العباسي":
            period1 = "abbasid"
        if self.comboBox_2.currentText() == "العصور الوسطى":
            period1 = "middle-ages"
        if self.comboBox_2.currentText() == "العصر الحديث":
            period1 = "modern"
        if self.comboBox_2.currentText() == "القرآن الكريم":
            period1 = "quran"
            
        # choose the second period
        if self.comboBox_3.currentText() == "العصر الجاهلي":
            period2 = "pre-islamic"
        if self.comboBox_3.currentText() == "عصر فجر الإسلام":
            period2 = "islamic"
        if self.comboBox_3.currentText() == "العصر الأموي":
            period2 = "umayyad"
        if self.comboBox_3.currentText() == "العصر العباسي":
            period2 = "abbasid"
        if self.comboBox_3.currentText() == "العصور الوسطى":
            period2 = "middle-ages"
        if self.comboBox_3.currentText() == "العصر الحديث":
            period2 = "modern"
        if self.comboBox_3.currentText() == "القرآن الكريم":
            period2 = "quran"
            
        print ("period1 is ", period1, " and period2 is ", period2)
        n = compare_diversity(period1, period2)
        rounded_n = round(n,3)
        print ("diversity is " , rounded_n)
        self.textEdit_22.setText(str(rounded_n))
        


#    def stats_text(self):
#        # récupérer le text
#        self.textEdit_11.setText(str("stats"))
#        nb = self.textEdit_12.toPlainText()
#        if self.comboBox.currentText() == "العصر الجاهلي":
#            period = "pre-islamic"
#        if self.comboBox.currentText() == "عصر فجر الإسلام":
#            period = "islamic"
#        if self.comboBox.currentText() == "العصر الأموي":
#            period = "umayyad"
#        if self.comboBox.currentText() == "العصر العباسي":
#            period = "abbasid"
#        if self.comboBox.currentText() == "العصور الوسطى":
#            period = "middle-ages"
#        if self.comboBox.currentText() == "العصر الحديث":
#            period = "modern"
#        if self.comboBox.currentText() == "القرآن الكريم":
#            period = "quran"
#
#        graph(period,int(nb))


    def fonction1(self):
        liste_paths.clear()
        length = 0
        self.tableWidget_Corpus.clear()
        self.textEdit_16.clear()

#        print("lllll")

        choix = self.comboBox.currentText()
        listAsr = ["abbasid", "islamic", "middle-ages", "modern", "pre-islamic", "quran", "umayyad"]


        if choix == "العصر الجاهلي":
            getAst = listAsr[4]
        if choix == "عصر فجر الإسلام":
            getAst = listAsr[1]
        if choix == "العصر الأموي":
            getAst = listAsr[6]
        if choix == "العصر العباسي":
            getAst = listAsr[0]
        if choix == "العصور الوسطى":
            getAst = listAsr[2]
        if choix == "العصر الحديث":
            getAst = listAsr[3]
        if choix == "القرآن الكريم":
            getAst = listAsr[5]
            print("************* HERE*******\n")
            path1 = "./finalCorpus/" + getAst + "/books"
            print("About quran -> ", os.path.isdir("./finalCorpus/" + getAst + "/books"))
    
            count = 0
            for surat in os.listdir(path1):
                print("\n*****Books****", surat)
                pathFolder = path1 + '/' + surat
                count +=1
                    
            self.tableWidget_Corpus.setRowCount(count)
            self.tableWidget_Corpus.setHorizontalHeaderLabels(["سور القرآن الكريم"])
    
            i = 0

            for file in os.listdir(path1):
                liste_paths.append(file)
                length += 1
#                liste_paths = [file] + liste_paths # add to begining

                mot = " القرآن الكريم - : " + file
                self.tableWidget_Corpus.setItem(i, 0, QTableWidgetItem(str(mot)))
                i += 1
                
            return 0
                

        path1 = "./finalCorpus/" + getAst + "/books"
        print("About books -> ", os.path.isdir("./finalCorpus/" + getAst + "/books"))

        count = 0
        for folder in os.listdir(path1):
            print("\n*****Books****", folder)
            pathFolder = path1 + '/' + folder
            for file in os.listdir(pathFolder):
                count +=1
                
        print("\n\n")
        
        path2 = "./finalCorpus/" + getAst + "/poetry"
        print("About books -> ", os.path.isdir("./finalCorpus/" + getAst + "/poetry"))        
        
        count2 = 0
        for folder in os.listdir(path2):
            print("\n****Poetry*****", folder)
            pathFolder = path2 + '/' + folder
            for file in os.listdir(pathFolder):
                count2 +=1
                
        countG = count + count2
        
        self.tableWidget_Corpus.setRowCount(countG)
        self.tableWidget_Corpus.setHorizontalHeaderLabels(["المؤلفات و المؤلفون"])

        i = 0
        for folder in os.listdir(path1):
#            print("\n*********", folder)
            pathFolder = path1 + '/' + folder
            for file in os.listdir(pathFolder):
                pathFile = pathFolder + '/' + file
                liste_paths.append(pathFile)
                length += 1
#                liste_paths = [pathFile] + liste_paths # add to begining
                nameFile = file.split(".")

                mot = " من الكاتب - " + folder + " - : " + nameFile[0]
                self.tableWidget_Corpus.setItem(i, 0, QTableWidgetItem(str(mot)))
                i += 1

        for folder in os.listdir(path2):
#            print("\n*********", folder)
            pathFolder = path2 + '/' + folder
            for file in os.listdir(pathFolder):
                pathFile = pathFolder + '/' + file
                liste_paths.append(pathFile)
                length += 1
#                liste_paths = [pathFile] + liste_paths # add to begining
                nameFile = file.split(".")

                mot = " من الشاعر - " + folder + " - : " + nameFile[0]
                self.tableWidget_Corpus.setItem(i, 0, QTableWidgetItem(str(mot)))
                i += 1
                
        liste_length.append(length)

        # a = []
        # for indx in self.tableWidget_Corpus.selectedIndexes():
        #     print(indx.row())
        #     a.append(indx.row())
        #
        # index = a[0]
        #
        # f = open(liste_paths[index], encoding="utf-8").read()
        # print(f)
        # self.textEdit_16.setText(str(f) + "******\n\n\n\n")

        # for folder in os.listdir(path1):
        #     print("\n*********",folder)
        #     pathFolder = path1+'/'+folder
        #     for file in os.listdir(pathFolder):
        #         pathFile = pathFolder+'/'+file
        #         f = open(pathFile, encoding="utf-8").read()
        #         print(pathFile)
        #         self.textEdit_16.setText(str(f) + "******\n\n\n\n")

        # f = open("C:/Users/USER/Documents/Master2/TAL/finalCorpus/islamic/books/أبو ذر القلموني/ماذا تعرف عن الله.txt", encoding="utf-8").read()
        # print("file ************\n", f)
        # self.textEdit_16.setText(str(f) + "******\n\n\n\n")

        # print(self.tableWidget_Corpus.itemAt(a[0],a[0]).text(), " choix is ", choix)

        # print(a[0], " type of a ", type(a))

        # a = []
        # for index in self.tableWidget_Corpus.selectedIndexes():
        #     a.append(index.row())
        #
        # print(self.tableWidget_Corpus.itemAt(a[0],a[0]).text())

        # print(a[0], " type of a ", type(a))


    def handle_item_clicked(self):
        a = []
        for indx in self.tableWidget_Corpus.selectedIndexes():
            print("========== index.row ",indx.row())
            a.append(indx.row())
            
        index = a[0]
            
#        if len(liste_length) == 1: # 1st clic
#            print("here 1")
#            index = a[0]
#        else:
#            print("here 2")
#            val = len(liste_length) - 2 # avant dernier
#            last_leng = liste_length[val]
#            index = last_leng + a[0]
        
        
        if self.comboBox.currentText() == "القرآن الكريم":
            path = "./finalCorpus/quran/books/"
            print("before path is for quran ", path)
            path2 = path + str(liste_paths[index])
            print("after path is for quran ", str(path2))
            f = codecs.open(str(path2), "r", encoding="utf-8").read()
#            print(f)
            self.textEdit_16.setText(str(f))

        else :
            print("liste_paths[index] is -> ", liste_paths[index])

    #        f = open(liste_paths[index], encoding="utf-8").read()
            f = codecs.open(liste_paths[index], "r", encoding="utf-8").read()
#            print(f)
            self.textEdit_16.setText(str(f))
        


    # def chercher(self):
    #
    #     print("yeyeess")
    #     mot = self.textEdit_mot1.toPlainText()
    #     # print("mot == ",mot)
    #     # defs = tagUp.get_definition_from_dict(mot)
    #     # print("nooo")
    #     # for definition in defs:
    #     #     print(definition)
    #     #     self.textEdit.append(str(definition))
    #
    #     examples = tagUp.get_examples_from_contexte(mot,object,dictPreIslamic,dictIslamic,dictUmayyad,dictMiddleAges,dictAbbasid,dictModern,dictQuran)
    #     for (numAsr, v) in examples.items():
    #         # print("asr= ", k, "value: ", v)
    #         if numAsr == 1:
    #             print("Asr = ",numAsr," => ",v)
    #             self.textEditAsr1.append(str(v))
    #         if numAsr == 2:
    #             print("Asr = ", numAsr, " => ", v)
    #             self.textEditAsr2_2.append(str(v))
    #         if numAsr == 3:
    #             print("Asr = ", numAsr, " => ", v)
    #             self.textEditAsr3.append(str(v))
    #         if numAsr == 4:
    #             print("Asr = ", numAsr, " => ", v)
    #             self.textEditAsr4.append(str(v))
    #         if numAsr == 5:
    #             print("Asr = ", numAsr, " => ", v)
    #             self.textEditAsr5.append(str(v))
    #         if numAsr == 6:
    #             print("Asr = ", numAsr, " => ", v)
    #             self.textEditAsr6.append(str(v))
    #         if numAsr == 7:
    #             print("Asr = ", numAsr, " => ", v)
    #             self.textEditAsr7.append(str(v))

    def chercher(self):
        self.textEditAsr1.clear()
        self.textEditAsr2_2.clear()
        self.textEditAsr3.clear()
        self.textEditAsr4.clear()
        self.textEditAsr5.clear()
        self.textEditAsr6.clear()
        self.textEditAsr7.clear()
        
        mot = self.textEdit_mot1.toPlainText()
        # print("mots est ", mot)
        # Pour les définitions du mot
        # hist = minidom.parse('C:/Users/USER/Documents/Master2/TAL/HistDictionary2.xml')
        if mot == "":
            QMessageBox.warning(self,  "تحذير","الرجاء إدخال الكلمة")
            return
        namebalise = removingTachkil(mot)
        namebal = lemmatize(object, namebalise)
        numdict = tagUp.get_numL_dictXML(namebal[0])  # get indice of the dict corresponding to the letter that starts with
        nb = numdict[0]
        xmlfile = "Dicts/HistDictionary" + str(nb)
        ###################
        tree = ET.parse(xmlfile+ ".xml")
        root = tree.getroot()
        # Récuperer le premier mot
        dicts = root.getchildren()
        w = tree.findall("./word[@name='" + namebal[0] + "']")
        if len(w) > 0:
            valeurValid  = w[0].get('value')
            if valeurValid == 'not valid':
                self.textEdit_15.setText("غير مأكد")
            if valeurValid == 'validate':
                self.textEdit_15.setText("مأكد")
            # dicts = w.getchildren()
            # print(w)
            # print(dicts[1].attributes['name'].value)
            # wordBalise = dicts.get(name=mot)
            # dicts = root[0].getchildren()
            # print("baliiise = ",wordBalise)
            definitions = ""
            self.textEdit.clear()
            for ele in w:
                # Récuperer les définitions
                defs = ele[0].getchildren()
                # print("defs = ",defs)
                for definition in defs:
                    definit = definition.getchildren()
                    for d in definit:
                        # print("def : ",d.text)
                        definitions = d.text 
                        self.textEdit.append(str(definitions))
                    self.textEdit.append("*")
                        
                

            # Récuperer les contextes same thing seulement 'ele[1]
            contextes = ele[1].getchildren()
            # print("ka = ",contextes)
            numAsr = 1
            for context in contextes:
                # get les exemples
                cont = context.getchildren()
#                    print("content = ", cont)
#                    asrName = "textEditAsr"+str(numAsr)
                # print("asr = ",asrName)
                for c in cont:
#                        print("contuuuuuuuuus = ",c.text)
                    if c.text != None:
                        if numAsr == 1:
                            self.textEditAsr1.append(str(c.text))
                        if numAsr == 2:
                            self.textEditAsr2_2.append(str(c.text))
                        if numAsr == 3:
                            self.textEditAsr3.append(str(c.text))
                        if numAsr == 4:
                            self.textEditAsr4.append(str(c.text))
                        if numAsr == 5:
                            self.textEditAsr5.append(str(c.text))
                        if numAsr == 6:
                            self.textEditAsr6.append(str(c.text))
                        if numAsr == 7:
                            self.textEditAsr7.append(str(c.text))
                    else:
                        print("Egaaale NOOONEE")
                numAsr += 1
        else:
            QMessageBox.warning(self,  "تحذير","لا يوجد تعريف للكلمة المطلوبة")
            return


    def validerAutomatique(self):
        # {'1': 'pre-islamic', '2': 'islamic', '3': 'umayyad', '4': 'abbasid',
        #  '5': 'middle_ages', '6': 'modern', '7': 'quran'}
        # definition = self.textEdit.toPlainText()
        
        self.textEdit_15.setText("مأكد")
        print("Automatique validé")
        dictContextes2 = {}
        if self.textEditAsr1.toPlainText() !="":
            dictContextes2['1'] = self.textEditAsr1.toPlainText()
            print("Asr ",self.textEditAsr1.toPlainText())

        if self.textEditAsr2_2.toPlainText() != "":
            dictContextes2['2'] = self.textEditAsr2_2.toPlainText()
            print("Asr ",self.textEditAsr2_2.toPlainText())

        if self.textEditAsr3.toPlainText() != "":
            dictContextes2['3'] = self.textEditAsr3.toPlainText()
            print("Asr ",self.textEditAsr3.toPlainText())

        if self.textEditAsr4.toPlainText() != "":
            dictContextes2['4'] = self.textEditAsr4.toPlainText()
            print("Asr = ",self.textEditAsr4.toPlainText())
        if self.textEditAsr5.toPlainText() != "":
            dictContextes2['5'] = self.textEditAsr5.toPlainText()
            print("Asr ",self.textEditAsr5.toPlainText())
        if self.textEditAsr6.toPlainText() != "":
            dictContextes2['6'] = self.textEditAsr6.toPlainText()
            print("Asr ",self.textEditAsr6.toPlainText())
        if self.textEditAsr7.toPlainText() != "":
            dictContextes2['7'] = self.textEditAsr7.toPlainText()
            print("Asr ",self.textEditAsr7.toPlainText())
        kalima = self.textEdit_mot1.toPlainText()

        defs = self.textEdit.toPlainText()
        definitions = defs.split('*')

        tagUp.add_entryToDict(definitions,kalima,dictContextes2)
#        for i in definitions:
#            print("def ",i)
            
        QMessageBox.information(self, "Information", "تمت الإضافة")
        return

        # print(definition)

    def validerManuel(self):
        # {'1': 'pre-islamic', '2': 'islamic', '3': 'umayyad', '4': 'abbasid',
        #  '5': 'middle_ages', '6': 'modern', '7': 'quran'}
        kalima = self.textEdit_2.toPlainText()
        if kalima == "":
            QMessageBox.warning(self,  "تحذير","الرجاء إدخال الكلمة")
            return
        
        print("kalimuus = ",kalima,"\n")
        definition = self.textEdit_2.toPlainText()
        liste_defs.append(definition)
        dictContextes = {}
        if self.textEdit_4.toPlainText() !="":
            dictContextes['1'] = self.textEdit_4.toPlainText()
            print(self.textEdit_4.toPlainText())
        if self.textEdit_7.toPlainText() != "":
            dictContextes['4'] = self.textEdit_7.toPlainText()
            print(self.textEdit_7.toPlainText())
        if self.textEdit_5.toPlainText() != "":
            dictContextes['2'] = self.textEdit_5.toPlainText()
            print(self.textEdit_5.toPlainText())

        if self.textEdit_8.toPlainText() != "":
            dictContextes['5'] = self.textEdit_8.toPlainText()
            print(self.textEdit_8.toPlainText())
        if self.textEdit_9.toPlainText() != "":
            dictContextes['6'] = self.textEdit_9.toPlainText()
            print(self.textEdit_9.toPlainText())
        if self.textEdit_10.toPlainText() != "":
            dictContextes['7'] = self.textEdit_10.toPlainText()
            print(self.textEdit_10.toPlainText())
        if self.textEdit_6.toPlainText() != "":
            dictContextes['3'] = self.textEdit_6.toPlainText()
            print(self.textEdit_6.toPlainText())
        tagUp.add_entryToDict(liste_defs,kalima,dictContextes)
        
        QMessageBox.information(self, "Information", "تمت الإضافة")
        return

#        for defi in liste_defs:
#            print("def : ",defi)



    def getAllDefs(self):
        definition = self.textEdit_3.toPlainText()
        liste_defs.append(definition)
        self.textEdit_3.clear()






#fonctopn principale executant l'application Qt
def main(args):
    a = QApplication(args)
    f = QMainWindow()
    c = TAL_Projet(f)
    f.show()
    r = a.exec_()
    return r

if __name__=="__main__":
    main(sys.argv)
