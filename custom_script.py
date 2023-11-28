import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType


def custom_script():

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
    time.sleep(10)

    hover_element = driver.find_element(By.ID, "link_2")
    actions = ActionChains(driver).move_to_element(hover_element)
    actions.perform()
    actions.click()
    time.sleep(4)

    equity_market = driver.find_element(By.LINK_TEXT, "Equity & SME Market")
    time.sleep(3)
    driver.delete_all_cookies()
    equity_market.click()
    time.sleep(8)

    sgb = driver.find_element(By.ID, "market-Svn-gold-bond")
    driver.delete_all_cookies()
    sgb.click()
    time.sleep(4)

    market_billion = driver.find_element(By.ID, "market-billion")
    market_billion.click()
    time.sleep(4)

    end_scroll_elem = driver.find_element(By.ID, "marketWatchSoverignGoldBondCmsNote")
    time.sleep(3)
    driver.execute_script("arguments[0].scrollIntoView();", end_scroll_elem)

    driver.close()


if __name__ == '__main__':
     custom_script()
