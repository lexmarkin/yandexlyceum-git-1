import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget
from PyQt5 import uic


class Coffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('coffee.sqlite')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM coffee""")
        rows = cur.fetchall()

        self.coffeeDB.setRowCount(len(rows))
        self.coffeeDB.setColumnCount(7)
        self.coffeeDB.setHorizontalHeaderLabels(['ID', 'Название', 'Степень прожарки', 'Молотый/в зёрнах', 'Описание',
                                                 'Цена', 'Объём уп.'])
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                self.coffeeDB.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Coffee()
    window.show()
    sys.exit(app.exec_())
