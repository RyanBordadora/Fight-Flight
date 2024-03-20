import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QAction, QMenu, QStackedWidget, QPushButton

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QAction, QMenu, QMenuBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Game Menu")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)

        self.initUI()

    def initUI(self):
        # Logo
        logo_label = QLabel(self)
        logo_label.setText("Press Enter to Continue")
        logo_label.setAlignment(Qt.AlignCenter)

        # Main Menu
        main_menu = QWidget(self)

        play_button = QPushButton("Play", self)
        play_button.clicked.connect(self.showPlayMenu)

        settings_button = QPushButton("Settings", self)
        settings_button.clicked.connect(self.showSettingsMenu)

        # Vertical Layout for Main Menu
        layout = QVBoxLayout(main_menu)
        layout.addWidget(play_button)
        layout.addWidget(settings_button)
        layout.addStretch(1)

        # Add logo and main menu to the stacked widget
        self.central_widget.addWidget(logo_label)
        self.central_widget.addWidget(main_menu)

        # Show the logo initially
        self.central_widget.setCurrentWidget(logo_label)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            # Switch to the main menu when Enter is pressed
            self.central_widget.setCurrentIndex(1)

    def showPlayMenu(self):
        play_menu = QMenu("Play Menu", self)
        # Add actions specific to the play menu if needed
        play_menu.exec_(self.mapToGlobal(self.central_widget.rect().center()))

    def showSettingsMenu(self):
        settings_menu = QMenu("Settings Menu", self)
        # Add actions specific to the settings menu if needed
        settings_menu.exec_(self.mapToGlobal(self.central_widget.rect().center()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
