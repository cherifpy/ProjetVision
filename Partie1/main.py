import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import cv2
import partie1


class WelcomeScreen(QWidget):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("WelcomeScreen.ui",self)
        self.Encode.clicked.connect(self.gotoEncodeScreen)
        self.Decode.clicked.connect(self.gotoDecodeScreen)

    #change to Encode Screen
    def gotoEncodeScreen(self):
        obj = EncodeScreen()
        widget.addWidget(obj)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    #Change to DecodeScreen
    def gotoDecodeScreen(self):
        obj = DecodeScreen()
        widget.addWidget(obj)
        widget.setCurrentIndex(widget.currentIndex()+1)
        

class EncodeScreen(QWidget):
    def __init__(self):
        super(EncodeScreen,self).__init__()
        loadUi("EncodeScreen.ui", self)
        self.Welcome.clicked.connect(self.gotoWelcomeScreen)
        self.Decode.clicked.connect(self.gotoDecodeScreen)
        self.LoadImage.clicked.connect(self.getImage)
        self.SaveImage.clicked.connect(self.exportImage)
        self.HideImage.clicked.connect(self.setEncodedImage)
        
    #Change to DecodeScreen
    def gotoDecodeScreen(self):
        obj = DecodeScreen()
        widget.addWidget(obj)
        widget.setCurrentIndex(widget.currentIndex()+1)

    #Change to WelcomeScreen
    def gotoWelcomeScreen(self):
        obj = WelcomeScreen()
        widget.addWidget(obj)
        widget.setCurrentIndex(widget.currentIndex()+1)

    #Load Image
    def getImage(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file', '', 'Image files (*.jpg *.jpeg *.png)')
        imagePath = fname[0]
        self.imagePath = imagePath
        self.image = cv2.imread(imagePath, -1)
        self.image_pix = QPixmap(imagePath)
        self.OrgnImage.setScaledContents(True)
        self.OrgnImage.setPixmap(QPixmap(self.image_pix))

    #Save Image
    def exportImage(self):
        print("Export Function")
        
        fname = QFileDialog.getSaveFileName(None, 'Export file', '', 'Image files (*.jpg *.jpeg *.png)')
        imagePath = fname[0]
        try:
            cv2.imwrite(imagePath, self.encodedImage)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Couldn't Save The Image")
            error_dialog.exec_()
    
    #Render Encoded image
    def setEncodedImage(self):
        try:
            print(self.imagePath)
            print(self.Text.toPlainText())
            self.Encode(self, self.imagePath, self.Text.toPlainText())
            print("dagi")
            # Convert CV2 To QImage
            height, width, channel = self.encodedImage.shape
            bytesPerLine = 3 * width
            qImg = QImage(self.encodedImage.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            self.qImg = qImg

            self.NewImage.setScaledContents(True)
            self.NewImage.setPixmap(QPixmap(qImg))
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error occured while rendering the encoded image')
            error_dialog.exec_()

    #à remplacer par la fonction d'encodage
    def Encode(self, imagePath, message):
        print("Encode Function")
        print(message)

        textToHide = message
        #Use encodedImage and textToHide to hide the text
        #return a cv2 matrix image

        self.encodedImage = partie1.Encode(textToHide,imagePath)



class DecodeScreen(QWidget):
    def __init__(self):
        super(DecodeScreen, self).__init__()
        loadUi("DecodeScreen.ui", self)
        self.Encode.clicked.connect(self.gotoEncodeScreen)
        self.Welcome.clicked.connect(self.gotoWelcomeScreen)
        self.LoadImage.clicked.connect(self.getImage)
        self.ExtractText.clicked.connect(self.setDecodedImage)

    #change to Encode Screen
    def gotoEncodeScreen(self):
        obj = EncodeScreen()
        widget.addWidget(obj)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    #Change to WelcomeScreen
    def gotoWelcomeScreen(self):
        obj = WelcomeScreen()
        widget.addWidget(obj)
        widget.setCurrentIndex(widget.currentIndex()+1)

    #Load Image
    def getImage(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file', '', 'Image files (*.jpg *.jpeg *.png)')
        imagePath = fname[0]
        self.imagePath = imagePath
        self.image = cv2.imread(imagePath, -1)
        self.image_pix = QPixmap(imagePath)
        self.OrgnImage.setScaledContents(True)
        self.OrgnImage.setPixmap(QPixmap(self.image_pix))
    
    #Render Decoded Image
    def setDecodedImage(self):
        try:
            self.decodedImage = self.Decode(self.imagePath)
            print("dagi")
            # Convert CV2 To QImage
            height, width, channel = self.decodedImage.shape
            bytesPerLine = 3 * width
            qImg = QImage(self.decodedImage.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            self.qImg = qImg
            
            self.HiddenTextImage.setScaledContents(True)
            self.HiddenTextImage.setPixmap(QPixmap(qImg))
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Error while rendering Decoded image')
            error_dialog.exec_()
    #à remplacer par la fonction de dencodage
    def Decode(self, imagePath):
        print("Decode Function")

        codage, shape_x,shape_y = partie1.DecodeText(imagePath)
        decodedImage = partie1.ConstructionImage(codage, shape_x,shape_y)
        #Use some functions to decode here
        #return a cv2 matrix image
        return decodedImage

    


#main
app = QApplication(sys.argv)
Welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(Welcome) 
widget.setFixedHeight(600)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting error!")
