import sys
from PyQt5.QtWidgets import *


class WidgetToDo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.wrapper = QWidget(self)
        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        self.setWindowTitle('PyToDo')
        self.statusBar().showMessage("Started")
        self.setWindowToCenter()
        self.vbox = QVBoxLayout(self.wrapper)
        self.vbox.setSpacing(10)
        self.h1box = QHBoxLayout(self.wrapper)
        table = QTableWidget(self.wrapper)
        table.resize(480, 400)
        self.vbox.addWidget(table)
        self.vbox.addLayout(self.h1box)
        task_line = QLineEdit(self)
        task_line.resize(200, 30)
        self.h1box.addWidget(task_line)
        task_date = QDateEdit(self)
        task_date.resize(140, 30)
        self.h1box.addWidget(task_date)
        task_btn = QPushButton(self)
        task_btn.resize(20, 30)
        self.h1box.addWidget(task_btn)
        self.setLayout(self.vbox)

        self.setCentralWidget(self.wrapper)
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
