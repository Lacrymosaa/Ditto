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
        self.clipboard_entries = []

        self.updateClipboard()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label_widgets = []

        for _ in range(10):
            label = QLabel("", self)
            label.setFixedHeight(50)
            label.setAlignment(Qt.AlignTop)
            label.setFrameStyle(QLabel.Panel | QLabel.Raised)
            label.setLineWidth(1)
            label.setMidLineWidth(1)
            layout.addWidget(label)
            self.label_widgets.append(label)

        central_widget.setLayout(layout)

        self.setWindowTitle("Ditto")
        icon = QIcon("Ditto.ico")
        self.setWindowIcon(icon)
        self.setGeometry(100, 100, 400, 500)

        for label in self.label_widgets:
            label.mousePressEvent = lambda event, l=label: self.copyLabelContent(l)

    def updateClipboard(self):
        cliptext = pyperclip.paste()

        if not self.clipboard_entries or cliptext != self.clipboard_entries[0][1]:
            new_entry = (1, cliptext)
            self.clipboard_entries.insert(0, new_entry)

            if len(self.clipboard_entries) > 10:
                self.clipboard_entries.pop()

            self.updateLabels()
        QTimer.singleShot(100, self.updateClipboard)

    def updateLabels(self):
        for i, (position, item) in enumerate(self.clipboard_entries):
            self.label_widgets[i].setText(item)

    def copyLabelContent(self, label):
        content = label.text()
        if content:
            pyperclip.copy(content)

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
