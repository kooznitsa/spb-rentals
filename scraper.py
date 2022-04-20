from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from datetime import timedelta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

quote_pages = []

for num in range(1,3):
    url = f'https://emls.ru/arenda/page{num}.html?query=s/1/r0/1/type/2/rtype/2/place/address/reg/2/dept/2/sort1/4/dir1/1/dir2/2/interval/3'
    quote_pages.append(url)

for num in range(1,7):
    url = f'https://emls.ru/arenda/page{num}.html?query=s/1/r1/1/type/2/rtype/2/place/address/reg/2/dept/2/sort1/4/dir1/1/dir2/2/interval/3'
    quote_pages.append(url)

for num in range(1,7):
    url = f'https://emls.ru/arenda/page{num}.html?query=s/1/r2/1/r3/1/r4/1/r5/1/r6/1/type/2/rtype/2/place/address/reg/2/dept/2/sort1/4/dir1/1/dir2/2/interval/3'
    quote_pages.append(url)

data = []

for pg in quote_pages:
    req = Request(url=pg, headers=headers)
    try:
        page = urlopen(req)
    except:
        continue
    soup = BeautifulSoup(page, 'html.parser')

    listings = soup.findAll('a', class_='row')
    for l in listings:
        next_elem = l.find('div', class_='shift-line')
        flat_type = getattr(next_elem.find_previous_sibling('div'), 'text', None)
        house_type = getattr(l.findAll('div', class_='series')[2], 'text', None)
        year = getattr(l.find('div', class_='w-year').find('div', class_='ellipsis').find('b'), 'text', None)
        floor = getattr(l.find('div', class_='w-floor').find('div').find('b'), 'text', None)
        
        address = getattr(l.find('a', class_='address-geo'), 'text', None)
        try:
            coor = l.find('a', {'class':'address-geo'})['href']
            x_coor = coor.rsplit('y', 2)[1][3:-1]
            y_coor = coor.rsplit('y', 1)[1][1:]
        except:
            x_coor = None
            y_coor = None
        try:
            metro_station = getattr(l.find('div', class_='metroline-2').find('div', class_='ellipsis'), 'text', None)
        except:
            maetro_station = None
        try:
            metro_m = getattr(l.find('div', class_='ellipsis em'), 'text', None)
            metro_m = metro_m.rsplit('метров', 1)[0].replace(' ', '')
        except:
            metro_m = None
        
        total_area = getattr(l.find('b', class_='space-all'), 'text', None)
        kitchen_area = getattr(l.find('td', {'align' : 'right'}), 'text', None)
        try:
            kitchen_area = kitchen_area.rsplit('кухня: ', 1)[1]
        except:
            kitchen_area = None
        living_area = getattr(l.find('div', class_='ellipsis shift-line').find('b'), 'text', None)
        
        rent = getattr(l.find('div', class_='price'), 'text', None).replace(' ', '')
        rent = int(''.join(list(filter(str.isdigit, rent))))
        try:
            utilities_text = getattr(l.findAll('div', class_='align-r')[1], 'text', None)
            utilities_f = int(''.join(list(filter(str.isdigit, str(utilities_text)))))
            utilities = 0 if utilities_text == 'КУ включены' else utilities_f
        except:
            utilities = None
        fees_pc = getattr(l.find('div', class_='comission-border'), 'text', None)[:-1]
        fees_abs = int(fees_pc) / 100 * int(rent)
        total_price = rent if utilities == None else rent + utilities

        date_text = getattr(l.find('div', class_='w-date'), 'text', None)
        today = datetime.today().strftime('%d.%m.%Y')
        yesterday =datetime.strftime(datetime.now() - timedelta(1), '%d.%m.%Y')
        date = today if date_text == 'сегодня' else yesterday if date_text == 'вчера' else date_text

        description = getattr(l.find('div', class_='description'), 'text', None)
        listing_id = getattr(l.find('div', class_='fullinfo-id series').find('b'), 'text', None)[9:]

        data.append((listing_id, date, flat_type, house_type, year, floor, address, x_coor, y_coor, 
                                metro_station, metro_m, total_area, kitchen_area, living_area, rent, utilities, 
                                fees_pc, fees_abs, total_price, description))

filename = 'data/jul-2021/spb-rentals-2021-jul'
columns = ['ID', 'Дата', 'Тип жилья', 'Тип дома', 'Год постройки', 'Этаж', 'Адрес', 'X', 'Y', 
                'Станция метро', 'Расстояние до метро, м', 'Общая площадь, м', 'Площадь кухни, м', 
                'Жилая площадь, м', 'Аренда, руб./мес.', 'Ком. платежи, руб./мес.', 'Комиссия, %', 
                'Комиссия, руб.', 'Общий платеж, руб./мес', 'Описание']

with open(filename + '.csv', 'w', encoding='utf-16') as csv_file:
    writer = csv.writer(csv_file, lineterminator='\n', delimiter ='\t')
    writer.writerow((columns))
    writer.writerows(data)