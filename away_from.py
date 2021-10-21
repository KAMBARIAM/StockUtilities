import datetime
from sys import argv
from nsepy import get_history
import pandas as pd
import json

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()


def print_stocks(past_days = 365):
    start = datetime.datetime.now() - datetime.timedelta(days = past_days)
    end = datetime.datetime.now()
    company_file = open('company.json',)
    company_data = json.load(company_file)
    stock_list = company_data['symbols']
    length_stocks = len(stock_list)
    stocks_info = []
    printProgressBar(0, length_stocks, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, stock_symbol in enumerate(stock_list):
        data = get_history(symbol = stock_symbol, start = start, end = end)
        current_price = data["Close"][-1]
        duration_low  = min(data["Low"])
        duration_high = max(data["High"])
        away_from_low = round(((current_price / duration_low) - 1) * 100, 2)
        away_from_high = round(100 - (current_price * 100 / duration_high), 2)
        avg_diliverables = sum(data["%Deliverble"])/len(data["%Deliverble"])
        stock_dict = {'stock' : stock_symbol, 
                    'current_price' : current_price, 
                    'away_from_low' : away_from_low, 
                    'away_from_high' : away_from_high,
                    'avg_deliverables' : avg_diliverables}
        printProgressBar(i + 1, length_stocks, prefix = 'Progress:', suffix = 'Complete', length = 50)
        stocks_info.append(stock_dict)
    sorted_stocks = sorted(stocks_info, key = lambda i : i['away_from_high'], reverse=True)
    df = pd.DataFrame(sorted_stocks)
    pd.set_option('display.max_rows', df.shape[0]+1)
    print(df)

if __name__ == '__main__':
    if len(argv) == 2:
        print_stocks(argv[1])
    else:
        print_stocks()
