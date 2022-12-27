import sys
import datetime
import sqlite3
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
        self.h1box = QHBoxLayout(self.wrapper)

        self.table = QTableWidget(self)

        self.task_line = QLineEdit(self)
        self.task_line.textChanged.connect(self.enable_disable_button)

        self.task_date = QDateEdit(self)
        self.task_date.setCalendarPopup(True)

        self.task_btn = QPushButton(self)
        self.task_btn.setEnabled(False)
        self.task_btn.setText("Добавить")
        self.task_btn.clicked.connect(self.addTask)

        self.layout_sizePol_init()
        self.table_init()
        self.setCentralWidget(self.wrapper)
        self.getTodayDate()
        self.outputTaskTable()
        self.show()

    def layout_sizePol_init(self):
        self.vbox.setSpacing(10)
        self.vbox.addWidget(self.table)
        self.vbox.addLayout(self.h1box)
        self.h1box.addWidget(self.task_line)
        self.h1box.addWidget(self.task_date)
        self.h1box.addWidget(self.task_btn)
        self.setLayout(self.vbox)

        self.sizePolicy_task_date = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.sizePolicy_task_date.setHorizontalStretch(30)
        self.task_date.setSizePolicy(self.sizePolicy_task_date)

        self.sizePolicy_task_line = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.sizePolicy_task_line.setHorizontalStretch(100)
        self.task_line.setSizePolicy(self.sizePolicy_task_line)

    def enable_disable_button(self):
        if self.task_line.text():
            self.task_btn.setEnabled(True)
        else:
            self.task_btn.setEnabled(False)

    def table_init(self):
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Номер", "Задача", "Дата", "Статус"])

        #self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)

        self.table.cellDoubleClicked.connect(self.rowSelected)

        self.table.setRowCount(0)

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

    def getTodayDate(self):
        now = datetime.datetime.now()
        str = now.strftime("%d.%m.%Y")
        print(f"getTodayDate->date:{str}")
        self.statusBar().showMessage(f"{str}: Запущено")
        self.task_date.setMinimumDate(now)
        return str

    def addTask(self):
        print(f"addTask->task_text:{self.task_line.text()}")
        print(f"addTask->task_date:{self.task_date.text()}")
        self.statusBar().showMessage(f"Новая задача: {self.task_line.text()}. Дата: {self.task_date.text()}")

        try:
            sqlite_connection = sqlite3.connect('TasksDataBase.db')
            cursor = sqlite_connection.cursor()
            print("addTask->Подключен к SQLite")

            sqlite_insert_with_param = """INSERT INTO TasksTable (text, date, isComplete)
                                          VALUES (?, ?, ?);"""
            data_tuple = (self.task_line.text(), self.task_date.text(), False)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqlite_connection.commit()

            print("addTask->Запись успешно добавлена")
            cursor.close()
            self.outputTaskTable()

        except sqlite3.Error as error:
            print("addTask->Ошибка при работе с SQLite", error)
            self.statusBar().showMessage(f"Ошибка при работе с SQLite: {error}")
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("addTask->Соединение с SQLite закрыто")

    def outputTaskTable(self):
        try:
            sqlite_connection = sqlite3.connect('TasksDataBase.db')
            cursor = sqlite_connection.cursor()
            print("outputTaskTable->Подключен к SQLite")

            sqlite_select_0 = """SELECT * FROM TasksTable WHERE isComplete = '0'"""
            cursor.execute(sqlite_select_0)
            result_0 = cursor.fetchall()

            sqlite_select_1 = """SELECT * FROM TasksTable WHERE isComplete = '1'"""
            cursor.execute(sqlite_select_1)
            result_1 = cursor.fetchall()

            n = 0
            for i in result_0:
                self.table.setRowCount(n + 1)
                self.table.setItem(n, 0, QTableWidgetItem(str(i[0])))
                self.table.setItem(n, 1, QTableWidgetItem(i[1]))
                self.table.setItem(n, 2, QTableWidgetItem(i[2]))
                if i[3] == 0:
                    self.table.setItem(n, 3, QTableWidgetItem("не выполнено"))
                elif i[3] == 1:
                    self.table.setItem(n, 3, QTableWidgetItem("выполнено"))
                n += 1

            for i in result_1:
                self.table.setRowCount(n + 1)
                self.table.setItem(n, 0, QTableWidgetItem(str(i[0])))
                self.table.setItem(n, 1, QTableWidgetItem(i[1]))
                self.table.setItem(n, 2, QTableWidgetItem(i[2]))
                if i[3] == 0:
                    self.table.setItem(n, 3, QTableWidgetItem("не выполнено"))
                elif i[3] == 1:
                    self.table.setItem(n, 3, QTableWidgetItem("выполнено"))
                n += 1

            cursor.close()

        except sqlite3.Error as error:
            print("outputTaskTable->Ошибка при работе с SQLite", error)
            self.statusBar().showMessage(f"Ошибка при работе с SQLite: {error}")

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("outputTaskTable->Соединение с SQLite закрыто")

    def completeTask(self):
        pass

    def rowSelected(self):
        print("rowSelected->Выбрана ячейка")
        selectedRow = int(self.table.currentRow())
        number = int(self.table.item(selectedRow, 0).text())
        print(number)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WidgetToDo()
    sys.exit(app.exec_())
