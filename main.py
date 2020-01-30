import fix_qt_import
from weather_pyqt import MainForm
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
import sys
from weather import get_weather, get_title, get_general_information, get_temp_and_wind, get_wind_chill


class ExtendedApplication(MainForm):
    def __init__(self):
        super().__init__()
        self.update_button.clicked.connect(self.set_label)
        self.redirect_button.clicked.connect(self.go_to_site)
        self.set_label()
        self.setWindowIcon(QtGui.QIcon('favicon.ico'))
        self.weather_timer.timeout.connect(self.set_label)
        self.weather_timer.start(1000 * 60 * 30)

    @staticmethod
    def go_to_site():
        QDesktopServices.openUrl(QUrl('www.kolgimet.ru'))

    def set_label(self):
        time_str = "Последнее обновление: {0}".format(QtCore.QTime.currentTime().toString())
        self.labelupdatetime.setText(time_str)

        lst = get_weather()
        self.labeltitle.setText(get_title(lst))
        self.labelweatherdescription.setText(lst[1])

        now_weather_list = get_general_information(lst)
        t, w = get_temp_and_wind(now_weather_list)
        result, result_description = get_wind_chill(t, w)

        self.labelweathervalues.setText("\n".join(now_weather_list))
        self.labelfelttext.setText(f'Ощущается как: {result}')
        self.labelfeltdescription.setText(result_description)

    def button_clicked(self):
        self.set_label()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExtendedApplication()
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
