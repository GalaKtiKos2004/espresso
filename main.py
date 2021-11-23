import sys
import sqlite3

from PyQt5 import uic, QtCore  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


con = sqlite3.connect('coffee.sqlite')
cur = con.cursor()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadTable()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
