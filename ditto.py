import sys
import pyperclip
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QSystemTrayIcon, QAction, QMenu

class Ditto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.trayIcon = None

        self.initUI()
        self.updateClipboard()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        self.label = QLabel("", self)
        self.label.setCursor(Qt.PointingHandCursor)
        self.label.setFrameStyle(QLabel.Panel | QLabel.Raised)
        self.label.setMargin(5)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        central_widget.setLayout(layout)

        self.setWindowTitle("Ditto's Clipboard Manager")
        icon = QIcon("Ditto.ico")
        self.setWindowIcon(icon)
        self.setGeometry(100, 100, 500, 200)

    def updateClipboard(self):
        cliptext = pyperclip.paste()
        self.processClipping(cliptext)
        QTimer.singleShot(100, self.updateClipboard)

    def processClipping(self, cliptext):
        cliptext_cleaned = self.cleanClipText(cliptext)
        self.label.setText(cliptext_cleaned)

    def cleanClipText(self, cliptext):
        cliptext = ''.join([c for c in cliptext if ord(c) <= 65535])
        return cliptext

    def mousePressEvent(self, event):
        self.onClick(event)

    def onClick(self, event):
        label_text = self.label.text()
        print("Copiado: ", label_text)
        pyperclip.copy(label_text)

    def createTrayIcon(self):
        if self.trayIcon is None:  # Verifica se o ícone já foi criado
            self.trayIcon = QSystemTrayIcon(QIcon('Ditto.ico'), self)
            self.trayIcon.setToolTip('Ditto Clipboard Manager')

            showAction = QAction('Abrir', self)
            exitAction = QAction('Sair', self)

            showAction.triggered.connect(self.show)
            exitAction.triggered.connect(self.exitApplication)

            trayMenu = QMenu()
            trayMenu.addAction(showAction)
            trayMenu.addAction(exitAction)

            self.trayIcon.setContextMenu(trayMenu)
            self.trayIcon.show()

    def exitApplication(self):
        self.trayIcon.hide()
        QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.createTrayIcon()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    mainWindow = Ditto()
    mainWindow.show()

    sys.exit(app.exec_())
