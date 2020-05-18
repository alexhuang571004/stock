import re

"""
isnumeric can not check number correctly.
Use this function to cehck number correctly

"""
def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False
"""
read stock list

"""
def get_setting():   # 取得 stock.txt 中的股票設定資訊
    try:
        with open('stock.txt') as stock_file:  #←以讀取模式開啟檔案
            slist = stock_file.readlines()     #←以行為單位讀取所有資料

            stock_list = []
            for lst in slist:
                stock_info = lst.split(',')
                if float(stock_info[1]):
                #stock_info: stock_id, price_low, price_high
                    stock_list.append([stock_info[0], float(stock_info[1]), float(stock_info[2])])
                else:
                    break
    except:
        print('stock.txt 讀取錯誤')
        return None
    return stock_list

