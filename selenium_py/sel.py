from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
options = Options() #Chrome Options

# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("user-data-dir=selenium")
# options.add_argument(r'--user-data-dir = /Users/tianhaoyao/Desktop/') #Extract this path from "chrome://version/"
# options.add_argument(r'--profile-directory=udata')

# exec_path_chrome = "path/to/Google Chrome" 
# Start Chrome Driver
# chromedriver = '/Users/tianhaoyao/Desktop/chromedriver'

driver = None

def get_fee():
    res = requests.get("https://mempool.space/api/v1/fees/recommended")
    return int(res.json()["fastestFee"])

def init():
    global driver
    driver = webdriver.Chrome(options = options)
    driver.get("https://unisat.io")
    driver.get("https://github.com")
    driver.back()

    for i in range(1, 10001):
        button = driver.find_element(by=By.XPATH, value=f"(//div)[{i}]")
        if button.text == "Connect":
            button.click()
            sleep(2)
            break

    for i in range(80, 1001):
        button = driver.find_element(by=By.XPATH, value=f"(//div)[{i}]")
        if button.text == "UniSat Wallet":
            button.click()
            sleep(2)
            break

    driver.switch_to.window(driver.window_handles[-1])

    num = 1
    button = driver.find_element(by=By.XPATH, value=f"(//input)[{num}]")
    button.send_keys('12345')

    for i in range(1, 5001):
        button = driver.find_element(by=By.XPATH, value=f"(//div)[{i}]")
        if button.text == "Unlock":
            button.click()
            sleep(1)
            break

    driver.switch_to.window(driver.window_handles[-1])
    for i in range(1, 5001):
        button = driver.find_element(by=By.XPATH, value=f"(//div)[{i}]")
        if button.text == "Sign":
            button.click()
            sleep(1)
            break   

    driver.switch_to.window(driver.window_handles[-1])
# driver.get("https://unisat.io/inscription/28d645ea6c4294068c27fb565b151d91a17dadeab55e92ddfc61af323708ad6bi0")

def switch_network(network="testnet"):
    global driver
    driver.execute_script(f'window.unisat.switchNetwork("{network}")')
    driver.switch_to.new_window()
    print(driver.window_handles)
    print(driver.current_window_handle)
    sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    print(driver.window_handles)
    print(driver.current_window_handle)
    driver.switch_to.window(driver.window_handles[-1])
    for i in range(1, 5001):
        button = driver.find_element(by=By.XPATH, value=f"(//div)[{i}]")
        if button.text == "Switch Network":
            button.click()
            sleep(1)
            break   
    account = driver.execute_script('return (await window.unisat.getAccounts())')[0]
    print(account)


def buy(tick):
    global driver
    if driver is not None: driver.quit()
    init()
    # switch_network("mainnet")

    driver.get(f"https://unisat.io/market/brc20?tick={tick}")
    sleep(3)

    buy_button = driver.find_element(by=By.CLASS_NAME, value="market-buy-btn")
    buy_button.click()
    sleep(3)

    buttons = driver.find_elements(by=By.CLASS_NAME, value="border-btn")
    for button in buttons: 
        if (button.text == "Customize"):
            button.click()
            sleep(2)
            break

    for i in range(1, 5001):
        button = driver.find_element(by=By.XPATH, value=f"(//div)[{i}]")
        if button.text == "Custom":
            button.click()
            sleep(2)
            break  

    input = driver.find_element(by=By.CLASS_NAME, value="ant-input-number-input")
    for i in range(10): input.send_keys(Keys.BACK_SPACE)
    input.send_keys('20')
    sleep(2)

    close_button = driver.find_elements(by=By.CLASS_NAME, value="close")[-1]
    close_button.click()
    sleep(2)

    for button in driver.find_elements(by=By.CLASS_NAME, value="border-btn"):
        sleep(5)
        if (button.text == "Cancel"): button.click()

# unlock = driver.find_element(by=By.XPATH, value=f"(//div)[0]")
# password_input.send_keys('12345')
# while True:
#     sleep(5)
# Open the URL you want to execute JS

# Execute JS
# while True:
#     r = input()
#     print(r)
#     if (r == "1"):
#         URL = "https://unisat.io"
#         driver.get(URL)
#         driver.execute_script("window.unisat")
#         # driver.execute_script("console.log(window.unisat.getAccounts())")
#         # driver.execute_script("console.log(window.unisat.getBalance())")
# for i in range(1, 101):
#     button = driver.find_element(by=By.XPATH, value=f"(//div)[{i}]")
#     if button.text == "Sign & Pay":
#         print(i)
#         print(button.text)
#         button.click()
#         break
#         f'(//div)[{i}]'
#         find_element(by=By.XPATH, value="(//div)[1]")
def main():
    buy("ordi")
    return
    init()
    switch_network()

if __name__ == "__main__":
    main()