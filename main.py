import csv
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.proxy import Proxy, ProxyType


def get_data():
    profile = webdriver.FirefoxProfile()

    profile.accept_untrusted_certs = True

    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': "11.456.448.110:8080",
        'noProxy': ''
    })
    driver_options = webdriver.FirefoxOptions()
    driver_options.add_argument('--proxy-server=%s' % proxy)
    driver_options.add_argument('--firefox-profile=%s' % profile)
    driver = webdriver.Firefox(driver_options)

    driver.get("https://www.nseindia.com")

    hover_element = driver.find_element(By.ID, "link_2")
    actions = ActionChains(driver).move_to_element(hover_element)
    actions.perform()
    actions.click()
    time.sleep(4)
    pre_open_market = driver.find_element(By.LINK_TEXT, "Pre-Open Market")
    time.sleep(3)
    driver.delete_all_cookies()
    pre_open_market.click()
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find('table')
    data = []
    for row in table.find_all('tr'):

        cols = row.find_all('td')

        if len(cols) == 0:
            cols = row.find_all('th')

        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    df = pd.DataFrame(data)
    df = df[[0, 5]].iloc[1:-1, :]
    df.to_csv(r' data.csv', header=False, index=False)
    print(df)

if __name__ == '__main__':
    get_data()
