from bs4 import BeautifulSoup
import requests
import re

def get_weather():
    url = 'http://www.kolgimet.ru/'
    try:
        html = requests.get(url).text
    except requests.exceptions.ConnectionError:
        info = ['0', '0', 'Информация с сайта НЕ получена']
        return info
    soup = BeautifulSoup(html, "lxml")

    info = [soup.find('h1').text.strip(), soup.find_all('p')[3].text.strip(),
            soup.find('div', attrs={'class': 'weatherce-main'}).text.strip()]

    return info


def get_title(general_info):
    general_info[0] = " ".join(general_info[0].split()).split(' ')
    title = general_info[0][0]
    for i in general_info[0][5:]:
        title += ' ' + i
    return title


def get_general_information(info_list):
    datetime_temp_wind_list = []
    info_list[2] = info_list[2].split('\n')
    for elem in info_list[2]:
        if info_list[2].index(elem) == 0 or info_list[2].index(elem) == 2 or info_list[2].index(elem) == 3:
            datetime_temp_wind_list.append(elem)
    return datetime_temp_wind_list


def get_temp_and_wind(datetime_temp_wind_list):
    wnd = 0
    print(datetime_temp_wind_list)
    try:
        get_wind = re.sub('\s+', ' ', datetime_temp_wind_list[2].strip())
        if '-' in get_wind:
            get_wind = get_wind.split(' ')[2].split('-')
        else:
            #  Если одно число
            get_wind = int(get_wind.split(' ')[1])
    except IndexError:
        get_wind = 0
    if not isinstance(get_wind, int):
        if len(get_wind) > 1:
            wnd = (int(get_wind[1]) + int(get_wind[0])) / 2
        else:
            wnd = get_wind[0]
    try:
        temperature = int(datetime_temp_wind_list[1])
    except IndexError:
        temperature = -500

    return temperature, wnd


def get_wind_chill(t, w):
    # t = 24
    # w = 6
    if w != 0.0:
        wkm = float(w) * 3.6
        result = 13.12 + (0.6215 * t) - (11.37 * (wkm ** 0.16)) + (0.3965 * t * (wkm ** 0.16))
        # print(result)
        result = round(result, 2)
    else:
        result = t
    result_description = ''
    if result == -500:
        result_description = '''Ошибка получения данных'''
    elif -10 <= result <= 0:
        result_description = '''Небольшой риск, некоторый дискомфорт.
        Рекомендуется тепло одеваться и оставаться сухим.'''
    elif -27 <= result <= -10:
        result_description = '''Дискомфорт, риск гипотермии в случае продолжительного нахождения на воздухе без 
        соответствующей защиты. Рекомендуется одеваться в несколько слоев теплой одежды, внешний слой не должен 
        пропускать ветра. Рекомендуется носить шапку, варежки или перчатки, шарф и закрытую, непромокаемую обувь. 
        Надо оставаться сухим и на морозе двигаться. '''
    elif -39 <= result <= -28:
        result_description = '''Открытая кожа может замерзнуть в течении 10-30 минут. Существует риск обморожения: 
        требуется проверять лицо, открытые участки кожи и конечности на окоченение и побеление. Риск гипотермии в 
        случае продолжительного нахождения на воздухе без соответствующей одежды или укрытия от холода и ветра. 
        Рекомендуется одеваться в несколько слоев теплой одежды, внешний слой не должен пропускать ветра. 
        Рекомендуется не оставлять открытых участков кожи. Рекомендуется носить шапку, варежки или перчатки, шарф, 
        маску и закрытую, непромокаемую обувь. Надо оставаться сухим и на морозе двигаться. '''
    elif -47 <= result <= -40:
        result_description = '''Открытая кожа может замерзнуть в течении 5-10 минут. Высокий риск обморожения: 
        требуется проверять лицо, открытые участки кожи и конечности на окоченение и побеление. Риск гипотермии в 
        случае продолжительного нахождения на воздухе без соответствующей одежды или укрытия от холода и ветра. 
        Рекомендуется одеваться в несколько слоев теплой одежды, внешний слой не должен пропускать ветра. 
        Рекомендуется не оставлять открытых участков кожи. Рекомендуется носить шапку, варежки или перчатки, шарф, 
        маску и закрытую, непромокаемую обувь. Надо оставаться сухим и на морозе двигаться '''
    elif -54 < result < -48:
        result_description = '''Открытая кожа может замерзнуть в течении 2–5 минут. Очень высокий риск обморожения: 
        требуется проверять лицо, открытые участки кожи и конечности на окоченение и побеление. Серьезный риск 
        гипотермии в случае продолжительного нахождения на воздухе без соответствующей одежды или укрытия от холода и 
        ветра. Требуется осторожность при пребывании на улице. Рекомендуется одеваться в несколько слоев теплой 
        одежды, внешний слой не должен пропускать ветра. Рекомендуется не оставлять открытых участков кожи. 
        Рекомендуется носить шапку, варежки или перчатки, шарф, маску и закрытую, непромокаемую обувь. Старайтесь 
        отменить или сократить выходы на улицу. Оставайтесь сухим и двигайтесь. '''

    return result, result_description


if __name__ == '__main__':
    lst = get_weather()
    get_title(lst)
    new_lst = get_general_information(lst)
    temp, wind = get_temp_and_wind(new_lst)
    print(get_wind_chill(temp, wind))
