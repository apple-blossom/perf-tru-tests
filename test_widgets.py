# -*- coding: utf-8 -*-
import unittest
# import time
# from ddt import ddt, file_data, data


# from selenium import webdriver

from base import Base
from pages import *
from locators import *
from api_methods import ApiRequests


class TestWidgets(unittest.TestCase, Base):

    """ Tests for Widgets click DSRs and Consents """

    def setUp(self):
        super().setUp()
        self.driver = self.setup_with_headless()
        # self.driver = webdriver.Chrome()
        self.api = ApiRequests()
        self.main = WidgetsMain(self.driver)
        self.pref = WidgetsPrefcenter(self.driver)
        self.data = self.open_data_json()
        url = self.data["widgets"]
        self.verify_server_available(url)
        self.jwt = self.api.create_jwt_for_user(self.data["user"], self.data["enterprise_id"],
                                                self.data["path_to_key"])
        self.locators = WidgetsMainLocators.table_elements()
        self.driver.get(url)

    def tearDown(self):
        self.driver.quit()

    def test_widgets_consents(self):
        """ Test for widgets"""
        self.main.login_with_user_jwt(self.jwt, self.data["host_address"])
        self.pref.open_table(WidgetsPrefcenterLocators.MY_PERMISSIONS[1])
        rows = self.pref.count_rows(*WidgetsPrefcenterLocators.PERMISSIONS_TABLE_ROWS)
        for row in range(2, rows):
            self.pref.switch_on_consents(WidgetsMainLocators.table_elements(row)["permissions_rows_btn_off"][1])

    def test_widgets_data(self):
        """ Test for widgets"""
        self.main.login_with_user_jwt(self.jwt, self.data["host_address"])
        self.pref.open_table(WidgetsPrefcenterLocators.MY_DATA[1])
        rows = self.pref.count_rows(*WidgetsPrefcenterLocators.DATA_TABLE_ROWS)
        print(rows)
        for row in range(2, rows):
            self.pref.apply_dsr(WidgetsMainLocators.table_elements(row)["data_rows_dsr_menu"],
                                *WidgetsMainLocators.table_elements(row)["data_rows_dsr_open"])
