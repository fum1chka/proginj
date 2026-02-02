# Импорт библиотек. Листинг программы:
``` python
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys 
import openpyxl as op
import qrcode
import datetime  # Добавим импорт модуля datetime
import random
import string
```

# Создание классов. Листинг программы:
``` python
class Book():

    def __init__(self, book_name, art, quantity):
        self.book_name = book_name
        self.art = art
        self.quantity = quantity
    def qr_show (self):
        qr_window = QtWidgets.QDialog()
        qr_window.setWindowTitle("QR Code")
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("temp_qr_code.png")
        label.setPixmap(pixmap)
        layout.addWidget(label)
        qr_window.setLayout(layout)
        qr_window.exec_()
    def reserve_book (self, book_info, prov_test):
        book_name, _, _, quantity = book_info
        if int(quantity) > 0:
            filename = 'Список книг библиотеки.xlsx'
            wb = op.load_workbook(filename)
            sheet = wb.active
            max_rows = sheet.max_row

            for i in range(3, max_rows + 1):
                if sheet.cell(row=i, column=2).value == book_name:
                    current_quantity = int(sheet.cell(row=i, column=6).value)
                    sheet.cell(row=i, column=6).value = current_quantity - 1
                    wb.save(filename)
                    QtWidgets.QMessageBox.information(self, "Успешно", "Вы успешно зарезервировали книгу")
                    self.ui.myFunction()  # Обновляем список книг

                    break
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Данной книги нет на складе")

class Author():

    def __init__(self, name_aut):
        self.name_aut = name_aut
class User():
    def __init__(self, name, fam, oth, date, email, status,):
        self.name = name
        self.fam = fam
        self.oth = oth
        self.date = date
        self.email = email
        self.status = status
        self.password = ""

    def change_password(self, new_password):
        self.password = new_password

    def borrow_book(self, book_info):
        return True
    def reg(self):
        # Проверка заполнения полей
        if not self.lineEdit.text() or not self.lineEdit_2.text() or not self.lineEdit_4.text() or not self.lineEdit_5.text():
            QtWidgets.QMessageBox.warning(None, 'Ошибка', 'Поля не заполнены')
            return

        # Проверка формата даты
        try:
            dob = datetime.datetime.strptime(self.lineEdit_4.text(), "%d.%m.%Y")
        except ValueError:
            QtWidgets.QMessageBox.warning(None, 'Ошибка', 'Неверный формат даты. Введите ДД.ММ.ГГГГ')
            return

        # Преобразование объекта datetime обратно в строку в нужном формате
        dob_formatted = dob.strftime("%d.%m.%Y")

        # Генерация нового библиотечного кода
        new_lib_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        filename = 'Список пользователей.xlsx'
        wb = op.load_workbook(filename)
        sheet = wb.active
        max_rows_reg = sheet.max_row

        User.name = self.lineEdit.text()
        User.fam = self.lineEdit_2.text()
        User.oth = self.lineEdit_3.text()
        User.date = dob_formatted  # Записываем отформатированную дату
        User.email = self.lineEdit_5.text()
        User.status = self.comboBox.currentText()
        User.lib_code = new_lib_code

        sheet.cell(row=max_rows_reg + 1, column=2).value = User.name
        sheet.cell(row=max_rows_reg + 1, column=3).value = User.fam
        sheet.cell(row=max_rows_reg + 1, column=4).value = User.oth
        sheet.cell(row=max_rows_reg + 1, column=5).value = User.date  
        sheet.cell(row=max_rows_reg + 1, column=6).value = User.email
        sheet.cell(row=max_rows_reg + 1, column=7).value = User.status
        sheet.cell(row=max_rows_reg + 1, column=8).value = User.lib_code

        wb.save(filename)

        QtWidgets.QMessageBox.information(None, 'Успешная регистрация', 'Ваша регистрация успешно завершена.\nВаш библиотечный код: {}'.format(new_lib_code))

        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()


    def auth(self, e):
        filename = 'Список пользователей.xlsx'
        wb = op.load_workbook(filename, data_only=True)
        sheet = wb.active
        max_rows_reg = sheet.max_row

        found = False  # Переменная для отслеживания успешного входа

        user_info = {}  # Словарь для хранения информации о пользователе

        for i in range(4, max_rows_reg + 1):
            User.email = str(sheet.cell(row=i, column=6).value)
            User.lib_code = str(sheet.cell(row=i, column=8).value)
            User.date = str(sheet.cell(row=i, column=5).value)
            
            if User.lib_code in self.lineEdit.text() or User.email in self.lineEdit.text(): 
                if User.date == self.lineEdit_2.text():  # Проверка правильности пароля
                    found = True  # Установка флага успешного входа
                    
                    # Извлечение информации о пользователе из Excel
                    user_info['first_name'] = str(sheet.cell(row=i, column=3).value)
                    user_info['last_name'] = str(sheet.cell(row=i, column=2).value)
                    user_info['middle_name'] = str(sheet.cell(row=i, column=4).value)
                    user_info['email'] = User.email
                    user_info['lib_code'] = User.lib_code

                    break

        if found:
            QtWidgets.QMessageBox.information(None, 'Успешный вход', 'Вы вошли в аккаунт')

            # Проверяем, открыто ли уже окно профиля
            if not self.profile_window:
                # Создаем экземпляр Ui_Profil и открываем окно профиля, передавая информацию о пользователе
                self.profile_window = QtWidgets.QMainWindow()
                ui = Ui_Profil()
                ui.setupUi(self.profile_window, user_info)
                self.profile_window.show()

            # Закрываем текущее окно "Вход в личный кабинет"
            self.PersonalArea.close()
        else:
            QtWidgets.QMessageBox.warning(None, 'Ошибка', 'Пароль или логин указаны неправильно')
            self.lineEdit.clear()
            self.lineEdit_2.clear()
class Ui_GraficRaboti(object):
    def setupUi(self, GraficRaboti):
        GraficRaboti.setObjectName("GraficRaboti")
        GraficRaboti.resize(259, 375)
        self.centralwidget = QtWidgets.QWidget(GraficRaboti)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 10, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 120, 161, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 140, 161, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 160, 161, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 180, 161, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 200, 161, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(10, 220, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 260, 161, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(10, 280, 161, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(10, 300, 181, 16))
        self.label_11.setObjectName("label_11")
        GraficRaboti.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(GraficRaboti)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 259, 21))
        self.menubar.setObjectName("menubar")
        GraficRaboti.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(GraficRaboti)
        self.statusbar.setObjectName("statusbar")
        GraficRaboti.setStatusBar(self.statusbar)

        self.retranslateUi(GraficRaboti)
        QtCore.QMetaObject.connectSlotsByName(GraficRaboti)
```

# Логика окна с графиком работы. листинг программы:
``` python
    def retranslateUi(self, GraficRaboti):
        _translate = QtCore.QCoreApplication.translate
        GraficRaboti.setWindowTitle(_translate("GraficRaboti", "MainWindow"))
        self.label.setText(_translate("GraficRaboti", "График работы"))
        self.label_2.setText(_translate("GraficRaboti", "Главный корпус"))
        self.label_3.setText(_translate("GraficRaboti", "понедельник-пятница"))
        self.label_4.setText(_translate("GraficRaboti", "с 10:00 до 18:00"))
        self.label_5.setText(_translate("GraficRaboti", "суббота"))
        self.label_6.setText(_translate("GraficRaboti", "с 11:00 до 17:00"))
        self.label_7.setText(_translate("GraficRaboti", "воскресенье - выходной"))
        self.label_8.setText(_translate("GraficRaboti", "Комплекс"))
        self.label_9.setText(_translate("GraficRaboti", "понедельник-пятница"))
        self.label_10.setText(_translate("GraficRaboti", "с 10:00 до 17:00"))
        self.label_11.setText(_translate("GraficRaboti", "суббота, воскресенье - выходной"))
```
# Логика главного окна. Листинг программы:
``` python
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 150, 400, 60))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(100, 220, 931, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.GetLibraryCode = QtWidgets.QPushButton(self.centralwidget)
        self.GetLibraryCode.setGeometry(QtCore.QRect(100, 260, 250, 25))
        self.GetLibraryCode.setObjectName("GetLibraryCode")
        self.NewArrivals = QtWidgets.QPushButton(self.centralwidget)
        self.NewArrivals.setGeometry(QtCore.QRect(350, 260, 250, 25))
        self.NewArrivals.setObjectName("NewArrivals")
        self.SubResources = QtWidgets.QPushButton(self.centralwidget)
        self.SubResources.setGeometry(QtCore.QRect(600, 260, 250, 25))
        self.SubResources.setObjectName("SubResources")
        self.EducMaterials = QtWidgets.QPushButton(self.centralwidget)
        self.EducMaterials.setGeometry(QtCore.QRect(850, 260, 250, 25))
        self.EducMaterials.setObjectName("EducMaterials")
        self.PersonalArea = QtWidgets.QPushButton(self.centralwidget)
        self.PersonalArea.setGeometry(QtCore.QRect(1000, 30, 100, 25))
        self.PersonalArea.setObjectName("PersonalArea")
        self.GraficRaboti = QtWidgets.QPushButton(self.centralwidget)
        self.GraficRaboti.setGeometry(QtCore.QRect(1000, 60, 100, 25))
        self.GraficRaboti.setObjectName("GraficRaboti")
        self.Search = QtWidgets.QPushButton(self.centralwidget)
        self.Search.setGeometry(QtCore.QRect(1030, 220, 71, 31))
        self.Search.setObjectName("Search")
        self.bookListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.bookListWidget.setGeometry(QtCore.QRect(100, 300, 1001, 150))
        self.bookListWidget.setObjectName("bookListWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.PersonalArea.clicked.connect(self.openPersonalAreaWindow) 
        self.GetLibraryCode.clicked.connect(self.openRegistrationWindow) 
        self.NewArrivals.clicked.connect(self.openNewArrivalsWindow) 
        self.SubResources.clicked.connect(self.openSubResourcesWindow)
        self.EducMaterials.clicked.connect(self.openHelpWindow)
        self.GraficRaboti.clicked.connect(self.openGraficRaboti) 
        self.Search.clicked.connect(self.myFunction) 
        self.lineEdit.returnPressed.connect(self.myFunction)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Научная библиотека"))
        self.label.setText(_translate("MainWindow", "НАУЧНАЯ БИБЛИОТЕКА"))
        self.GetLibraryCode.setText(_translate("MainWindow", "Получить библиотечный код"))
        self.NewArrivals.setText(_translate("MainWindow", "Новые поступления"))
        self.SubResources.setText(_translate("MainWindow", "Список подписных ресурсов"))
        self.EducMaterials.setText(_translate("MainWindow", "Справка"))
        self.PersonalArea.setText(_translate("MainWindow", "Ваш кабинет"))
        self.Search.setText(_translate("MainWindow", "Поиск"))
        self.GraficRaboti.setText(_translate("MainWindow", "График работы"))

    def openPersonalAreaWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_PersonalArea()
        self.ui.setupUi(self.window)
        self.window.show()
    
    def openRegistrationWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_RegistrationWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def openNewArrivalsWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_NewArrivalsWindow()
        self.ui.setupUi(self.window, self.bookListWidget)  # Передаем bookListWidget
        self.window.show()

    def openSubResourcesWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SubResourcesWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def openHelpWindow(self):
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_HelpWindow()
            self.ui.setupUi(self.window)
            self.window.show()

    def openProfilWindow(self):
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_Profil()
            self.ui.setupUi(self.window)
            self.window.show()

    def openGraficRaboti(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_GraficRaboti()
        self.ui.setupUi(self.window)
        self.window.show()
    
    def myFunction(self):
        search_text = self.lineEdit.text()
        filename = 'Список книг библиотеки.xlsx'
        wb = op.load_workbook(filename, data_only=True)
        sheet = wb.active
        max_rows = sheet.max_row

        found_books = []
        for i in range(3, max_rows + 1):
            Book_ser = Book(str(sheet.cell(row=i, column=2).value), str(sheet.cell(row=i, column=4).value), str(sheet.cell(row=i, column=6).value))
            Author_ser = Author(str(sheet.cell(row=i, column=3).value))
            if search_text in Author_ser.name_aut or search_text in Book_ser.book_name or search_text in Book_ser.art:
                found_books.append((Book_ser.book_name, Author_ser.name_aut, Book_ser.art, Book_ser.quantity))

        self.bookListWidget.clear()
        if found_books:
            for book in found_books:
                # Изменяем формат вывода, чтобы включить количество книг
                item = QtWidgets.QListWidgetItem(f"{book[0]} - {book[1]} - {book[2]} - Количество: {book[3]}")
                self.bookListWidget.addItem(item)
                item.setData(QtCore.Qt.UserRole, book)
```
# Окно, всплывающее, если дважды щелкнуть на найденную книгу. Листинг программы:
``` python
class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.bookListWidget.itemClicked.connect(self.bookAction)

    def bookAction(self, item):
        book_info = item.data(QtCore.Qt.UserRole)
        if book_info:
            options = ["Получить QR-код", "Зарезервировать данную книгу"]
            dialog = QtWidgets.QInputDialog()
            dialog.setWindowTitle("Выберите действие")
            dialog.setLabelText("Выберите действие")
            dialog.setComboBoxItems(options)
            dialog.setCancelButtonText("Отмена")
            
            if dialog.exec_():
                choice = dialog.textValue()  # Получаем текст выбранного элемента
                if choice == "Получить QR-код":
                    self.displayQRCode(book_info)
                elif choice == "Зарезервировать данную книгу":
                    self.reserveBook(book_info)
            else:
                # Код, который будет выполнен при нажатии кнопки "Отмена"
                pass  

    def displayQRCode(self, book_info):
        book_name, _, _, _ = book_info
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(book_name)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("temp_qr_code.png")
        self.showQRCode()

    def showQRCode(self):
        Book.qr_show(self)


    def reserveBook(self, book_info):
        Book.reserve_book(self, book_info)
```
# Окно справки. Листинг программы:
``` python
class Ui_HelpWindow(object):
    def setupUi(self, HelpWindow):
        HelpWindow.setObjectName("Справка")
        HelpWindow.resize(700, 450)
        self.centralwidget = QtWidgets.QWidget(HelpWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
        self.textEdit.setText("""
            Получение библиотечного кода:

        Нажмите кнопку "Получить библиотечный код" для получения вашего библиотечного кода, необходимого для доступа к ресурсам библиотеки.

            Доступ к электронной библиотеке:

        Нажмите кнопку "Электронная библиотека", чтобы получить доступ к цифровой коллекции книг и ресурсов.

            Просмотр новых поступлений:

        Нажмите кнопку "Новые поступления", чтобы увидеть последние добавления в коллекцию библиотеки.

            Поиск книг и ресурсов:

        Используйте функцию поиска, чтобы найти нужные книги и ресурсы по названию, автору или ключевому слову.

            Личный кабинет:

        Нажмите кнопку "Ваш кабинет", чтобы получить доступ к вашему личному кабинету для управления учетной записью.

            Регистрация новой учетной записи:

        Новые пользователи могут зарегистрироваться, нажав кнопку "Получить библиотечный код" и заполнив форму регистрации.

            Отображение QR-кода:

        Нажмите на название книги в результатах поиска, чтобы просмотреть QR-код, упрощающий доступ к деталям книги.

        При необходимости помощи или дополнительной информации обращайтесь к справке или обратитесь к администратору системы.
        """)
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        HelpWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(HelpWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        HelpWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(HelpWindow)
        self.statusbar.setObjectName("statusbar")
        HelpWindow.setStatusBar(self.statusbar)

        self.retranslateUi(HelpWindow)
        QtCore.QMetaObject.connectSlotsByName(HelpWindow)

    def retranslateUi(self, HelpWindow):
        _translate = QtCore.QCoreApplication.translate
        HelpWindow.setWindowTitle(_translate("HelpWindow", "Справка"))
```
# Вход в личный кабинет. Листинг программы:
``` python
class Ui_PersonalArea(object):
    def setupUi(self, PersonalArea): 
        PersonalArea.setObjectName("PersonalArea")
        PersonalArea.resize(450, 220)
        self.centralwidget = QtWidgets.QWidget(PersonalArea)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 400, 25))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 400, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 400, 25))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 110, 400, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 150, 120, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 150, 270, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        PersonalArea.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PersonalArea)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 21))
        self.menubar.setObjectName("menubar")
        PersonalArea.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PersonalArea)
        self.statusbar.setObjectName("statusbar")
        PersonalArea.setStatusBar(self.statusbar)

        self.PersonalArea = PersonalArea  # Сохраняем ссылку на окно

        self.profile_window = None

        self.retranslateUi(PersonalArea)
        QtCore.QMetaObject.connectSlotsByName(PersonalArea)
        self.pushButton.clicked.connect(self.myFunction_auth)
        self.pushButton_2.clicked.connect(self.show_email_dialog)

    def retranslateUi(self, PersonalArea):
        _translate = QtCore.QCoreApplication.translate
        PersonalArea.setWindowTitle(_translate("PersonalArea", "Вход в личный кабинет"))
        self.label.setText(_translate("PersonalArea", "Библиотечный код или email"))
        self.label_2.setText(_translate("PersonalArea", "Пароль (дата рождения в формате ГГГГММДД):"))
        self.pushButton.setText(_translate("PersonalArea", "Войти"))
        self.pushButton_2.setText(_translate("PersonalArea", "Забыли свой библиотечный код?"))

    def myFunction_auth(self, e):
        User.auth(self, e)

    def show_email_dialog(self):
        email, ok_pressed = QtWidgets.QInputDialog.getText(None, "Восстановление библиотечного кода", "Введите свою почту:")
        if ok_pressed and email:
            new_lib_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))  # генерация нового библиотечного кода
            self.send_new_lib_code(email, new_lib_code)

    def send_new_lib_code(self, email, new_lib_code):
        # отправка нового библиотечного кода на почту
        QtWidgets.QMessageBox.information(None, 'Успешно', f'Новый библиотечный код отправлен вам на почту: {email}')

        # Обновление библиотечного кода в Excel файле
        filename = 'Список пользователей.xlsx'
        wb = op.load_workbook(filename)
        sheet = wb.active
        for row in sheet.iter_rows(min_row=4, max_row=sheet.max_row, min_col=6, max_col=6):
            for cell in row:
                if cell.value == email:
                    sheet.cell(row=cell.row, column=8).value = new_lib_code
                    break
        wb.save(filename)
```
# Окно регистрации. Листинг программы:
``` python
class Ui_RegistrationWindow(object): 
    def setupUi(self, RegistrationWindow): 
        RegistrationWindow.setObjectName("RegistrationWindow")
        RegistrationWindow.resize(450, 550)
        self.centralwidget = QtWidgets.QWidget(RegistrationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(65, 30, 310, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 110, 400, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 140, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(30, 170, 400, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 200, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(30, 230, 400, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 260, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(30, 290, 400, 25))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 320, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(30, 350, 400, 25))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(30, 380, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(30, 410, 400, 25))
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(125, 460, 200, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        RegistrationWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RegistrationWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 21))
        self.menubar.setObjectName("menubar")
        RegistrationWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RegistrationWindow)
        self.statusbar.setObjectName("statusbar")
        RegistrationWindow.setStatusBar(self.statusbar)

        self.comboBox.setCurrentIndex(0)
        self.comboBox.addItems('студенты магистранты аспиранты докторанты преподаватели'.split())
        self.pushButton.clicked.connect(self.myFunction_reg)

        self.retranslateUi(RegistrationWindow)
        QtCore.QMetaObject.connectSlotsByName(RegistrationWindow)

def retranslateUi(self, RegistrationWindow):
        _translate = QtCore.QCoreApplication.translate
        RegistrationWindow.setWindowTitle(_translate("RegistrationWindow", "Регистрация"))
        self.label.setText(_translate("RegistrationWindow", "Регистрация библиотечного кода"))
        self.label_2.setText(_translate("RegistrationWindow", "Фамилия:"))
        self.label_3.setText(_translate("RegistrationWindow", "Имя:"))
        self.label_4.setText(_translate("RegistrationWindow", "Отчество (при наличии):"))
        self.label_5.setText(_translate("RegistrationWindow", "Дата рождения:"))
        self.label_6.setText(_translate("RegistrationWindow", "email:"))
        self.label_7.setText(_translate("RegistrationWindow", "Выберите категорию:"))
        self.pushButton.setText(_translate("RegistrationWindow", "Зарегистрироваться"))

    def myFunction_reg(self):
        User.reg(self)
```
# Кабинет пользователя. Листинг программы:
``` python
class Ui_Profil(object):
    def setupUi(self, Profil, user_info):
        Profil.setObjectName("Profil")
        Profil.resize(400, 400)
        self.centralwidget = QtWidgets.QWidget(Profil)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 20, 100, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 130, 360, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 170, 360, 31))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 210, 131, 30))
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 90, 360, 31))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 250, 131, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 330, 131, 30))
        self.pushButton_3.setObjectName("pushButton_3")
        Profil.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Profil)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        Profil.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Profil)
        self.statusbar.setObjectName("statusbar")
        Profil.setStatusBar(self.statusbar)

        self.retranslateUi(Profil, user_info)
        QtCore.QMetaObject.connectSlotsByName(Profil)

    def retranslateUi(self, Profil, user_info):
        _translate = QtCore.QCoreApplication.translate
        Profil.setWindowTitle(_translate("Profil", "Профиль"))
        self.label.setText(_translate("Profil", "Профиль"))
        self.label_2.setText(_translate("Profil", f"Библиотечный код: {user_info['lib_code']}"))
        self.label_3.setText(_translate("Profil", f"Почта: {user_info['email']}"))
        self.label_4.setText(_translate("Profil", f"{user_info['last_name']} {user_info['first_name']} {user_info['middle_name']}"))
        self.pushButton.setText(_translate("Profil", "Выданные издания"))
        self.pushButton_2.setText(_translate("Profil", "Подписные ресурсы"))
        self.pushButton_3.setText(_translate("Profil", "Выйти"))
```
# Регистрация пользователя. Листинг программы:
``` python
class Ui_RegistrationWindow(object): 
    def setupUi(self, RegistrationWindow): 
        RegistrationWindow.setObjectName("RegistrationWindow")
        RegistrationWindow.resize(450, 550)
        self.centralwidget = QtWidgets.QWidget(RegistrationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(65, 30, 310, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 110, 400, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 140, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(30, 170, 400, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 200, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(30, 230, 400, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 260, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(30, 290, 400, 25))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 320, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(30, 350, 400, 25))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(30, 380, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(30, 410, 400, 25))
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(125, 460, 200, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        RegistrationWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RegistrationWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 21))
        self.menubar.setObjectName("menubar")
        RegistrationWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RegistrationWindow)
        self.statusbar.setObjectName("statusbar")
        RegistrationWindow.setStatusBar(self.statusbar)

        self.comboBox.setCurrentIndex(0)
        self.comboBox.addItems('студенты магистранты аспиранты докторанты преподаватели'.split())
        self.pushButton.clicked.connect(self.myFunction_reg)

        self.retranslateUi(RegistrationWindow)
        QtCore.QMetaObject.connectSlotsByName(RegistrationWindow)

    def retranslateUi(self, RegistrationWindow):
        _translate = QtCore.QCoreApplication.translate
        RegistrationWindow.setWindowTitle(_translate("RegistrationWindow", "Регистрация"))
        self.label.setText(_translate("RegistrationWindow", "Регистрация библиотечного кода"))
        self.label_2.setText(_translate("RegistrationWindow", "Фамилия:"))
        self.label_3.setText(_translate("RegistrationWindow", "Имя:"))
        self.label_4.setText(_translate("RegistrationWindow", "Отчество (при наличии):"))
        self.label_5.setText(_translate("RegistrationWindow", "Дата рождения:"))
        self.label_6.setText(_translate("RegistrationWindow", "email:"))
        self.label_7.setText(_translate("RegistrationWindow", "Выберите категорию:"))
        self.pushButton.setText(_translate("RegistrationWindow", "Зарегистрироваться"))

    def myFunction_reg(self):
        User.reg(self)
```
# Новые поступления. Листинг программы:
``` python
class Ui_NewArrivalsWindow(object):
    def setupUi(self, NewArrivalsWindow, bookListWidget):
        NewArrivalsWindow.setObjectName("NewArrivalsWindow")
        NewArrivalsWindow.resize(400, 220)
        self.centralwidget = QtWidgets.QWidget(NewArrivalsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(107, 30, 185, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 130, 20))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 90, 360, 25))
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 130, 120, 30))
        self.pushButton.setObjectName("pushButton")
        NewArrivalsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(NewArrivalsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        NewArrivalsWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(NewArrivalsWindow)
        self.statusbar.setObjectName("statusbar")
        NewArrivalsWindow.setStatusBar(self.statusbar)

        self.bookListWidget = bookListWidget  # Сохраняем переданный виджет

        self.comboBox.setCurrentIndex(0)
        self.comboBox.addItems(['за этот месяц','с прошлого месяца','с позапрошлого месяца'])

        self.retranslateUi(NewArrivalsWindow)
        QtCore.QMetaObject.connectSlotsByName(NewArrivalsWindow)

        self.pushButton.clicked.connect(self.showBooks)

    def retranslateUi(self, NewArrivalsWindow):
        _translate = QtCore.QCoreApplication.translate
        NewArrivalsWindow.setWindowTitle(_translate("NewArrivalsWindow", "Новые поступления"))
        self.label.setText(_translate("NewArrivalsWindow", "Новые поступления"))
        self.label_2.setText(_translate("NewArrivalsWindow", "Новые книги в каталоге"))
        self.pushButton.setText(_translate("NewArrivalsWindow", "Показать"))

    def showBooks(self):
        # Получаем выбранный тип поступления
        selected_type = self.comboBox.currentText()

        # Открываем файл Excel и читаем данные
        filename = 'Список книг библиотеки.xlsx'
        wb = op.load_workbook(filename, data_only=True)
        sheet = wb.active
        max_rows = sheet.max_row

        found_books = []

        # Проверяем каждую строку в Excel на соответствие выбранному типу поступления
        for i in range(3, max_rows + 1):
            type_of_arrival = str(sheet.cell(row=i, column=5).value)  # 5 столбец в файле Excel

            # Проверяем соответствие типа поступления
            if type_of_arrival == selected_type:
                name_aut = str(sheet.cell(row=i, column=3).value)
                book_name = str(sheet.cell(row=i, column=2).value)
                art = str(sheet.cell(row=i, column=4).value)
                # Добавляем количество книг из шестого столбца
                quantity = str(sheet.cell(row=i, column=6).value)
                found_books.append((book_name, name_aut, art, quantity))

        # Очищаем виджет списка книг
        self.bookListWidget.clear()

        # Если найдены книги, добавляем их в список
        if found_books:
            for book in found_books:
                item = QtWidgets.QListWidgetItem(f"{book[0]} - {book[1]} - {book[2]} - Количество: {book[3]}")
                self.bookListWidget.addItem(item)
                item.setData(QtCore.Qt.UserRole, book)
```
# Подписные ресурсы. Листинг программы:
``` python
class SubscriptionWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Подписка")
        layout = QtWidgets.QVBoxLayout()
        self.subscribe_button = QtWidgets.QPushButton("Подписаться")
        self.unsubscribe_button = QtWidgets.QPushButton("Отписаться")
        layout.addWidget(self.subscribe_button)
        layout.addWidget(self.unsubscribe_button)
        self.setLayout(layout)

class Ui_SubResourcesWindow(object):
    def setupUi(self, SubResourcesWindow):
        SubResourcesWindow.setObjectName("SubResourcesWindow")
        SubResourcesWindow.resize(500, 500)
        self.centralwidget = QtWidgets.QWidget(SubResourcesWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 40, 261, 25))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 80, 235, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(255, 80, 235, 25))
        self.comboBox_2.setObjectName("comboBox_2")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 120, 391, 331))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(410, 120, 81, 31))
        self.pushButton.setObjectName("pushButton")
        SubResourcesWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SubResourcesWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        SubResourcesWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SubResourcesWindow)
        self.statusbar.setObjectName("statusbar")
        SubResourcesWindow.setStatusBar(self.statusbar)
        
        self.comboBox.setCurrentIndex(0)
        self.comboBox.addItems(['все темы','авиационная и космическая техника','автоматика и управление','архитектура и строительство',
        'гуманитарные науки','культура и искусство','социальные науки','физико-математические науки'])
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_2.addItems(['все материалы','база знаний','видео','книги','лекции','материалы конференций','технические документы','справочные издания'])

        self.retranslateUi(SubResourcesWindow)
        QtCore.QMetaObject.connectSlotsByName(SubResourcesWindow)

        self.pushButton.clicked.connect(self.showResources)
        self.listWidget.itemClicked.connect(self.showSubscriptionWindow)

    def retranslateUi(self, SubResourcesWindow):
        _translate = QtCore.QCoreApplication.translate
        SubResourcesWindow.setWindowTitle(_translate("SubResourcesWindow", "Список подписных ресурсов"))
        self.label.setText(_translate("SubResourcesWindow", "Список подписных ресурсов"))
        self.pushButton.setText(_translate("SubResourcesWindow", "Показать"))

    def showResources(self):
        # Получаем выбранные категории
        selected_theme = self.comboBox.currentText()
        selected_material = self.comboBox_2.currentText()

        # Открываем файл Excel и читаем данные
        filename = 'Список подписных ресурсов.xlsx'
        wb = op.load_workbook(filename, data_only=True)
        sheet = wb.active
        max_rows = sheet.max_row

        found_resources = []

        # Проверяем каждую строку в Excel на соответствие выбранным категориям
        for i in range(2, max_rows + 1):
            theme = str(sheet.cell(row=i, column=3).value)  # 3 столбец - тема
            material = str(sheet.cell(row=i, column=4).value)  # 4 столбец - материалы

            # Проверяем соответствие категориям
            if (selected_theme == 'все темы' or selected_theme == theme or selected_theme == '') and \
            (selected_material == 'все материалы' or selected_material == material or selected_material == ''):
                resource_name = str(sheet.cell(row=i, column=2).value)  # 2 столбец - название ресурса
                if resource_name:
                    found_resources.append(resource_name)

        # Очищаем виджет списка ресурсов
        self.listWidget.clear()

        # Если найдены ресурсы, добавляем их в список
        if found_resources:
            for resource in found_resources:
                item = QtWidgets.QListWidgetItem(resource)
                self.listWidget.addItem(item)

    def showSubscriptionWindow(self, item):
        subscription_window = SubscriptionWindow()
        subscription_window.exec_()
```
# Выход из программы. Листинг программы:
``` python
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
 ```
