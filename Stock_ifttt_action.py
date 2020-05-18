import requests      # 匯入 requests 套件

"""
IFTTT reference 
https://maker.ifttt.com/trigger/toline/with/key/
    dzTssveGpT_tVxMuIXj0zjKrrutGbBSbBmxvACxSn8g?
    value1=%E5%8F%B0%E7%A9%8D%E9%9B%BB&
    value2=98.5&
    value3=%E8%B2%B7%E9%80%B2
"""
const_ifttt_key = 'dzTssveGpT_tVxMuIXj0zjKrrutGbBSbBmxvACxSn8g'

def send_ifttt(v1, v2, v3):   # 定義函式來向 IFTTT 發送 HTTP 要求
    url = ('https://maker.ifttt.com/trigger/toline/with/key/' +
          const_ifttt_key +
          '?value1='+str(v1) +
          '&value2='+str(v2) +
          '&value3='+str(v3))
    try:
        r = requests.get(url)      # 送出 HTTP GET 並取得網站的回應資料
        if r.text[:5] == 'Congr':  # 回應的文字若以 Congr 開頭就表示成功了
            print('已傳送 (' +str(v1)+', '+str(v2)+', '+str(v3)+ ') 到 Line')
        return r.text
    except:
        return "requests.get 失敗!"


