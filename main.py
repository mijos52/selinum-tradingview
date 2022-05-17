# will have the main class and functions to sort data from tradinvgview

from  selenium import  webdriver
import websocket , json
import time
from config import *

# credentials
username = USER_NAME
password = PASSWORD

# variables
website = 'https://www.tradingview.com/accounts/signin/ '
websocket_url ='wss://data.tradingview.com/socket.io/websocket?from=chart/s79Lxi3Z/&date=2022_05_16-11_37'

# functions to handle websocket data message , error , close
def on_message(ws , message):
    print(message)

def on_close(ws):
    print("closed connection")

def on_error(ws , error):
    print(error)

def on_open(ws):
    print('connection open ')


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

# initialize websocket using websocket client

ws = websocket.WebSocketApp(websocket_url,
on_message=on_message , on_close=on_close , on_error=on_error)

ws.on_open = on_open
ws.run_forever()