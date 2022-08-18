import sys
import random
import json
from PyQt5.QtCore import QAbstractListModel, QMargins, QPoint, QSize, Qt
from PyQt5.QtGui import QColor, QFontMetrics
import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from time import sleep
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from neuralintents import GenericAssistant
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QListView,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QStyledItemDelegate
)

USER_ME = 0
USER_THEM = 1

BUBBLE_COLORS = {USER_ME: "#FFFFFF", USER_THEM: "#7BF782"}

BUBBLE_PADDING = QMargins(15, 5, 15, 5)
TEXT_PADDING = QMargins(25, 15, 25, 15)
mappings = {

    
    
} 
assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

class MessageDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        user, text = index.model().data(index, Qt.DisplayRole)

        bubblerect = option.rect.marginsRemoved(BUBBLE_PADDING)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        painter.setPen(Qt.NoPen)
        color = QColor(BUBBLE_COLORS[user])
        painter.setBrush(color)
        painter.drawRoundedRect(bubblerect, 10, 10)

        if user == USER_ME:
            p1 = bubblerect.topRight()
        else:
            p1 = bubblerect.topLeft()
        painter.drawPolygon(p1 + QPoint(-20, 0), p1 + QPoint(20, 0), p1 + QPoint(0, 20))

        
        painter.setPen(Qt.black)
        painter.drawText(textrect, Qt.TextWordWrap, text)

    def sizeHint(self, option, index):
        _, text = index.model().data(index, Qt.DisplayRole)
        metrics = QApplication.fontMetrics()
        rect = option.rect.marginsRemoved(TEXT_PADDING)
        rect = metrics.boundingRect(rect, Qt.TextWordWrap, text)
        rect = rect.marginsAdded(TEXT_PADDING)
        return rect.size()


class MessageModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
        self.messages = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.messages[index.row()]

    def rowCount(self, index):
        return len(self.messages)

    def add_message(self, who, text):
        if text:
            self.messages.append((who, text))
            self.layoutChanged.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Maviş")
        self.setFixedSize(QSize(450,800))
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.bgwidget = QtWidgets.QWidget(self)
        self.bgwidget.setGeometry(QtCore.QRect(0, 0, 450, 800))
        self.bgwidget.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0.353, y1:0.210409, x2:0.930348, y2:1, stop:0.0746269 rgba(0, 234, 255, 1), stop:0.850746 rgba(0, 192, 255, 1))")
        self.bgwidget.setObjectName("bgwidget")
        self.listView = QtWidgets.QListView(self.bgwidget)
        self.listView.setGeometry(QtCore.QRect(20, 20, 410, 670))
        self.listView.setStyleSheet("background-color:rgba(255,255,255,150);\n"
"border-radius:15px;\n"
"\n"
"")
        self.listView.setObjectName("listView")
        self.lineEdit = QtWidgets.QLineEdit(self.bgwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 705, 350, 80))
        self.lineEdit.setStyleSheet("background-color:rgba(255,255,255,250);\n"
"border-radius:15px;\n"
"")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.bgwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 705, 50, 80))
        self.pushButton.setStyleSheet("border: 1px solid #8f8f91;\n"
"border-radius: 15px;\n"
"background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
"")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")

        self.listView.setItemDelegate(MessageDelegate())

        self.model = MessageModel()
        self.listView.setModel(self.model)

        self.lineEdit.returnPressed.connect(self.message_to)

    def message_to(self):
        self.model.add_message(USER_ME, self.lineEdit.text())
        message = self.lineEdit.text()
        message = message.lower()
        self.model.add_message(USER_THEM, self.lineEdit.text())
       
        

   



    # def message_from(self):    
    #     self.model.add_message(USER_THEM, )

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()