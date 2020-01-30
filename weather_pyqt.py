import sys
from PyQt5 import QtWidgets, QtCore


class MainForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(330, 455)
        self.setWindowTitle('Информация с сайта Kolgimet')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        ag = QtWidgets.QDesktopWidget().availableGeometry()
        widget = self.geometry()
        x = ag.width() - widget.width() + 1903
        y = 0
        self.move(x, y)
        self.labeltime = QtWidgets.QLabel()
        self.labelupdatetime = QtWidgets.QLabel()

        self.labeltitle = QtWidgets.QLabel()
        self.labeltitle.setStyleSheet("font: 16pt Comic Sans MS")
        self.labeltitle.setWordWrap(True)

        self.labelweatherdescription = QtWidgets.QLabel()
        self.labelweatherdescription.setWordWrap(True)
        self.labelweatherdescription.setStyleSheet("font: 12pt Comic Sans MS;color: rgb(0,100,1)")
        self.labelweathervalues = QtWidgets.QLabel()
        self.labelweathervalues.setStyleSheet("font: 16pt Comic Sans MS")

        self.labelfelttext = QtWidgets.QLabel()
        self.labelfelttext.setStyleSheet("font: 16pt Comic Sans MS; color: rgb(0,0,150)")

        self.labelfeltdescription = QtWidgets.QLabel()
        self.labelfeltdescription.setWordWrap(True)
        self.labelfeltdescription.setStyleSheet("font: 12pt Comic Sans MS")

        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(self.labeltime)
        lay.addWidget(self.labelupdatetime)
        lay.addWidget(self.labeltitle)
        lay.addWidget(self.labelweatherdescription)
        lay.addWidget(self.labelweathervalues)
        lay.addWidget(self.labelfelttext)
        lay.addWidget(self.labelfeltdescription)
        self.setLayout(lay)
        self.update_button = QtWidgets.QPushButton('Обновить', self)
        self.update_button.setToolTip('Обновить данные')
        self.update_button.resize(330, 30)
        self.redirect_button = QtWidgets.QPushButton('Open on Site', self)
        self.weather_timer = QtCore.QTimer()
        # self.weather_timer.timeout.connect(self.set_label)
        # полчаса
        # self.weather_timer.start(1000 * 60 * 30)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainForm()
    main.show()
    sys.exit(app.exec_())
