import main
import openpyxl
import pandas as pd
ticker = 'AAPL'
sma = main.get_format_sma(ticker, 50)
# ema = main.get_format_ema(ticker)
# daterange = main.get_daterange(sma)
# price = main.get_format_price(ticker, daterange[0], daterange[1])
# print(price)
# stock_data = pd.concat([sma, ema, price])
# stock_data.to_excel('data.xlsx', index=False)
# print('done')
# stock_data = main.get_format_macd(ticker)
# stock_data = pd.DataFrame(stock_data)
# stock_data.to_excel('data.xlsx', index=False)
# print('done')
main.calculate_donchian_channel(sma, 0)