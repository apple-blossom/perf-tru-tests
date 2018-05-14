# -*- coding: utf-8 -*-
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from base import Base
from locators import *


class WidgetsMain(Base):

    """ Page object class for Portal login page """

    def login_with_user_jwt(self, jwt, host):
        self.click_button(WidgetsMainLocators.EXPRESS_AUTH_BTN, *WidgetsMainLocators.LOGIN_POPUP_BTN)
        self.click_element_with_js(WidgetsMainLocators.EXPRESS_AUTH_BTN[1])
        self.wait_page_to_load(WidgetsMainLocators.JWT_FILED)
        code = "var f=document.querySelectorAll('{}')[0]; f.value+='{}';".format(WidgetsMainLocators.JWT_FILED[1], jwt)
        self.driver.execute_script(code)
        self.find_element(*WidgetsMainLocators.HOST_FILED).send_keys(host)
        self.click_button(WidgetsPrefcenterLocators.MY_PERMISSIONS, *WidgetsMainLocators.SAVE_BTN)


class WidgetsPrefcenter(Base):

    def open_table(self, locator):
        self.click_element_with_js(locator)
        try:
            WebDriverWait(self.driver, 60).until((EC.invisibility_of_element_located(
                WidgetsPrefcenterLocators.SPINNER)))
        except TimeoutException:
            self.screenshot("table1_didnt_load")
            raise AssertionError("Table didn't open")

    def count_rows(self, *locator):
        rows = self.driver.find_elements(*locator)
        for row in rows:
            print(row.text, "\n")
        rows = len(rows) - 1
        return rows

    def switch_on_consents(self, button_locator):
        self.click_element_with_js(button_locator)
        try:
            WebDriverWait(self.driver, 60).until((EC.invisibility_of_element_located(
                WidgetsPrefcenterLocators.SPINNER)))
        except TimeoutException:
            self.screenshot("button_didnt_load")
            raise AssertionError("Button didnt switch:", button_locator)

    def apply_dsr(self, dsr_locator, *menu_locator):
        self.click_button(dsr_locator, *menu_locator)
        self.click_button(WidgetsPrefcenterLocators.REASON_1, *dsr_locator)
        self.click_element(*WidgetsPrefcenterLocators.REASON_1)
        self.click_element(*WidgetsPrefcenterLocators.REASONS_SUBMIT)
        try:
            WebDriverWait(self.driver, 60).until((EC.invisibility_of_element_located(
                WidgetsPrefcenterLocators.REASONS_POPUP)))
        except TimeoutException:
            self.screenshot("popup_didnt_close")
            raise AssertionError("Popup didn't close")
