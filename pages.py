# -*- coding: utf-8 -*-
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from base import Base
from locators import *


class WidgetsMain(Base):

    """ Page object class for Portal login page """

    def login_with_user_jwt(self, jwt, host):
        self.click_button(WidgetsMainLocators.EXPRESS_AUTH_BTN, *WidgetsMainLocators.LOGIN_POPUP_BTN)
        self.click_button(WidgetsMainLocators.JWT_FILED, *WidgetsMainLocators.EXPRESS_AUTH_BTN)
        self.find_element(*WidgetsMainLocators.JWT_FILED).send_keys(jwt)
        self.find_element(*WidgetsMainLocators.HOST_FILED).send_keys(host)
        self.click_button(WidgetsPrefcenterLocators.MY_PERMISSIONS, *WidgetsMainLocators.SAVE_BTN)


class WidgetsPrefcenter(Base):

    def open_my_permissions(self):
        self.click_button(WidgetsPrefcenterLocators.PERMISSINS_TABLE, *WidgetsPrefcenterLocators.MY_PERMISSIONS)

    def count_rows(self, locator):
        rows = self.driver.find_elements(locator)
        return len(rows) - 1

    def switch_on_consents(self, wait, *button_locator):
        self.click_button(wait, *button_locator)
