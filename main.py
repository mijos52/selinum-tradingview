from  selenium import  webdriver 
import json
from websocket import create_connection
from datetime import datetime
import csv
import time
import random
import string
import re
import config

# credentials
username = config.USER_NAME
password = config.PASSWORD

# variables
website = 'https://www.tradingview.com/accounts/signin/ '
websocket_url ='wss://data.tradingview.com/socket.io/websocket?from=chart/s79Lxi3Z/&date=2022_05_16-11_37'

def filter_raw_message(text):
    try:
        found = re.search('"m":"(.+?)",', text).group(1)
        found2 = re.search('"p":(.+?"}"])}', text).group(1)
        print(found)
        print(found2)
        return found, found2
    except AttributeError:
        print("error")
    

def generateSession():

    letters = string.ascii_lowercase
    random_string= ''.join(random.choice(letters) for i in range(12))
    return "qs_" +random_string

def generateChartSession():

    letters = string.ascii_lowercase
    random_string= ''.join(random.choice(letters) for i in range(12))
    return "cs_" +random_string

# creates a string of ex ~m~3~m~hai
def prependHeader(st):
    return "~m~" + str(len(st)) + "~m~" + st

def constructMessage(func, paramList):
    return json.dumps({
        "m":func,
        "p":paramList
        }, separators=(',', ':'))

def createMessage(func, paramList):
    return prependHeader(constructMessage(func, paramList))

def sendRawMessage(ws, message):
    ws.send(prependHeader(message))

def sendMessage(ws, func, args):
    ws.send(createMessage(func, args))

def generate_csv(a):
    out= re.search('"s":\[(.+?)\}\]', a).group(1)
    x=out.split(',{\"')
    
    with open('data_file.csv', mode='w', newline='') as data_file:
        employee_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        employee_writer.writerow(['index', 'date', 'open', 'high', 'low', 'close', 'volume'])
        
        for xi in x:
            xi= re.split('\[|:|,|\]', xi)
            print(xi)
            ind= int(xi[1])
            ts= datetime.fromtimestamp(float(xi[4])).strftime("%Y/%m/%d, %H:%M:%S")
            employee_writer.writerow([ind, ts, float(xi[5]), float(xi[6]), float(xi[7]), float(xi[8]), float(xi[9])])


driver = webdriver.Chrome()
driver.get(website)

# TODO https://www.tradingview.com/accounts/signin/ 

# click signin by email 
embutton = driver.find_element_by_class_name("tv-signin-dialog__toggle-email")
embutton.click()

# input user name and password in the text fields
username_input = driver.find_element_by_name("username")
username_input.send_keys(username)
password_input = driver.find_element_by_name("password")
password_input.send_keys(password)

# submit username and password
submit_button = driver.find_element_by_class_name("tv-button__loader")
submit_button.click()

time.sleep(5)

driver.get('https://in.tradingview.com/chart/s79Lxi3Z/?symbol=NSE%3ANIFTY')
''' loads the nifty page for this account wont work on other accounts a url is directly loaded 
instead of clicking anything for else '''

headers = json.dumps({
    'Origin': 'https://data.tradingview.com'
})

ws = create_connection(
    'wss://data.tradingview.com/socket.io/websocket',headers=headers)


session= generateSession()
print("session generated {}".format(session))

chart_session= generateChartSession()
print("chart_session generated {}".format(chart_session))

# Then send a message through the tunnel 
sendMessage(ws, "set_auth_token", ["unauthorized_user_token"])
sendMessage(ws, "chart_create_session", [chart_session, ""])
sendMessage(ws, "quote_create_session", [session])
sendMessage(ws,"quote_set_fields", [session,"ch","chp","current_session","description","local_description","language","exchange","fractional","is_tradable","lp","lp_time","minmov","minmove2","original_name","pricescale","pro_name","short_name","type","update_mode","volume","currency_code","rchp","rtc"])
sendMessage(ws, "quote_add_symbols",[session, "BINANCE:BTCUSDT", {"flags":['force_permission']}])

sendMessage(ws, "resolve_symbol", [chart_session, "symbol_1","={\"symbol\":\"BINANCE:BTCUSDT\",\"adjustment\":\"splits\"}"])
sendMessage(ws, "create_series", [chart_session,"s1","s1","symbol_1","1",300])

sendMessage(ws, "quote_fast_symbols", [session,"BINANCE:BTCUSDT"])

sendMessage(ws, "quote_hibernate_all", [session])



# Printing all the result
a=""
while True:
    try:
        time.sleep(1)
        result = ws.recv()
        pattern = re.compile("~m~\d+~m~~h~\d+$") 
        if pattern.match(result):
            ws.recv()
            ws.send(result)
            print("\n\n\n hhhhhhhhhhhhhhhhhhhhhh "+ str(result) + "\n\n")
        print(result)
        a=a+result+"\n"
    except Exception as e:
        print(e)
        break
    
generate_csv(a)
