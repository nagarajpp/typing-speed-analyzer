# ⌨️ Typing Speed Analyzer (wxPython)

Typing Speed Analyzer is a desktop application built using Python and wxPython that measures typing speed (WPM) and accuracy in real time. The application runs a 60-second typing test, selects random paragraphs, and stores the top 5 scores in a local leaderboard file.

Features include a dark-mode interface, live timer, real-time WPM and accuracy calculation, restart option, and a persistent leaderboard saved without using any external database.

Technologies used:
Python 3.x, wxPython, and built-in Python modules such as time and random.

Project structure:
typing_speed_analyzer.py – main application file  
leaderboard.txt – stores user scores (auto-generated)  
README.md – project documentation

Installation steps:
1. Install Python from https://www.python.org and ensure it is added to PATH.
2. Install wxPython using the command:
   pip install wxPython
3. Run the application using:
   python typing_speed_analyzer.py

Working principle:
The application starts timing when the user begins typing. WPM is calculated using the formula:
WPM = (Total characters typed / 5) ÷ time in minutes.
Accuracy is calculated by comparing typed characters with the reference paragraph:
Accuracy = (Correct characters / Total typed characters) × 100.

Leaderboard:
Scores are stored in a text file in the format:
Name:User,WPM:60,Accuracy:95
The app displays the top 5 users sorted by highest WPM.

Future enhancements may include character-level highlighting, online leaderboard support, performance graphs, difficulty levels, and sound effects.

This project is open-source and intended for learning and educational purposes.

Developed using Python and wxPython.
