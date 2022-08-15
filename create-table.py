import mysql.connector as msql
import csv
import pandas as pd
from datetime import datetime

db_name = 'spbdb'
file_name = 'data/spb-rentals-2021-jun'

conn = msql.connect(host='127.0.0.1', user='root',  
                        password='akulabutaforia42', db=db_name, charset='utf8')
cursor = conn.cursor()
print('Connected')

df = pd.read_csv(file_name + '.csv', encoding='utf-16', delimiter='\t')
print('File has been read')

df = df.where(pd.notnull(df), None)
df = df.drop_duplicates()

cursor.execute('TRUNCATE spb_rent_jun')

for index, row in df.iterrows():
	id = int(row.iloc[0])
	ad_date = pd.to_datetime(row.iloc[1], format='%d.%m.%Y').strftime('%Y-%m-%d')
	flat_type = row.iloc[2] or ''
	house_type = row.iloc[3] or ''
	constr_date = row.iloc[4] or ''
	floor = row.iloc[5] or ''
	address = row.iloc[6] or ''
	x_coor = float(row.iloc[7] or 0)
	y_coor = float(row.iloc[8] or 0)
	metro = row.iloc[9] or ''
	metro_dist = int(row.iloc[10] or 0)
	area = float(row.iloc[11] or 0)
	kitchen = float(row.iloc[12] or 0)
	liv_area = row.iloc[13] or ''
	rent = int(row.iloc[14] or 0)
	utilities = int(row.iloc[15] or 0)
	fees_perc = int(row.iloc[16] or 0)
	fees_abs = int(row.iloc[17] or 0)
	total_pay = int(row.iloc[18] or 0)
	cursor.execute('INSERT INTO spb_rent_jun VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
		(id, ad_date, flat_type, house_type, constr_date, floor, address, x_coor, y_coor, metro, metro_dist, area, kitchen, liv_area, \
		rent, utilities, fees_perc, fees_abs, total_pay))

conn.commit()
print('Data inserted into table')