# Introduction

## How to run my program?

1. If you haven't installed Python yet, please download and install Python from the official website first.
2. Open the download page of JetBrains official website in your browser: https://www.jetbrains.com/pycharm/download/#section=windows, download and install PyCharm.
3. Open PyCharm, create a new project, choose the interpreter and project location.
4. Install PyQt5 and SpeechRecognition in PyCharm
5. Add the `asr.py`, `asrInterface.py`, `jaychou.wav`, and files in the `icon` folder to the project. You can open the files by clicking on the File -> Open option in the PyCharm interface and then drag and drop them into the project file tree.
6. To run the project and open the GUI interface, right-click on the `asr.py` file in the project file tree, and select the option "Run 'asr'".
7.  Read the prompts on the GUI interface to understand how to accurately use the several functions of the speech recognition system.
8. Click on the microphone button at the bottom right corner of the GUI to start voice input, and you can observe the information prompts in the terminal at the same time. The content of the speech recognition will be displayed in the text box at the bottom. If you say "play music", the system will automatically play the prepared `jaychou.wav` music. If you say "open Notepad", the system will automatically open the Windows built-in Notepad for you. If the sentence you say contains the word "search", the system will automatically help you search the text content after "search" on `www.baidu.com`.