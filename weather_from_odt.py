# install pandas
# install odfpy

import pandas as pd
from datetime import date, timedelta
from odf import text, teletype
from odf.opendocument import load
import re

#-------- Parsing days temperature from ODT-file --------

file = 'parsing_odt_src.odt'

def read_odt_with_odfpy(file_path):
    # Load the document
    textdoc = load(file_path)
    
    
    # Find all paragraph elements
    paragraphs = textdoc.getElementsByType(text.P)
    
    # Extract text from each paragraph
    for paragraph in paragraphs:
        paragraph_text = teletype.extractText(paragraph)
        matches = re.findall(r'\d+-\d+°', paragraph_text, re.IGNORECASE) # Find matches "10-15°"
        if matches != []:
            return matches
        

weather_temp = read_odt_with_odfpy(file)
weather_chita = weather_temp[5].rstrip('°') # 10-15° -> 10-15
a, b = map(int, weather_chita.split('-')) # 10-15 -> 10 15 and mapping on two variables
weather_chita_average = int((a + b) / 2)

print(weather_chita_average)

#-------- Parsing days temperature from ODT-file end --------


#-------- Convert ODT-spreadshit to Pandas DataFrame and write CSV-file --------
df = pd.read_excel('weather_src_odt.odt', engine='odf', skiprows=1, header=0)

print(df.head())

months = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}

df = df.drop(columns=['Ночью'])
new_row = pd.DataFrame([{"Осадки": "переменная облачность", "Днем": weather_chita_average, "Населенные пункты": "Чита"}])
df = pd.concat([new_row, df], ignore_index=True)

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
    
#-------- Convert ODT-spreadshit to Pandas DataFrame and write CSV-file end --------

file = 'parsing_odt_src.odt'
textdoc = load(file)
print(textdoc)
paragraphs = textdoc.getElementsByType(text.P)

#-------- Testing method for extracting precipitation state --------
text_content = [teletype.extractText(p) for p in paragraphs]
chita = text_content[text_content.index('ПО ЧИТЕ:'):]
chita_str = ", ".join(chita)
print(chita)
matches = re.findall(r'\d+-\d+°', chita_str, re.IGNORECASE)
print(matches)
