import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QWidget
from PyQt5.QtCore import pyqtSignal
from UI.mainUI import Ui_Widget
from UI.addEditCoffeeForm import Ui_addEditCoffeeForm


class Coffee(QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_data()

        self.addButton.clicked.connect(self.add_record)
        self.coffeeDB.cellDoubleClicked.connect(self.edit_record)

    def load_data(self):
        conn = sqlite3.connect('data/coffee.sqlite')
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

    def add_record(self):
        self.addEditCoffeeForm = CoffeeForm()
        self.addEditCoffeeForm.record_saved.connect(self.load_data)
        self.addEditCoffeeForm.show()

    def edit_record(self, row, column):
        id = self.coffeeDB.item(row, 0).text()
        self.addEditCoffeeForm = CoffeeForm(id)
        self.addEditCoffeeForm.record_saved.connect(self.load_data)
        self.addEditCoffeeForm.show()


class CoffeeForm(QDialog, Ui_addEditCoffeeForm):
    record_saved = pyqtSignal()

    def __init__(self, id=None):
        super().__init__()
        self.setupUi(self)

        self.id = id
        self.conn = sqlite3.connect('data/coffee.sqlite')
        self.cur = self.conn.cursor()

        if self.id:
            self.load_record()
        else:
            self.generate_id()

        self.saveButton.clicked.connect(self.save_record)

    def load_record(self):
        self.cur.execute("SELECT * FROM coffee WHERE id = ?", (self.id))
        record = self.cur.fetchone()

        self.idLineEdit.setText(str(record[0]))
        self.nameLineEdit.setText(record[1])
        self.roastLineEdit.setText(record[2])
        self.typeLineEdit.setText(record[3])
        self.descriptionLineEdit.setText(record[4])
        self.priceLineEdit.setText(str(record[5]))
        self.volumeLineEdit.setText(str(record[6]))

    def generate_id(self):
        self.cur.execute("SELECT MAX(id) FROM coffee")
        max_id = self.cur.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1
        self.idLineEdit.setText(str(new_id))

    def save_record(self):
        id = self.idLineEdit.text()
        name = self.nameLineEdit.text()
        roast = self.roastLineEdit.text()
        type = self.typeLineEdit.text()
        description = self.descriptionLineEdit.text()
        price = self.priceLineEdit.text()
        volume = self.volumeLineEdit.text()

        if self.id:
            self.cur.execute("""UPDATE coffee SET name=?, roast_degree=?, ground_or_whole=?, description=?,
                                    price=?, volume=? WHERE id=?""",
                             (name, roast, type, description, price, volume, id))
        else:
            self.cur.execute(
                """INSERT INTO coffee (id, name, roast_degree, ground_or_whole, description, price, volume) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (id, name, roast, type, description, price, volume))
        self.conn.commit()
        self.cur.close()
        self.record_saved.emit()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Coffee()
    window.show()
    sys.exit(app.exec_())
