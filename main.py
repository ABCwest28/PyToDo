import sys
from PyQt5.QtWidgets import *


class WidgetToDo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        self.setWindowTitle('PyToDo')
        self.setWindowToCenter()
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Подтверждение',
                "Подтвердите выход", QMessageBox.Yes |
                QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def setWindowToCenter(self):
        my_frame_geom = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        my_frame_geom.moveCenter(screen_center)
        self.move(my_frame_geom.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WidgetToDo()
    sys.exit(app.exec_())
