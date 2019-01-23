        print("########## fonction #############")
        texte = self.textEdit_16.toPlainText()
        lng_moy = longeurMoyenneWord(texte)
        fd = frequenceDist(texte)

        print("longeur moyenne est ", lng_moy)

        self.textEdit_11.setText(str("stats"))

        lg = "- longeur moyenne des mots est : " + lng_moy + "\n" + "- Distribution de fréquence est : \n"

        self.textEdit_11.append(str(lg))

        for (w,freq) in fd:
            t = w + " -> " + freq + "\n"
            print(w, "->", freq)
            self.textEdit_11.append(str(t))

        self.textEdit_11.append(str("les bigrams sont \n"))

        fd_bg = most_common_bigram(texte)

        for (w,freq) in fd_bg:
            t = w + " -> " + freq + "\n"
            print(w, "->", freq)
            self.textEdit_11.append(str(t))

        nb = self.textEdit_12.toPlainText()
        fd_lt = frequence_lessThen(texte,int(nb))
        t = "fréquence inférieur à " + nb + " : \n "
        self.textEdit_11.append(str(t))

        for (w,freq) in fd_lt:
            t = w + " -> " + freq + "\n"
            print(w, "->", freq)
            self.textEdit_11.append(str(t))