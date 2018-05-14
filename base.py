# -*- coding: utf-8 -*-
import json
import time
import random
import requests
import datetime
import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Base(object):

    """ Basic class for pages """

    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def random_user_id():
        user = str(random.randint(1000, 9999))
        return user

    def copy_all_file_text(self, path):
        with open(path, 'r') as f:
            data = f.read()
        return data

    def verify_server_available(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            AssertionError("\x1b[31m Server unavailable \x1b[0m", response.status_code)

    def open_data_json(self):
        with open('./data.json', 'r') as f:
            file = json.load(f)
            data = dict(enterprise_id=file['ENTERPRISE_ID'], user=file['CUSTOMER_ID'],
                        host_address=file['HOST_ADDRESS'], path_to_key=file['PATH_TO_KEY'],
                        dt_ids=file['DATA_TYPE_IDS'], context_ids=file['CONTEXT_IDS'],
                        widgets=file['WIDGETS_URL'])
        return data

    def open_ids_json(self):
        with open('./ids.json', 'r') as f:
            file = json.load(f)
            for el in file:
                el = dict(el)
                yield el

    def setup_with_headless(self):
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": os.path.join(os.getcwd())}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--screen-size=1366x800')
        options.add_argument('window-size=1366x800')
        options.add_argument('start-maximized')
        des_cap = DesiredCapabilities.CHROME
        des_cap['loggingPrefs'] = {'browser': 'ALL'}
        driver = webdriver.Chrome(
            chrome_options=options, desired_capabilities=des_cap)
        return driver

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def get_url(self):
        return self.driver.current_url

    def wait_page_to_load(self, locator, seconds=60):
        try:
            WebDriverWait(self.driver, seconds).until((EC.visibility_of_element_located(locator)))
        except TimeoutException:
            self.screenshot("page_didnt_load")
            raise AssertionError("Page didn't load. Locator:", locator)

    def scroll_to(self, element, height='0'):
        code = "var btn = document.querySelectorAll('%s')[0]; var y = btn.offsetParent + %s; window.scrollTo(0,y);"
        script = code % (element, height)
        self.driver.execute_script(script)

    def screenshot(self, name):
        name = "screenshot_{}.png".format(name)
        self.driver.save_screenshot(name)

    def click_element_with_js(self, locator):
        code = "var btn=document.querySelectorAll('{}')[0]; btn.click();".format(locator)
        self.driver.execute_script(code)

    def click_element(self, *locator):
        self.find_element(*locator).click()

    def click_button(self, wait_locator, *btn_locator):
        self.find_element(*btn_locator).click()
        try:
            WebDriverWait(self.driver, 60).until((EC.visibility_of_element_located(wait_locator)))
        except TimeoutException:
            self.screenshot("wait_error")
            raise AssertionError("The next page did not opened. Locator:", wait_locator)

    def choose_item_from_dropdown(self, *elem):
        el = self.find_element(*elem)
        ActionChains(self.driver).click(el).send_keys(
            'a').key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).perform()
        time.sleep(0.5)
        ActionChains(self.driver).move_to_element(el).key_down(Keys.ARROW_DOWN).key_down(Keys.RETURN).perform()

    def get_element_text(self, *locator):
        return self.find_element(*locator).text

    def get_current_day_month_year(self):
        my_date = datetime.datetime.now()
        date = {"Day": my_date.strftime("%d"), "Month": my_date.strftime("%b"), "Year": my_date.strftime("%Y")}
        return date

    def verify_number_of_elements(self, expected_number, *locator):
        number_of_elements = len(self.driver.find_elements(*locator))
        if number_of_elements != expected_number:
            self.screenshot("verify_number_of_elements")
            raise AssertionError("Number of elements is wrong. Expected number:", expected_number,
                                 "Actual number:", number_of_elements, "locator: ", *locator)
