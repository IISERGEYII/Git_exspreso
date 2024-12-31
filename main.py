import sqlite3
import sys

from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QApplication

from add_form import Add
from main_form import Main_Form


class Example(QWidget, Main_Form):
    def __init__(self):
        self.connection = sqlite3.connect("coffee")
        super().__init__()
        self.setupUi(self)
        self.createFields()
        self.list_modified = []

        res = self.connection.cursor().execute("SELECT * FROM coffee")
        self.pushButton.clicked.connect(self.add_row)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.data = {}
        for i, row in enumerate(res):
            self.tableWidget.insertRow(i)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect((self.save_results))
        self.modified = {}

    def item_changed(self, item):
        row = item.row()
        rowdata = {}
        for fieldId, fieldName in self.fields.items():
            rowdata[fieldName] = self.tableWidget.item(row, fieldId).text()
        self.modified[row] = rowdata

    def save_results(self):
        if self.modified:
            cur = self.connection.cursor()
            for data in self.modified.values():
                que = "UPDATE coffee\n"
                que += 'SET'
                que += '\n'
                que += ", ".join([f"{key}='{data.get(key)}'"
                                  for key in data.keys()])
                que += '\n'
                que += f"WHERE id = {data.get('id')}"
            cur.execute(que)
            self.connection.commit()
            self.modified.clear()

    def add_row(self):
        self.addWindows = Add(self.tableWidget)
        self.addWindows.show()

    def createFields(self):
        cur = self.connection.cursor()
        cur.execute('PRAGMA table_info("coffee")')
        self.fields = {}
        for i, col in enumerate(cur.fetchall()):
            self.tableWidget.insertColumn(i)
            self.fields[i] = col[1]




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
