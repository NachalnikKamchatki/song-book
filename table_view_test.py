import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QTableView,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QAbstractItemView
)
from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QFont,
    QIcon
)
from PyQt5.QtCore import Qt

from db_creator import get_data


class DisplaySongs(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.pb_search.clicked.connect(self.pb_search_clicked)
        self.pb_reload.clicked.connect(self.pb_reload_clicked)
        self.table_view.clicked.connect(self.select_song)

    def initializeUI(self):
        """
        Initialize the window and display its contents to the screen.
        """
        self.setWindowIcon(QIcon('icon.ico'))
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle('Songer-book')

        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionMode(1)
        self.table_view.setSelectionBehavior(1)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.horizontalHeader().setSectionResizeMode(1)

        self.setupModelView()
        self.le_search = QLineEdit()
        self.le_search.setPlaceholderText('Ведите название песни')
        self.pb_search = QPushButton('Найти')
        self.pb_reload = QPushButton('Загрузить заново')
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Times", 17))

        vbox1 = QVBoxLayout()
        hbox_mini = QHBoxLayout()
        hbox_mini.addWidget(self.le_search)
        hbox_mini.addWidget(self.pb_search)
        vbox1.addLayout(hbox_mini)
        vbox1.addWidget(self.table_view)
        vbox1.addWidget(self.pb_reload)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.text_edit)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.setLayout(hbox)

        self.show()

    def setupModelView(self):
        """
        Set up standard item model and table view.
        """
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        self.model.setRowCount(0)
        self.model.setColumnCount(2)

        self.loadDataFromDB()

    def loadDataFromDB(self, text=None):

        headers = ['Название композиции', 'Исполнитель(Автор)']
        self.model.clear()
        self.model.setHorizontalHeaderLabels(headers)
        if text:
            data = get_data(text)
        else:
            data = get_data()
        for i, row in enumerate(data):
            items = [QStandardItem(item) for item in row[1:3]]
            self.model.insertRow(i, items)
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()

    def pb_search_clicked(self):
        text = self.le_search.text()
        self.loadDataFromDB(text)

    def pb_reload_clicked(self):
        self.le_search.clear()
        self.loadDataFromDB()

    def select_song(self):
        indexes = self.table_view.selectedIndexes()
        if indexes:
            index = indexes[0]
            title = self.table_view.model().data(index, Qt.DisplayRole)
            data = get_data(title)[0]
            self.text_edit.setText(data[3])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DisplaySongs()
    sys.exit(app.exec_())
