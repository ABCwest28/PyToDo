import sys
from PyQt5.QtWidgets import *


class WidgetToDo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.list_widget = QListWidget()

    def initUI(self):
        self.resize(500, 500)
        self.setObjectName("WidgetToDo")
        self.setWindowTitle('PyToDo')
        self.setWindowToCenter()
        self.statusBar().showMessage("Started")
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

    def newRow(self):
        new_check_box = QCheckBox()
        new_line_edit = QLineEdit()
        new_button = QPushButton()

        new_h_layout = QHBoxLayout()
        new_h_layout.addWidget(new_check_box)
        new_h_layout.addWidget(new_line_edit)
        new_h_layout.addWidget(new_button)

        self.list_widget.addItem(new_h_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WidgetToDo()
    sys.exit(app.exec_())
