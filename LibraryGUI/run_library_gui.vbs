Set shell = CreateObject("WScript.Shell")

' Путь к основному файлу приложения
scriptPath = "C:\Users\kobel\Documents\LibraryGUI\main_gui.py"

' Запуск через pythonw (без консольного окна)
shell.Run "pythonw """ & scriptPath & """", 0, False

