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

        # Extracting the table headers

        if len(cols) == 0:
            cols = row.find_all('th')

        cols = [ele.text.strip() for ele in cols]

        data.append([ele for ele in cols if ele])  # Get rid of empty values

    df = pd.DataFrame(data)
    df = df[[0, 5]].iloc[1:-1, :]
    df.to_csv(r' data.csv', header=False, index=False)
    print(df)

    # table = soup.find('div', class_=('customTable-width deque-table-sortable-group')).find('table').find_all('tr')
    # for tr in table:
    #     find_name_symbol = tr.find_all('a', class_='symbol-word-break')
    #     # find_final_price = tr.find('td', class_='bold text-right').get_text()
    #
    #     for i in find_name_symbol:
    #         name_symbol = i.text.replace('\n', '')
    #         data = {'names': name_symbol}
    #
    #     find_final_price = tr.find_all('td', class_='bold text-right')
    #     for i in find_final_price:
    #         final_price = i.text
    #         data = {'final_prices': final_price}
    #     write_csv(data)

    driver.quit()


def write_csv(data):
    with open('data.csv', 'a') as f:
        recorder = csv.writer(f)
        recorder.writerow((data['names'],
                           data['final_prices']))
        # for elem in data:
        #     recorder.writerow((elem, data[elem]))


if __name__ == '__main__':
    get_data()
