# Листинг теста класса book:
``` python
import unittest
from unittest.mock import patch
from PyQt5 import QtWidgets, QtCore
from utils import MyMainWindow

class TestMyMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication([])
        self.window = MyMainWindow()

    def tearDown(self):
        self.window.close()

    def test_bookAction_withQRCodeOption(self):
        item = QtWidgets.QListWidgetItem()
        item.setData(QtCore.Qt.UserRole, ("Book Name", "Author", "12345", 5))
        with patch.object(QtWidgets.QInputDialog, 'exec_', return_value=True), \
             patch.object(QtWidgets.QInputDialog, 'textValue', return_value="Получить QR-код"), \
             patch('utils.MyMainWindow.displayQRCode') as mock_displayQRCode:
            self.window.bookAction(item)
            mock_displayQRCode.assert_called_with(("Book Name", "Author", "12345", 5))

    def test_bookAction_withReservationOption(self):
        item = QtWidgets.QListWidgetItem()
        item.setData(QtCore.Qt.UserRole, ("Book Name", "Author", "12345", 3))
        with patch.object(QtWidgets.QInputDialog, 'exec_', return_value=True), \
             patch.object(QtWidgets.QInputDialog, 'textValue', return_value="Зарезервировать данную книгу"), \
             patch.object(MyMainWindow, 'reserveBook') as mock_reserveBook:
            self.window.bookAction(item)
            mock_reserveBook.assert_called_with(("Book Name", "Author", "12345", 3))

    def test_bookAction_withCancelOption(self):
        item = QtWidgets.QListWidgetItem()
        item.setData(QtCore.Qt.UserRole, ("Book Name", "Author", "12345", 5))
        with patch.object(QtWidgets.QInputDialog, 'exec_', return_value=False), \
             patch.object(MyMainWindow, 'displayQRCode') as mock_displayQRCode, \
             patch.object(MyMainWindow, 'reserveBook') as mock_reserveBook:
            self.window.bookAction(item)
            mock_displayQRCode.assert_not_called()
            mock_reserveBook.assert_not_called()


if __name__ == '__main__':
    unittest.main()
```