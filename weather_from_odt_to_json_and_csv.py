# install pandas
# install odfpy

import pandas as pd
from datetime import date, timedelta
from odf import text, teletype
from odf.opendocument import load
import re

#-------- Parsing days and nights temperature from ODT-file --------

file = 'parsing_odt_src.odt'
textdoc = load(file)
CITY = 'Чита'
paragraphs = textdoc.getElementsByType(text.P)

text_content = [teletype.extractText(p) for p in paragraphs]
chita = text_content[text_content.index('ПО ЧИТЕ:'):]
chita_str = ", ".join(chita)
fallout = chita[1].split('.')
fallout_str = fallout[0].lower()
print(fallout_str)
matches = re.findall(r'\d+-\d+°', chita_str, re.IGNORECASE)
temp_chita_day = matches[1].rstrip('°')
temp_chita_night = matches[0].rstrip('°')
a1, b1 = map(int, temp_chita_day.split('-'))
a2, b2 = map(int, temp_chita_night.split('-'))
temp_chita_average_day = int((a1 + b1) / 2)
temp_chita_average_night = int((a2 + b2) / 2)
print(temp_chita_average_day, temp_chita_average_night)

#-------- Parsing days temperature from ODT-file end --------


#-------- Convert ODT-spreadshit to Pandas DataFrame and write CSV and JSON files --------
src_file = 'weather_src_odt.odt'
df = pd.read_excel(src_file, engine='odf', skiprows=1, header=0)

new_row = pd.DataFrame([{"Осадки": fallout_str, "Ночью": temp_chita_average_night, "Днем": temp_chita_average_day, "Населенные пункты": CITY}])
df = pd.concat([new_row, df], ignore_index=True)

json_string = df.to_json(force_ascii=False, orient='records', indent=4)
df.to_json('output.json', force_ascii=False, orient='records', indent=4)
print(json_string)

df = df.drop(columns=['Ночью'])

months = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}

today = date.today() + timedelta(days=1)
d_date = f'{today.day}'
m_date = f'{months[today.month]}'

df_len = len(df)

for a in range(df_len - 1):
    city = str(df.iloc[a, 2])
    temp = '+' + str(df.iloc[a, 1])
    rainfall = str(df.iloc[a, 0])
    w_str = '   ' + d_date + ' ' + m_date + ': ' + city + '  ' + temp + '  ' + rainfall +'\r\n'
    print('   ' + d_date + ' ' + m_date + ': ' + city + '  ' + temp + '  ' + rainfall +'\r\n')
    
    with open("output.csv", "a") as file:
        file.write(w_str)

city = str(df.iloc[df_len - 1, 2])
temp = '+' + str(df.iloc[df_len - 1, 1])
rainfall = str(df.iloc[df_len - 1, 0])
w_str = '   ' + d_date + ' ' + m_date + ': ' + city + '  ' + temp + '  ' + rainfall
print('   ' + d_date + ' ' + m_date + ': ' + city + '  ' + temp + '  ' + rainfall)

with open("output.csv", "a") as file:
    file.write(w_str)
    
#-------- Convert ODT-spreadshit to Pandas DataFrame and write and JSON files end --------