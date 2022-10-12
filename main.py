import requests
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def clear_weekends(date_lists):
    return [d for d in date_list if d.isoweekday() < 6]


def to_date(s):
    d = datetime.strptime(s, '%b %d')
    dd = datetime.strptime(d.strftime(f'{datetime.now().year}-%m-%d'),'%Y-%m-%d')
    return dd

def parse_inside(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    screen = requests.get(url,headers=headers)
    table = pd.read_html(screen.text)[-1]
    table.columns = table.iloc[0]
    table = table[1:]
    return table


table = parse_inside("https://finviz.com/insidertrading.ashx?or=-10&tv=100000&tc=2&o=-transactionvalue")

for i in range(0, 5):
    ryh = table.iloc[[i]]
    d = datetime.today() - to_date(ryh.values[0][3]) + timedelta(days=6)
    date_list = [datetime.today() - timedelta(days=x) for x in range(d.days)]
    date_list = clear_weekends(date_list)
    start_date = to_date(ryh.values[0][3]) - timedelta(days=5)

    ticker = yf.Ticker(ryh.values[0][0]).history(start=start_date, end=datetime.now(), frequency='1dy')[
        ['Open', 'High', 'Low', 'Close']]
    print(i + 1, ryh.values[0][0], " ", ryh.values[0][3], " ", ryh.values[0][4], " ", ryh.values[0][5], " ",
          ryh.values[0][9])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(ticker)
    data = pd.DataFrame(ticker)
    data['date'] = date_list
    data.plot(x='date', y='Close',
              title=f'{i + 1}) Ticker: {ryh.values[0][0]}, {ryh.values[0][4]}, Price:{ryh.values[0][5]}$')
    plt.axvline(pd.Timestamp(to_date(ryh.values[0][3])), color='r')
    secform = to_date(ryh.values[0][9].split()[0] + ' ' + ryh.values[0][9].split()[1])
    plt.axvline(pd.Timestamp(secform.date()), color='g')
    plt.show()
    print(
        "-------------------------------------------------------------------------------------------------------------------------------------------------")
