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
        self.statusBar().showMessage("Запущено")
        self.setWindowToCenter()

        self.vbox = QVBoxLayout(self.wrapper)
        self.vbox.setSpacing(10)

        self.h1box = QHBoxLayout(self.wrapper)

        self.table = QTableWidget(self.wrapper)
        self.vbox.addWidget(self.table)
        self.vbox.addLayout(self.h1box)

        self.task_line = QLineEdit(self)
        self.h1box.addWidget(self.task_line)

        self.task_date = QDateEdit(self)
        self.h1box.addWidget(self.task_date)

        self.task_btn = QPushButton(self)
        self.task_btn.setText("Добавить")
        self.task_btn.clicked.connect(self.addTask)
        self.h1box.addWidget(self.task_btn)

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

    def addTask(self):
        print(f"addTask->task_text:{self.task_line.text()}")
        print(f"addTask->task_date:{self.task_date.text()}")
        self.statusBar().showMessage(f"Новая задача: {self.task_line.text()}. Время: {self.task_date.text()}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WidgetToDo()
    sys.exit(app.exec_())
