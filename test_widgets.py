# -*- coding: utf-8 -*-
import unittest
import os
import time

# from selenium import webdriver

from base import Base
from pages import *
from locators import *
from api_methods import ApiRequests


class TestPortalDataTypes(unittest.TestCase, Base):

    """ Tests for Portal contexts creation and modification """

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

    def test_widgets(self):
        """ Test for widgets"""
        self.main.login_with_user_jwt(self.jwt, self.data["host_address"])
        self.pref.open_my_permissions()
        rows = self.pref.count_rows(WidgetsPrefcenterLocators.PERMISSINS_TABLE_ROWS)
        for row in rows:
            self.pref.switch_on_consents(row)
