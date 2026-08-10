# install pandas
# install odfpy

import pandas as pd
from datetime import date, timedelta

df = pd.read_excel('weather_src_odt.odt', engine='odf')
print(df.head())

months = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}

df = df.drop(columns=['Ночью'])
today = date.today() + timedelta(days=1)
d_date = today.strftime("%d").replace('0', '')
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

with open("output.csv", "a") as file:
    file.write(w_str)