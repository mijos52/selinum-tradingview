# will have the main class and functions to sort data from tradinvgview

from  selenium import  webdriver
import time

# credentials
username = 'bobj53255@gmail.com'
password = 'jhskhe34654se98f74dfkj'

website = 'https://in.tradingview.com/'

driver = webdriver.Chrome()
driver.get(website)

# click the user button
driver.find_element_by_class_name("tv-header__user-menu-button").click()

# click sign in button
driver.find_element_by_class_name('label-4TFSfyGO').click()

# time delay for the code to work properly
time.sleep(5)

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