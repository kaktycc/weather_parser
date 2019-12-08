import sys
from PyQt5 import QtWidgets, QtCore
import datetime
from weather import get_weather, get_title, get_general_information, get_temp_and_wind, get_wind_chill


class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(330, 440)
        self.setWindowTitle('Информация с сайта kolgimet.ru')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        # ag = QtWidgets.QDesktopWidget().availableGeometry()
        # # print(ag.width())
        # widget = self.geometry()
        # x = ag.width() - widget.width() + 1903
        # y = 0
        # self.move(x, y)

        self.to_corner_on_top()

        self.labeltime = QtWidgets.QLabel()
        self.labelupdatetime = QtWidgets.QLabel()

        self.labeltitle = QtWidgets.QLabel()
        self.labeltitle.setStyleSheet("font: 16pt Comic Sans MS")
        # self.label1.setFixedSize(650, 30)
        self.labeltitle.setWordWrap(True)
        self.labelweatherdescription = QtWidgets.QLabel()
        self.labelweatherdescription.setWordWrap(True)
        self.labelweatherdescription.setStyleSheet("font: 12pt Comic Sans MS;color: rgb(0,100,1)")
        self.labelweatherdescription.setGeometry(QtCore.QRect(0, 0, 10, 10))
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
        self.update_button = QtWidgets.QPushButton('Update', self)
        self.update_button.setToolTip('Example')
        self.update_button.resize(330,30)
        self.update_button.clicked.connect(self.set_label)
        # .QTimer
        # self.setFixedSize()
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.update_labeltime)
        # self.timer.start(1000)  # repeat self.update_labelTime every 1 sec
        self.set_label()
        self.weather_timer = QtCore.QTimer()
        self.weather_timer.timeout.connect(self.set_label)
        # полчаса
        self.weather_timer.start(1000 * 60 * 30)
        # self.weather_timer.start(6000)

    def to_corner_on_top(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = screen.width() - widget.width()
        y = 0
        self.move(x, y)

    def update_labeltime(self):
        time_str = "Текущее время: {0}".format(QtCore.QTime.currentTime().toString())
        self.labeltime.setText(time_str)

    def set_label(self):
        # self.label0.setText(str(datetime.datetime.today()))
        time_str = "Последнее обновление: {0}".format(QtCore.QTime.currentTime().toString())
        self.labelupdatetime.setText(time_str)

        lst = get_weather()
        self.labeltitle.setText(get_title(lst))
        self.labelweatherdescription.setText(lst[1])

        now_weather_list = get_general_information(lst)
        t,w = get_temp_and_wind(now_weather_list)
        rezult, rezult_description = get_wind_chill(t,w)

        self.labelweathervalues.setText("\n".join(now_weather_list))
        self.labelfelttext.setText(f'Ощущается как: {rezult}')
        self.labelfeltdescription.setText(rezult_description)

    def button_clicked(self):
        self.set_label()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
