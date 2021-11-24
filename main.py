import sys
import sqlite3

from PyQt5 import uic, QtCore  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog


con = sqlite3.connect('coffee.sqlite')
cur = con.cursor()


class OldDialog(QDialog):
    def __init__(self, id):
        super().__init__()
        self.id = id
        uic.loadUi('update.ui', self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        print(self.comboBox.currentText())
        print(self.lineEdit.text())
        cur.execute(f"""update coffes set '{self.comboBox.currentText()}' = '{self.lineEdit.text()}' 
        where id = {self.id}""").fetchall()
        con.commit()
        self.table_window = MyWidget()
        self.table_window.show()
        self.close()


class NewDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('new.ui', self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        cur.execute(f"""insert into coffes('Название сорта', 'Степень обжарки', 'молотый/в зернах', 'Описание вкуса',
                 'Цена', 'Объем упаковки')
         values('{self.name.text()}', '{self.st.text()}', '{self.mz.text()}','{self.tasty.text()}',
          '{self.price.text()}', '{self.v.text()}')""")
        con.commit()
        self.table_window = MyWidget()
        self.table_window.show()
        self.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadTable()
        self.pushButton.clicked.connect(self.run)

    def loadTable(self):
        query = f"""select * from coffes"""
        res = cur.execute(query).fetchall()
        title = ['ID', 'Название сорта', 'Степень обжарки', 'молотый/в зернах', 'Описание вкуса',
                 'Цена', 'Объем упаковки']
        # Заполним размеры таблицы
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(title)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
                self.tableWidget.item(i, j).setFlags(QtCore.Qt.ItemIsEnabled)

    def run(self):
        self.new_window = OldNew()
        self.new_window.show()
        self.close()


class OldNew(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.new)
        self.pushButton_2.clicked.connect(self.old)

    def new(self):
        self.dialog_window = NewDialog()
        self.dialog_window.show()
        self.close()

    def old(self):
        self.dialog_window = OldDialog(self.lineEdit.text())
        self.dialog_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
