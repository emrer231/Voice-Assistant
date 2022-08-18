from re import A
import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from time import sleep
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from neuralintents import GenericAssistant
import speech_recognition
from commands import*


mappings = {

    'greeting': greeting,
    'goodbye': goodbye,
    'what_time': what_time,
    'search_in_wiki': search_in_wiki,
    'open_video_youtube': open_video_youtube,
    'search_google': search_google,
    'open_twitter': open_twitter,
    'open_github': open_github,
    'day_week': day_week,
    'current_date': current_date,
    'weather_forc': weather_forc,
    'system_shut_down': system_shut_down,
    'create_alarm': create_alarm,
    'antivirus': antivirus,
    'lock_screen': lock_screen,
    'uygulama_ac': uygulama_ac,
    'sarki': sarki
}  

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()




class Worker(QObject):
    finished =  pyqtSignal()
    def mic(self):
        
        from main import speech_recognition
        speech_recognition.Recognizer()
        
        self.finished.emit()

class Microphone(QObject):
    finished = pyqtSignal()
    def duy(self):
        
        recognizer = speech_recognition.Recognizer()
        playsound("opening.mp3")
        

        while True:
            
            try:
                
                with speech_recognition.Microphone() as mic:
                    
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)
                    
                    message = recognizer.recognize_google(audio, language="tr-TR")
                    message = message.lower()
                    
                playsound("ending.mp3")
                assistant.request(message)
                

            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                self.finished.emit()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Maviş")
        self.setFixedSize(QSize(450,800))
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.bgwidget = QtWidgets.QWidget(self)
        self.bgwidget.setFixedSize(450,800)
        self.bgwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.bgwidget.setStyleSheet("QWidget#bgwidget{\n"
"background-color:qlineargradient(spread:pad, x1:0.353, y1:0.210409, x2:0.930348, y2:1, stop:0.0746269 rgba(0, 234, 255, 1), stop:0.850746 rgba(0, 192, 255, 1))}")
        self.bgwidget.setObjectName("bgwidget")
        self.pushButton = QtWidgets.QPushButton(self.bgwidget)
        self.pushButton.setGeometry(QtCore.QRect(190, 630, 80, 80))
        self.pushButton.setStyleSheet(
"QPushButton {\n"
"    border: 1px solid #8f8f91;\n"
"    border-radius: 40px;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
"    min-width: 80px;\n"
"}\n"
"\n"

"QPushButton:pressed {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #dadbde, stop: 1 #f6f7fa);\n"
"}\n"
)       
        
        self.pushButton.setIcon(QtGui.QIcon('mic.ico'))
        self.pushButton.setIconSize(QtCore.QSize(75,75))
        self.pushButton.clicked.connect(self.clicked)

    
        


    def clicked(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker2 = Microphone()
        self.worker2.moveToThread(self.thread)
        self.thread.started.connect(self.worker2.duy)
        self.worker2.finished.connect(self.thread.quit)
        self.worker2.finished.connect(self.worker2.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.mic)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.pushButton.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.pushButton.setEnabled(True)
        )
        



        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    recognizer = speech_recognition.Recognizer()
    window = MainWindow()
    window.setWindowIcon(QtGui.QIcon('lora.ico'))
    window.show()
    sys.exit(app.exec())
