# -*- coding: utf-8 -*-
import unittest
from locust import HttpLocust, TaskSet, task
from realbrowserlocusts import HeadlessChromeLocust

# from selenium import webdriver

from base import Base
from pages import *
from locators import *
from api_methods import ApiRequests


class TestWidgets(TaskSet, Base):

    def find_element(self, *locator):
        return self.client.find_element(*locator)

    def wait_page_to_load(self, locator, seconds=60):
        try:
            WebDriverWait(self.client, seconds).until((EC.visibility_of_element_located(locator)))
        except TimeoutException:
            self.screenshot("page_didnt_load")
            raise AssertionError("Page didn't load. Locator:", locator)

    def screenshot(self, name):
        name = "screenshot_{}.png".format(name)
        self.client.save_screenshot(name)

    def click_element_with_js(self, locator):
        code = "var btn=document.querySelectorAll('{}')[0]; btn.click();".format(locator)
        self.client.execute_script(code)

    def click_element(self, *locator):
        self.find_element(*locator).click()

    def click_button(self, wait_locator, *btn_locator):
        self.find_element(*btn_locator).click()
        try:
            WebDriverWait(self.client, 60).until((EC.visibility_of_element_located(wait_locator)))
        except TimeoutException:
            self.screenshot("wait_error")
            raise AssertionError("The next page did not opened. Locator:", wait_locator)

    def login_with_user_jwt(self, jwt, host):
        self.click_button(WidgetsMainLocators.EXPRESS_AUTH_BTN, *WidgetsMainLocators.LOGIN_POPUP_BTN)
        self.click_element_with_js(WidgetsMainLocators.EXPRESS_AUTH_BTN[1])
        self.wait_page_to_load(WidgetsMainLocators.JWT_FILED)
        code = "var f=document.querySelectorAll('{}')[0]; f.value+='{}';".format(WidgetsMainLocators.JWT_FILED[1], jwt)
        self.client.execute_script(code)
        self.find_element(*WidgetsMainLocators.HOST_FILED).send_keys(host)
        # self.click_button(WidgetsPrefcenterLocators.MY_PERMISSIONS, *WidgetsMainLocators.SAVE_BTN)
        self.click_element_with_js(WidgetsMainLocators.SAVE_BTN[1])
        self.wait_page_to_load(WidgetsPrefcenterLocators.MY_PERMISSIONS)

    def open_table(self, locator):
        self.click_element_with_js(locator)
        try:
            WebDriverWait(self.client, 60).until((EC.invisibility_of_element_located(
                WidgetsPrefcenterLocators.SPINNER)))
        except TimeoutException:
            self.screenshot("table1_didnt_load")
            raise AssertionError("Table didn't open")

    def count_rows(self, *locator):
        rows = self.client.find_elements(*locator)
        # for row in rows:
        #     print(row.text, "\n")
        rows = len(rows) - 1
        return rows

    def switch_on_consents(self, button_locator):
        self.click_element_with_js(button_locator)
        try:
            WebDriverWait(self.client, 60).until((EC.invisibility_of_element_located(
                WidgetsPrefcenterLocators.SPINNER)))
        except TimeoutException:
            self.screenshot("button_didnt_load")
            raise AssertionError("Button didnt switch:", button_locator)

    def apply_dsr(self, dsr_locator, *menu_locator):
        self.screenshot("1")
        self.click_button(WidgetsPrefcenterLocators.MENU, *menu_locator)
        self.screenshot("2")
        self.click_element_with_js(dsr_locator)
        self.screenshot("3")
        self.wait_page_to_load(WidgetsPrefcenterLocators.REASON_1)
        self.screenshot("4")
        self.click_element(*WidgetsPrefcenterLocators.REASON_1)
        self.click_element(*WidgetsPrefcenterLocators.REASONS_SUBMIT)
        try:
            WebDriverWait(self.client, 60).until((EC.invisibility_of_element_located(
                WidgetsPrefcenterLocators.REASONS_POPUP)))
        except TimeoutException:
            self.screenshot("popup_didnt_close")
            raise AssertionError("Popup didn't close")

    def test_widgets_consents(self):
        """ Test for widgets"""
        data = self.open_data_json()
        # url = data["widgets"]
        jwt = ApiRequests().create_jwt_for_user(data["user"], data["enterprise_id"],
                                                data["path_to_key"])
        self.client.get('https://test.trunomi.com/preview/prefcentre')
        self.login_with_user_jwt(jwt, data["host_address"])
        self.open_table(WidgetsPrefcenterLocators.MY_PERMISSIONS[1])
        rows = self.count_rows(*WidgetsPrefcenterLocators.PERMISSIONS_TABLE_ROWS)
        for row in range(2, rows):
            self.switch_on_consents(WidgetsMainLocators.table_elements(row)["permissions_rows_btn_off"][1])

    def test_widgets_data(self):
        """ Test for widgets"""
        data = self.open_data_json()
        # url = data["widgets"]
        jwt = ApiRequests().create_jwt_for_user(data["user"], data["enterprise_id"],
                                                data["path_to_key"])
        self.client.get("https://test.trunomi.com/preview/prefcentre")
        self.login_with_user_jwt(jwt, data["host_address"])
        self.open_table(WidgetsPrefcenterLocators.MY_DATA[1])
        rows = self.count_rows(*WidgetsPrefcenterLocators.DATA_TABLE_ROWS)
        for row in range(2, rows):
            dsr_locator = WidgetsMainLocators.table_elements(row)["data_rows_dsr_open"]
            self.apply_dsr(dsr_locator, *WidgetsMainLocators.table_elements(row)["data_rows_dsr_menu"])

    @task(1)
    def my_data(self):
        self.client.timed_event_for_locust("my_data", "", self.test_widgets_data)

    @task(1)
    def consents(self):
        self.client.timed_event_for_locust("consents", "", self.test_widgets_consents)


class MyLocust(HeadlessChromeLocust):
    task_set = TestWidgets
    timeout = 30  # in seconds in waitUntil thingies
    min_wait = 100
    max_wait = 1000
    screen_width = 1200
    screen_height = 600
