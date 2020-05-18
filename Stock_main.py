import time                # 匯入 time 模組, 會使用其 sleep() 來暫停時間
import twstock
import sys
#import re
import Stock_ifttt_action as ifttt
import stock_read_file as fileact

#const_stock_num = '2330'
check_min = 10              # check every 10 min
check_period = check_min*60 # count by sec
check_cnt = 120/check_min    # execute 1 hour

"""
get stock realtime information

"""
def get_price(stockid):   # 取得股票名稱和及時股價
    rt = twstock.realtime.get(stockid)   # 取得台積電的及時交易資訊

    if rt['success']:                    # 如果讀取成功
        if fileact.is_number(rt['realtime']['latest_trade_price']):
            return (rt['info']['name'],                         #傳回 (股票名稱)
                    float(rt['realtime']['latest_trade_price']))#傳回 (及時價格)
        else:
            return (rt['info']['name'], False)                  #傳回 (股票名稱, 無及時價格)
    else:
        return (False, False)
"""
check suggestion

"""
def get_best(stockid):     # 檢查是否符合四大買賣點
    stock = twstock.Stock(stockid)
    bp = twstock.BestFourPoint(stock).best_four_point()
    if(bp):
        return ('買進' if bp[0] else '賣出', bp[1])  #←傳回買進或賣出的建議
    else:
        return (False, False)  #←都不符合

"""
main 
"""
stock_list = fileact.get_setting()   # 呼叫匯入模組中的函式取得股票設定資料
if stock_list:
    stock_num = len(stock_list)          # 計算有幾支股票
else:
    print('read file failed')
    sys.exit()

log1 = []   # 記錄曾經傳送過的股票高或低於期望價的訊息, 以避免重複傳送
log2 = []   # 記錄曾經傳送過符合四大買賣點的訊息, 以避免重複傳送
for i in range(stock_num):   #}
    log1.append('')    #} 為每支股票加入一個對應的元素
    log2.append('')    #}

while True:
    for i in range(stock_num):   # 走訪每一支股票
        id, buy_price, volume = stock_list[i]   #讀出股票的代號、期望買進價格、期望賣出
        name, price = get_price(id)   #讀取股票的名稱和即時價格
        
        print('檢查：',name, '買進股價：',buy_price, '共',volume,'現價:',price)
        """
        if price <= low:      #←如果即時股價到達期望買點
            if log1[i] != '買進':  # 檢查前次傳送訊息, 以避免重複傳送
                ifttt.send_ifttt(name, price, '買進 (股價低於 '+str(low)+')')
                log1[i]= '買進'    # 記錄傳送訊息, 以避免重複傳送
        elif price >= high:   #←如果即時股價到達期望賣點
            if log1[i] != '賣出':  # 檢查前次傳送訊息, 以避免重複傳送
                ifttt.send_ifttt(name, price, '賣出 (股價高於 '+str(high)+')')
                log1[i]= '賣出'    # 記錄傳送訊息, 以避免重複傳送
        """
        act, why = get_best(id)  # 檢查四大買賣點
        if why:   #←如果符合四大買賣點
            if log2[i] != why:    # 檢查前次傳送訊息, 以避免重複傳送
                iftttVal0 = name + str(buy_price)
                ifttt_result = ifttt.send_ifttt(iftttVal0, price, act + ' (' +why+ ')')
                log2[i] = why     # 記錄傳送訊息, 以避免重複傳送
                #print(ifttt_result)
                time.sleep(10)  #避免頻繁發送
    print('--------------')
    check_cnt -= 1             # 將計數器減 1
    if check_cnt == 0: break   # 檢查計數器為 0 時即離開迴圈、結束程式
    time.sleep(check_period)   # 每 check_min 分鐘 檢查一遍
#end of while
"""
name, price = get_price(const_stock_num)  #←用 name 及 price 來承接傳回的 tuple
act, why = get_best(const_stock_num)      #←用 act 及 why 來承接傳回的四大買賣點 tuple
ret = ifttt.send_ifttt(name, price, act + why)  #傳送 HTTP 請求到 IFTTT
print('IFTTT 的回應訊息：', ret)     # 輸出 IFTTT 回應的文字
"""