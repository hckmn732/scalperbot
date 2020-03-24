
import threading
import pandas as pd
import numpy as np
from datetime import datetime

import requests as requests

import threading

url = "https://api.telegram.org/bot1098470015:AAHKCX26B2LG_MRo76It1Jx0l913c9_4RBk/"


# create func that get chat id
def get_chat_id(update):
    chat_id = update['message']["chat"]["id"]
    return chat_id


# create function that get message text
def get_message_text(update):
    message_text = update["message"]["text"]
    return message_text


# create function that get last_update
def last_update(req):
    response = requests.get(req + "getUpdates")
    response = response.json()
    result = response["result"]
    total_updates = len(result) - 1
    return result[total_updates]  # get last record message update


# create function that let bot send message to user
def send_message(chat_id, message_text):
    params = {"chat_id": chat_id, "text": message_text}
    response = requests.post(url + "sendMessage", data=params)
    return response


# create main function for navigate or reply message back
def notification():
    update_id = last_update(url)["update_id"]
    while True:
        update = last_update(url)
        if update_id == update["update_id"]:
            if get_message_text(update).lower() == "/open_orders" :
                send_message(get_chat_id(update), "Orders ready")
            else:
                send_message(get_chat_id(update), "Sorry Not Understand what you inputted:( I love you")
            update_id += 1



def FetchData(symbol,binSize,count):
  
  url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize="+binSize+"&partial=false&symbol="+symbol+"&count="+count+"&reverse=true"

  response = requests.get(url)
  response = response.json()

  date = []
  open = []
  high = []
  low = []
  close = []
  trades = []

  for i in range(int(count)-1,-1,-1) :
      time_data = response[i]["timestamp"]
      time_data = datetime.strptime(time_data, '%Y-%m-%dT%H:%M:%S.%fZ')
      time_data = str(time_data.year)+"-"+str(time_data.month)+"-"+str(time_data.day)+" "+str(time_data.hour)+":"+str(time_data.minute)+":"+str(time_data.second)    
      date.append(time_data) 

      open.append(response[i]["open"])
      high.append(response[i]["high"])
      low.append(response[i]["low"])
      close.append(response[i]["close"])
      trades.append(response[i]["trades"])


  data_set = {'Date': date,
          'Open': open,
          'High': high,
          'Low': low,
          'Close': close,
          'Trades': trades
          }
  
  return pd.DataFrame(data_set, columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Trades'])

def computeRSI (data, time_window):
    diff = data.diff(1).dropna()     
    up_chg = 0 * diff
    down_chg = 0 * diff
    up_chg[diff > 0] = diff[ diff>0 ]
    down_chg[diff < 0] = diff[ diff < 0 ]
    
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi

def moving_average(data, n=9):
    sma = data.rolling(window=n).mean()
    return sma

def init_data():
    threading.Timer(5.0, init_data).start()
    df = FetchData("ETHUSD","5m","100")
    df['RSI'] = computeRSI(df['Close'], 14)
    #df['MA'] = moving_average(df['Close'],9)
    #df['EMASLOW'] = df['Close'].ewm(span=26).mean()
    #df['EMAFAST'] = df['Close'].ewm(span=12).mean()
    #df['MACD'] = df['EMAFAST'] - df['EMASLOW']
    #df['SIGNAL_LINE'] = df['MACD'].ewm(span=9).mean()

#t = threading.Thread(target = init_data,name="RSI")
#t.start()

#t = threading.Thread(target = notification,name="Notifcation")
#t.start()
notification