from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time, sys, traceback, random, re, os
import tkinter
from tkinter import filedialog
import sys, re, os
import _thread
import random
from random import randint
import numpy

root = tkinter.Tk()
root.withdraw()

class Validator(QValidator):
    def validate(self, string, pos):
        special = False
        regex = re.compile("^[a-zA-Z0-9 ]*$")
        if(regex.match(string)):
            special = True
        if(special):
            return QValidator.Acceptable, string, pos
        else:
            return QValidator.Invalid, string, pos

class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        self.txtregex = re.compile("^.*\.txt$")
        self.picregex = re.compile("^.*\.(bmp|png|jpg|pdf)$")
        self.imageType = 0

        super(Okno, self).__init__(*args,*kwargs)
        self.setWindowTitle("MegaProgramNaPOD")

        titleText = QLabel()
        titleText.setText("Robi Wszystko")
        titleText.setAlignment(Qt.AlignHCenter)
        titleText.setFont(QFont('times',40))
        titleText.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        emptyLine = QLabel()
        emptyLine.setText("")
        emptyLine.setFont(QFont('times',20))

        authorText = QLabel()
        authorText.setText("Karol Sienkiewicz 140774")
        authorText.setAlignment(Qt.AlignHCenter)
        authorText.setFont(QFont('times',10))
        authorText.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        self.keyPathText = QLabel()
        self.keyPathText.setText("")
        self.keyPathText.setAlignment(Qt.AlignCenter)
        self.keyPathText.setFont(QFont('times',12))
        self.keyPathText.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        self.extraInfo = QLabel()
        self.extraInfo.setText("")
        self.extraInfo.setAlignment(Qt.AlignCenter)
        self.extraInfo.setFont(QFont('times',12))
        self.extraInfo.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        self.fileName = QLineEdit()
        self.validator = Validator()
        self.fileName.setValidator(self.validator)
        self.fileName.setPlaceholderText("Nazwa pliku do zapisu")

        runButton = QPushButton()
        runButton.setText("Zaszyfruj/Odszyfruj")
        runButton.setStyleSheet("background-color : rgb(240,245,245);")
        runButton.clicked.connect(self.runClicked)

        self.timeText = QLabel()
        self.timeText.setText("0")
        self.timeText.setAlignment(Qt.AlignHCenter)
        self.timeText.setFont(QFont('times',12))
        self.timeText.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        selectTextButton = QPushButton()
        selectTextButton.setText("Wybierz plik z tekstem")
        selectTextButton.setMinimumWidth(150)
        selectTextButton.clicked.connect(self.selectTextClicked)

        selectKeyButton = QPushButton()
        selectKeyButton.setText("Wybierz plik z kluczem")
        selectKeyButton.setMinimumWidth(150)
        selectKeyButton.clicked.connect(self.selectKeyClicked)

        generateButton = QPushButton()
        generateButton.setText("Nowa generacja Kodu")
        generateButton.setStyleSheet("background-color : rgb(240,245,245);")
        generateButton.clicked.connect(self.newGenerate)

        generateAndCodeButton = QPushButton()
        generateAndCodeButton.setText("Zaszyfruj/Odszyfruj z generatorem")
        generateAndCodeButton.setStyleSheet("background-color : rgb(240,245,245);")
        generateAndCodeButton.clicked.connect(self.GenerateAndCode)

        digitNumberText = QLabel()
        digitNumberText.setText("TYLKO PRZY NOWEJ GENERACJI: Ile znaków wygenerować:")
        digitNumberText.setFont(QFont('times',12))
        digitNumberText.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        self.digitsNumber = QLineEdit()
        self.digitsNumber.setValidator( QRegExpValidator(QRegExp('^([1-9][0-9]{0,5})|1000000$')) )
        self.digitsNumber.setPlaceholderText("1 - 1000000")

        registerNumberText = QLabel()
        registerNumberText.setText("TYLKO PRZY NOWEJ GENERACJI: Ile rejestrów wykorzystać:")
        registerNumberText.setFont(QFont('times',12))
        registerNumberText.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        self.registerNumber = QLineEdit()
        self.registerNumber.setValidator( QRegExpValidator(QRegExp('^[3-9]|(1[0-7])$')) )
        self.registerNumber.setPlaceholderText("3 - 17")

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(digitNumberText)
        inputLayout.addWidget(self.digitsNumber)
        inputLayout.addWidget(registerNumberText)
        inputLayout.addWidget(self.registerNumber)
        inputLayoutW = QWidget()
        inputLayoutW.setLayout(inputLayout)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(runButton)
        buttonsLayoutW = QWidget()
        buttonsLayoutW.setLayout(buttonsLayout)

        selectLayout = QHBoxLayout()
        selectLayout.addWidget(selectTextButton)
        selectLayout.addWidget(selectKeyButton)
        selectLayoutW = QWidget()
        selectLayoutW.setLayout(selectLayout)

        self.textPathText = QLabel()
        self.textPathText.setText("")
        self.textPathText.setAlignment(Qt.AlignCenter)
        self.textPathText.setFont(QFont('times',12))
        self.textPathText.setStyleSheet("QLabel { color : rgb(30,70,80); }")

        infoButton = QPushButton()
        infoButton.setText("Informacje")
        infoButton.clicked.connect(self.infoClicked)

        helpButton = QPushButton()
        helpButton.setText("Pomoc")
        helpButton.clicked.connect(self.helpClicked)

        Test1Button = QPushButton()
        Test1Button.setText("Test pojedynczych bitów")
        Test1Button.setMinimumWidth(150)
        Test1Button.clicked.connect(self.selectTest1)

        Test2Button = QPushButton()
        Test2Button.setText("Test serii")
        Test2Button.setMinimumWidth(150)
        Test2Button.clicked.connect(self.selectTest2)

        Test3Button = QPushButton()
        Test3Button.setText("Test długiej serii")
        Test3Button.setMinimumWidth(150)
        Test3Button.clicked.connect(self.selectTest3)

        Test4Button = QPushButton()
        Test4Button.setText("Test pokerowy")
        Test4Button.setMinimumWidth(150)
        Test4Button.clicked.connect(self.selectTest4)

        HidePictureButton = QPushButton()
        HidePictureButton.setText("Schowaj w obrazie")
        HidePictureButton.setMinimumWidth(150)
        HidePictureButton.clicked.connect(self.HidePicture)

        SeekPictureButton = QPushButton()
        SeekPictureButton.setText("Znajdź w obrazie")
        SeekPictureButton.setMinimumWidth(150)
        SeekPictureButton.clicked.connect(self.SeekPicture)

        ShowPictureButton = QPushButton()
        ShowPictureButton.setText("Wyświetl obraz")
        ShowPictureButton.setMinimumWidth(150)
        ShowPictureButton.clicked.connect(self.ShowPicture)

        TestLayout = QHBoxLayout()
        TestLayout.addWidget(Test1Button)
        TestLayout.addWidget(Test2Button)
        TestLayout.addWidget(Test3Button)
        TestLayout.addWidget(Test4Button)
        TestLayoutW = QWidget()
        TestLayoutW.setLayout(TestLayout)

        PictureLayout = QHBoxLayout()
        PictureLayout.addWidget(HidePictureButton)
        PictureLayout.addWidget(SeekPictureButton)
        PictureLayout.addWidget(ShowPictureButton)
        PictureLayoutW = QWidget()
        PictureLayoutW.setLayout(PictureLayout)
    
        selectFinLayout = QVBoxLayout()
        selectFinLayout.setAlignment(Qt.AlignCenter)
        selectFinLayout.addWidget(selectLayoutW)
        selectFinLayout.addWidget(TestLayoutW)
        selectFinLayout.addWidget(PictureLayoutW)
        selectFinLayoutW = QWidget()
        selectFinLayoutW.setLayout(selectFinLayout)

        topLayout = QHBoxLayout()
        topLayout.addWidget(infoButton)
        topLayout.addWidget(helpButton)
        topLayoutW = QWidget()
        topLayoutW.setLayout(topLayout)

        mainMenu = QVBoxLayout()
        mainMenu.addWidget(topLayoutW)
        mainMenu.addWidget(titleText)
        mainMenu.addWidget(emptyLine)
        mainMenu.addWidget(self.fileName)
        mainMenu.addWidget(inputLayoutW)
        mainMenu.addWidget(self.extraInfo)
        mainMenu.addWidget(emptyLine)
        mainMenu.addWidget(self.textPathText)
        mainMenu.addWidget(self.keyPathText)
        mainMenu.addWidget(buttonsLayoutW)
        mainMenu.addWidget(generateAndCodeButton)
        mainMenu.addWidget(generateButton)
        mainMenu.addWidget(selectFinLayoutW)
        mainMenu.addWidget(self.timeText)
        mainMenu.addWidget(authorText)

        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        self.setCentralWidget(mainMenuW)

    #Table of prime polinomials
    xorTable = {
        20 : [16,19],
        21 : [18,20],
        22 : [20,21],
        23 : [17,22],
        24 : [19,20,22,23],
        25 : [21,24],
        26 : [19,23,24,25],
        27 : [21,24,25,26],
        28 : [24,27],
        29 : [26,28],
        30 : [23,25,28,29],
        31 : [27,30],
        32 : [24,26,28,29,30,31],
        33 : [19,32],
        34 : [26,27,28,31,32,33],
        35 : [32,34],
        36 : [24,35],
        37 : [30,32,35,36],
        38 : [31,32,36,37],
        39 : [34,38],
        40 : [34,35,36,39],
        41 : [37,40],
        42 : [34,37,38,39,40,41],
        43 : [36,38,39,42],
        44 : [37,38,41,43],
        45 : [40,41,43,44],
        46 : [37,38,39,45],
        47 : [41,46],
        48 : [38,40,43,47],
        49 : [39,48],
        50 : [45,46,47,49],
        51 : [44,47,49,50],
        52 : [48,51],
        53 : [46,50,51,52],
        54 : [45,47,50,53],
        55 : [30,54],
        56 : [48,51,53,55],
        57 : [49,56],
        58 : [38,57],
        59 : [51,54,56,58],
        60 : [58,59]
    }
    
    def runClicked(self):
        self.timeText.setText("Prosimy czekać na koniec pracy programu!")
        _thread.start_new_thread ( Okno.enDeCode, (self,))

    def enDeCode(self):
        if(self.textPathText.text() != "" and self.keyPathText.text() != ""):
            timeStart = 0
            timeStop = 0
            timeStart = time.time()

            fileText = open(self.textPathText.text(),'rb')
            fileCode = open(self.keyPathText.text(),'r',encoding="utf8")
            outputBytes = []
            xorValue = 0
            error = False
            while True:
                readSingleCharacter = fileText.read(1)
                xorValue = 0
                if not readSingleCharacter:
                    break
                for i in range(8):
                    c = fileCode.read(1)
                    if not c:
                        fileSize = os.path.getsize(self.textPathText.text())
                        self.extraInfo.setText("Kod jest zbyt krótki! Powinien mieć conajmniej " + str(8* fileSize) + " znaków!")
                        fileCode.seek(0)
                        c = fileCode.read(1)
                    elif (c != "0" and c != "1"):
                        error = True
                        self.extraInfo.setText("Kod nie jest binarny!")
                        break
                    xorValue += (2**(7-i)) * int(c)
                if error:
                    message = QMessageBox()
                    message.setWindowTitle("Błąd")
                    message.setIcon(QMessageBox.Critical)
                    message.setText("Uwaga: Kod zawierał znaki inne niż 0 i 1!")
                    message.exec_()
                    break
                outputBytes.append( int.from_bytes(readSingleCharacter, byteorder='big', signed=False) ^ xorValue)
            with open("text/"+self.fileName.text()+".txt","wb") as outputfile:
                outputfile.write(bytes(outputBytes))
            fileText.close()
            fileCode.close()

            timeStop = time.time()
            self.timeText.setText("Pracę wykonano w ciągu " + str(timeStop - timeStart) + "s!")
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Uwaga: Nie wybrano plików!")
            message.exec_()

    def selectTextClicked(self):
        filePath = filedialog.askopenfilename()
        if(self.txtregex.match(filePath)):
            self.textPathText.setText(filePath)
        else:
            filePath = ""
            self.textPathText.setText(filePath)
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Wybrany plik nie jest w formacie .txt!")
            message.exec_()

    def selectKeyClicked(self):
        codePath = filedialog.askopenfilename()
        if(self.txtregex.match(codePath)):
            self.keyPathText.setText(codePath)
        else:
            codePath = ""
            self.keyPathText.setText(codePath)
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Wybrany plik nie jest w formacie .txt!")
            message.exec_()

    def infoClicked(self):
        with open("info.txt", "r",encoding="utf8") as f:
            infoText = f.read()
        QMessageBox.about(self, "Informacje", infoText)

    def helpClicked(self):
        with open("help.txt", "r",encoding="utf8") as f:
            helpText = f.read()
        QMessageBox.about(self, "Pomoc", helpText)


    #GENERATOR

    #Initializing all LFSRs
    def initLFSRArray(self,ammount):
        lengthA = []
        for i in range(20,61):
            lengthA.append(i)
        random.shuffle(lengthA)
        arr = []
        for i in range(ammount):
            arr.append([])
            for j in range(lengthA[i]-1):
                arr[i].append(0)
            arr[i].append(1)
        return arr,lengthA[:ammount]

    #Initializing all LFSRs from file
    def initFLFSRArray(self,lines):
        arr = []
        for i in range(1,len(lines)):
            arr.append([])
            for j in range(int(lines[i])-1):
                arr[i-1].append(0)
            arr[i-1].append(1)
        return arr

    #Funktion used to perform a single LFSR operation
    def LFSROperation(self,lfsr): 
        xorIndex = self.xorTable.get(len(lfsr))
        temp = lfsr[xorIndex[0]]
        for i in range(1,len(xorIndex)):
            temp = temp ^ lfsr[xorIndex[i]]
        ret = lfsr.pop()
        lfsr.insert(0,temp)
        return ret

    #Puts values into the outpur array
    def initRun(self,outputs,lfsrA):
        while (outputs[-1] == -1):
            outputs[0] = self.LFSROperation(lfsrA[0])
            outputs[0] = outputs[0] ^ 1
            for i in range(1,len(lfsrA)-1):
                if(outputs[i-1]):
                    break
                outputs[i] = self.LFSROperation(lfsrA[i])
                outputs[i] = outputs[i] ^ outputs[i-1]
            if(outputs[-2]==1):
                outputs[-1] = self.LFSROperation(lfsrA[-1])

    #Performs a number of initial runs to put some 1s into the LFSRs
    def getRunning(self,output,lfsrA):
        howLong = randint(10000,100000)
        for i in range(howLong):
            self.generate(output,lfsrA)
        return howLong

    #Performs a number of initial runs to put some 1s into the LFSRs from file
    def getFRunning(self,output,lfsrA,lines):
        howLong = int(lines[0])
        for i in range(howLong):
            self.generate(output,lfsrA)
        return howLong

    #Generates a single digit
    def generate(self, outputs,lfsrA):
        outputs[0] = self.LFSROperation(lfsrA[0])
        outputs[0] = outputs[0] ^ 1
        for i in range(1,len(lfsrA)-1):
            if(outputs[i-1]):
                continue
            outputs[i] = self.LFSROperation(lfsrA[i])
            outputs[i] = outputs[i] ^ outputs[i-1]
        if(outputs[-2]==1):
            outputs[-1] = self.LFSROperation(lfsrA[-1])
        return str(outputs[-1])

    #Pre Generate
    def newGenerate(self):
        self.timeText.setText("Prosimy czekać na koniec pracy programu!")
        _thread.start_new_thread ( Okno.newGenerateTrue, (self,))

    #Pre Generate from file
    def GenerateAndCode(self):
        filePath = filedialog.askopenfilename()
        if(self.txtregex.match(filePath)):
            file = open(filePath,'r',encoding="utf8")
            Lines = file.readlines()
            for i in range(len(Lines)):
                Lines[i] = Lines[i].replace('\n','')
            self.timeText.setText("Prosimy czekać na koniec pracy programu!")
            _thread.start_new_thread ( Okno.newFGenerateTrue, (self,Lines,))
        else:
            filePath = ""
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            self.timeText.setText("0")
            self.extraInfo.setText("Wybrany plik nie jest w formacie .txt!")
            message.exec_()

    #Generate full text from scratch
    def newGenerateTrue(self):   
        if(self.registerNumber.text() == "" or self.registerNumber.text() == "1"):
            ammount = 3
        else:
            ammount = int(self.registerNumber.text())
   
        if(self.digitsNumber.text() == ""):
            outputSize = 1
        else:
            outputSize = int(self.digitsNumber.text())

        outputs = [-1] * ammount
        lfsrArray,sizes = self.initLFSRArray(ammount)
        self.initRun(outputs,lfsrArray)
        getRun = self.getRunning(outputs,lfsrArray)
        outputStr = ""

        timeStart = 0
        timeStop = 0
        timeStart = time.time()

        for i in range(outputSize):
            outputStr = outputStr + self.generate(outputs,lfsrArray)

        timeStop = time.time()

        f1 = open("code/"+self.fileName.text()+".txt","w")
        f1.write(outputStr)
        f1.close()
        f2 = open("keys/"+self.fileName.text()+".txt","w")
        f2.write(str(getRun))
        for x in sizes:
            f2.write("\n")
            f2.write(str(x))
        f2.close()

        self.timeText.setText("Pracę wykonano w ciągu " + str(timeStop - timeStart) + "s!")

    #Generate full text from file
    def newFGenerateTrue(self,lines):
        ammount = len(lines) -1

        outputs = [-1] * ammount
        lfsrArray = self.initFLFSRArray(lines)
        self.initRun(outputs,lfsrArray)
        self.getFRunning(outputs,lfsrArray,lines)     
   
        if(self.textPathText.text() != ""):
            timeStart = 0
            timeStop = 0
            timeStart = time.time()

            fileText = open(self.textPathText.text(),'rb')
            outputBytes = []
            xorValue = 0
            while True:
                readSingleCharacter = fileText.read(1)
                xorValue = 0
                if not readSingleCharacter:
                    break
                for i in range(8):
                    xorValue += (2**(7-i)) * int(self.generate(outputs,lfsrArray))
                outputBytes.append( int.from_bytes(readSingleCharacter, byteorder='big', signed=False) ^ xorValue)
            with open("text/"+self.fileName.text()+".txt","wb") as outputfile:
                outputfile.write(bytes(outputBytes))
            fileText.close()

            timeStop = time.time()
            self.timeText.setText("Pracę wykonano w ciągu " + str(timeStop - timeStart) + "s!")
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Uwaga: Nie wybrano pliku do zapisu!")
            message.exec_()


    def selectTest1(self):
        if(self.keyPathText.text() != ""):

            if(os.path.getsize(self.keyPathText.text()) < 20000):
                message = QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QMessageBox.Critical)
                message.setText("Zbyt krótki ciąg!")
                message.exec_()
                return 0

            with open(self.keyPathText.text(), 'r') as file:
                n = len(re.findall("1", file.read(20000)))
            if n > 9725 and n < 10275:
                QMessageBox.about(self, "Test pojedynczych bitów", "Test wypadł pozytywnie!\nUzyskano " + str(n) + " jedynek.")
            else:
                 QMessageBox.about(self, "Test pojedynczych bitów", "Test wypadł negatywnie!\nUzyskano " + str(n) + " jedynek.")
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Nie wybrano pliku z kodem!")
            message.exec_()

    def selectTest2(self):
        if(self.keyPathText.text() != ""):

            if(os.path.getsize(self.keyPathText.text()) < 20000):
                message = QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QMessageBox.Critical)
                message.setText("Zbyt krótki ciąg!")
                message.exec_()
                return 0
            
            count = []
            with open(self.keyPathText.text(), 'r') as file:
                n1 = re.findall("1+", file.read(20000))
                file.seek(0)
                n0 = re.findall("0+", file.read(20000))
            for i in range(12):
                count.append(0)
                if(i < 5):
                    for n in n1:
                        if len(n) == i+1:
                            count[i] += 1
                elif(i == 5):
                    for n in n1:
                        if len(n) >= 6:
                            count[i] += 1
                elif(i < 11):
                    for n in n0:
                        if len(n) == i-5:
                            count[i] += 1
                elif(i == 11):
                    for n in n0:
                        if len(n) >= 6:
                            count[i] += 1
            ok = True
            if not (count[0] > 2315 and count[0] < 2685 and count[6] > 2315 and count[6] < 2685 ):
                ok = False
            if not (count[1] > 1114 and count[1] < 1386 and count[7] > 1114 and count[7] < 1386 ):
                ok = False
            if not (count[2] > 527 and count[2] < 723 and count[8] > 527 and count[8] < 723 ):
                ok = False
            if not (count[3] > 240 and count[3] < 384 and count[9] > 240 and count[9] < 384 ):
                ok = False
            if not (count[4] > 103 and count[4] < 209 and count[10] > 103 and count[10] < 209 ):
                ok = False
            if not (count[5] > 103 and count[5] < 209 and count[11] > 103 and count[11] < 209 ):
                ok = False
            if ok:
                QMessageBox.about(self, "Test serii", "Test wypadł pozytywnie!\nPojedyncze 1: " + str(count[0]) + "\nDwie 1: "  + str(count[1]) + "\nTrzy 1: "  + str(count[2]) + "\nCztery 1: "  + str(count[3]) + "\nPięć 1: "  + str(count[4]) + "\nWięcej 1: "  + str(count[5]) + "\nPojedyncze 0: " + str(count[6]) + "\nDwie 0: "  + str(count[7]) + "\nTrzy 0: "  + str(count[8]) + "\nCztery 0: "  + str(count[9]) + "\nPięć 0: "  + str(count[10]) + "\nWięcej 0: "  + str(count[11]))
            else:
                 QMessageBox.about(self, "Test serii", "Test wypadł negatywnie!\nPojedyncze 1: " + str(count[0]) + "\nDwie 1: "  + str(count[1]) + "\nTrzy 1: "  + str(count[2]) + "\nCztery 1: "  + str(count[3]) + "\nPięć 1: "  + str(count[4]) + "\nWięcej 1: "  + str(count[5]) + "\nPojedyncze 0: " + str(count[6]) + "\nDwie 0: "  + str(count[7]) + "\nTrzy 0: "  + str(count[8]) + "\nCztery 0: "  + str(count[9]) + "\nPięć 0: "  + str(count[10]) + "\nWięcej 0: "  + str(count[11]))
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Nie wybrano pliku z kodem!")
            message.exec_()

    def selectTest3(self):
        if(self.keyPathText.text() != ""):

            if(os.path.getsize(self.keyPathText.text()) < 20000):
                message = QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QMessageBox.Critical)
                message.setText("Zbyt krótki ciąg!")
                message.exec_()
                return 0

            with open(self.keyPathText.text(), 'r') as file:
                x = re.findall(r"(0{26})|(1{26})", file.read(20000))
                print(x)
                if x is None:
                    QMessageBox.about(self, "Test długich serii", "Test wypadł pozytywnie!")
                else:
                    QMessageBox.about(self, "Test długich serii", "Test wypadł negatywnie!\nPierwszy dłuższy ciąg to " + str(x[0]))
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Nie wybrano pliku z kodem!")
            message.exec_()

    def selectTest4(self):
        if(self.keyPathText.text() != ""):

            if(os.path.getsize(self.keyPathText.text()) < 20000):
                message = QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QMessageBox.Critical)
                message.setText("Zbyt krótki ciąg!")
                message.exec_()
                return 0

            s = {format(i, '#06b')[2:]: 0 for i in range(16)}
            with open(self.keyPathText.text(), 'r') as file:
                while range(5000):
                    strNum = file.read(4)
                    if not strNum:
                        break
                    s[strNum] = s[strNum]+1
            sSum = 0
            for value in s.values():
                sSum += value**2
            X = 16/5000*sSum-5000
            if X > 2.16 and X < 46.17:
                QMessageBox.about(self, "Test pokerowy", "Test wypadł pozytywnie!\nUzyskana wartość to " + str(X))
            else:
                QMessageBox.about(self, "Test pokerowy", "Test wypadł negatywnie!\nUzyskana wartość to " + str(X))
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Nie wybrano pliku z kodem!")
            message.exec_()


    #Picturers

    def HidePicture(self):
        tempPath = filedialog.askopenfilename()
        if(self.picregex.match(tempPath)):
            if(self.textPathText.text() != ""):
                picBits = numpy.unpackbits(numpy.fromfile(tempPath, dtype = "uint8"))
                if(os.path.getsize(self.textPathText.text()) +54 > len(picBits)/8):
                    message = QMessageBox()
                    message.setWindowTitle("Błąd")
                    message.setIcon(QMessageBox.Critical)
                    message.setText("Wybrany obraz jest zbyt mały!")
                    message.exec_()                     
                else:
                    timeStop = 0
                    timeStart = time.time()

                    textBits = numpy.unpackbits(numpy.fromfile(self.textPathText.text(), dtype = "uint8"))

                    i = randint(54,len(picBits)/8 - os.path.getsize(self.textPathText.text())+1)
                    with open("piccode/"+self.fileName.text()+".txt","w") as codefile:
                        codefile.write(str(i))
                    self.extraInfo.setText("W folderze piccode utworzono odpowiedni plik z kluczem!")

                    for b in textBits:
                        picBits[i*8+7] = b
                        i = i+1
                    for x in range(16):
                        picBits[i*8+7] = 1
                        i = i+1
                    with open("pic/"+self.fileName.text()+tempPath[-4:],"wb") as outputfile:
                        outputfile.write(numpy.packbits(picBits))

                    timeStop = time.time()
                    self.timeText.setText("Pracę wykonano w ciągu " + str(timeStop - timeStart) + "s!")
            else:
                message = QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QMessageBox.Critical)
                message.setText("Nie wybrano pliku z tekstem do schowania!")
                message.exec_()  
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Wybrany plik nie jest w odpowiednim formacie!\nNie można więc schować pliku!\nProszę wybrać plik w którym tekst ma zostać schowany.")
            message.exec_()  

    def SeekPicture(self):
        tempPath = filedialog.askopenfilename()
        if(self.picregex.match(tempPath)):
            picBits = numpy.unpackbits(numpy.fromfile(tempPath, dtype = "uint8"))
            timeStop = 0
            timeStart = time.time()
            outputBits = []

            if(self.keyPathText.text() == ""):
                i = 54
                self.extraInfo.setText("Nie wybrano pliku z kluczem i efekt może odbiegać od zamieżanego!")
            else:
                with open(self.keyPathText.text(),"r") as inputfile:
                    tempString = inputfile.readline()
                    tempString = tempString.replace("\n","")
                    if(tempString.isnumeric and int(tempString) < os.path.getsize(tempPath)-1):
                        i = int(tempString)
                    else:
                        i = 54
                        self.extraInfo.setText("Wybrany z plik kluczem był niepoprawny i efekt może odbiegać od zamieżanego!")

            with open("text/"+self.fileName.text()+".txt","wb") as outputfile:
                checkEnd = []
                while True:
                    for x in range(8):
                        if(i >= len(picBits)/8):
                            break
                        outputBits.append(picBits[i*8+7])
                        i = i+1
                        
                    if((outputBits == checkEnd == [1,1,1,1,1,1,1,1]) or i >= len(picBits)/8):
                        outputfile.seek(-1, os.SEEK_END)
                        outputfile.truncate()
                        break
                    else:
                        checkEnd = outputBits.copy()
                        outputfile.write(numpy.packbits(outputBits))
                        outputBits = []

            timeStop = time.time()
            self.timeText.setText("Pracę wykonano w ciągu " + str(timeStop - timeStart) + "s!")
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Wybrany plik nie jest w odpowiednim formacie!\nNie można więc schować pliku!\nProszę wybrać plik w którym tekst ma zostać schowany.")
            message.exec_() 

    def ShowPicture(self):
        tempPath = filedialog.askopenfilename()
        if(self.picregex.match(tempPath)):
            example = QMessageBox()
            example.setWindowTitle("Wybrany obraz")
            example.setIconPixmap(QPixmap(tempPath))
            example.exec_()
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Wybrany plik nie jest w odpowiednim formacie!")
            message.exec_()  
            
    

# MAIN
app = QApplication(sys.argv)

if not os.path.exists('code'):
    os.makedirs('code')
if not os.path.exists('keys'):
    os.makedirs('keys')
if not os.path.exists('text'):
    os.makedirs('text')
if not os.path.exists('pic'):
    os.makedirs('pic')
if not os.path.exists('piccode'):
    os.makedirs('piccode')

window = Okno()
window.setStyleSheet("background-color: rgb(230,235,235);")
window.setFixedWidth(1200)
window.show()

app.exec_()