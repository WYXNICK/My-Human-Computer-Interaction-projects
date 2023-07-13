import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
from asrInterface import Ui_MainWindow
import sys
import speech_recognition as sr
import subprocess
import os
import threading
from PyQt5.QtGui import QMovie
chunk = 1024


class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #添加麦克风图标按钮
        self.micButton = QtWidgets.QPushButton(self.ui.centralwidget)
        self.micButton.setGeometry(QtCore.QRect(235, 368, 47, 63))
        self.micButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/phone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.micButton.setIcon(icon)
        self.micButton.setIconSize(QtCore.QSize(50, 50))
        self.micButton.setObjectName("micButton")
        self.micButton.clicked.connect(self.start_listening)

        # 添加播放动画
        self.movie = QMovie("icon/play.gif")
        self.movie.setScaledSize(QtCore.QSize(160, 100))
        self.ui.mic_on.setMovie(self.movie)


    def start_listening(self):
        self.movie.start()
        threading.Thread(target=self.listen).start()

    def play_audio(self, audio_file):
        subprocess.call(["start", audio_file], shell=True)
        print("Playing music...")

    def open_notepad(self):
        subprocess.Popen(["notepad.exe"])
        print("Opening Notepad...")

    def search_in_browser(self,text):
        query = text.replace("search", "").strip()
        url = f"https://www.baidu.com/s?wd={query}"
        webbrowser.open_new_tab(url)
        print(f"Searching for {query}...")
    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Say something please")
            audio = recognizer.listen(source)
            self.movie.stop()
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio, language='en-US')
            self.ui.textbox.setText(f"You said: {text}")
            if text == "play music":
                # Play audio file jaychou.wav
                audio_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jaychou.wav")
                threading.Thread(target=self.play_audio, args=(audio_file,)).start()
            elif text == "open notepad" or text == "open Notepad":
                self.open_notepad()
            elif "search" in text:
                self.search_in_browser(text)
            print(f"You said: {text}")
            self.myCommand = text
        except sr.UnknownValueError:
            print("Could not understand you,please try again")
            self.ui.textbox.setText("Could not understand you,please try again")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            self.ui.textbox.setText(f"Error: {e}")


app = QtWidgets.QApplication([])
application = myWindow()
application.show()
sys.exit(app.exec())
