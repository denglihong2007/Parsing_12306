import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from functools import partial
import use
import gui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.sure_date.clicked.connect(partial(use.sure_date,ui))
    ui.sure_train_number.clicked.connect(partial(use.sure_train_number,ui))
    ui.sure_proxy.clicked.connect(partial(use.sure_proxy,ui))
    ui.quit.clicked.connect(use.quit)
    ui.save.clicked.connect(use.save)
    sys.exit(app.exec_())
