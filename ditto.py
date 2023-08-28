import pystray
import pyperclip
import threading
from PIL import Image
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget



class Ditto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ditto - Clipboard Manager")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Click on words to copy")
        self.layout.addWidget(self.label)

        self.update_clipboard_timer = QTimer(self)
        self.update_clipboard_timer.timeout.connect(self.updateClipboard)
        self.update_clipboard_timer.start(100)

    def updateClipboard(self):
        cliptext = pyperclip.paste()
        self.processClipping(cliptext)

    def processClipping(self, cliptext):
        cliptextCleaned = self.cleanClipText(cliptext)
        self.label.setText(cliptextCleaned)
        self.updateClickableText(cliptextCleaned)

    def cleanClipText(self, cliptext):
        cliptext = "".join([c for c in cliptext if ord(c) <= 65535])
        return cliptext

    def updateClickableText(self, cliptext):
        words = cliptext.split()
        clickable_text = ""

        for word in words:
            clickable_text += f'<a href="{word}">{word}</a> '

        self.label.setText(clickable_text)
        self.label.linkActivated.connect(self.copyToClipboard)

    def copyToClipboard(self, link):
        self.clipboard().setText(link)

    def start(self):
        threading.Thread(target=self.check_user_activity).start()

    def stop(self):
        self.running = False

def show_menu(icon, item):
    if item.text == 'Abrir':
        prog.show()
    elif item.text == 'Encerrar':
        prog.stop()
        icon.stop()

def main():
    global prog
    prog = Ditto()
    prog.start()

    image = Image.open("Ditto.ico")

    menu = (
        pystray.MenuItem('Abrir', show_menu),
        pystray.MenuItem('Encerrar', show_menu),
    )

    menu_icon = pystray.Icon(prog.name, image, prog.name, menu)
    menu_icon.run()

if __name__ == '__main__':
    main()
