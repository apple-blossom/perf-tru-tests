# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class WidgetsMainLocators(object):

    """Locators for Widgets main"""

    @staticmethod
    def table_elements(row_number=2):
        locators = {
            "permissions_rows_btn_off": (By.CSS_SELECTOR, "div.panel-group>div.panel.panel-default:nth-of-type(1) "
                                         "tr:nth-of-type({}) .btn.toggle-off.btn-md.btn-default".format(row_number)),
            "permissions_rows_btn_on": (By.CSS_SELECTOR, "div.panel-group>div.panel.panel-default:nth-of-type(1) "
                                        "tr:nth-of-type({}) .btn.toggle-on.btn-md.btn-success".format(row_number)),
            "data_rows_dsr_open": ("div.panel-group>div.panel.panel-default:nth-of-type(2) "
                                   "tr:nth-of-type({}) #dropdown-size-medium".format(row_number)),
            "data_rows_dsr_menu": (By.CSS_SELECTOR, "div.panel-group>div.panel.panel-default:nth-of-type(2) "
                                   "tr:nth-of-type({}) .dropdown-menu".format(row_number)),
            "data_rows_access": (By.CSS_SELECTOR, "div.panel-group>div.panel.panel-default:nth-of-type(2) "
                                 "tr:nth-of-type({}) .dropdown-menu li:nth-of-type(1) a".format(row_number)),
            "data_rows_rectify": (By.CSS_SELECTOR, "div.panel-group>div.panel.panel-default:nth-of-type(2) "
                                  "tr:nth-of-type({}) .dropdown-menu li:nth-of-type(2) a".format(row_number)),
            "data_rows_erase": (By.CSS_SELECTOR, "div.panel-group>div.panel.panel-default:nth-of-type(2) "
                                "tr:nth-of-type({}) .dropdown-menu li:nth-of-type(3) a".format(row_number)),
        }
        return locators

    LOGIN_POPUP_BTN = (By.CSS_SELECTOR, "p .black-background.white.btn.btn-lg.btn-default")
    EXPRESS_AUTH_BTN = (By.CSS_SELECTOR, "div .radio-inline:last-of-type")
    JWT_FILED = (By.CSS_SELECTOR, "#jwtToken")
    HOST_FILED = (By.ID, "host_addr")
    SAVE_BTN = (By.CSS_SELECTOR, ".btn.btn-success")


class WidgetsPrefcenterLocators(object):
    MY_PERMISSIONS = (By.CSS_SELECTOR, ".panel.panel-default:nth-of-type(1) a.collapsed")
    PERMISSIONS_TABLE = (By.CSS_SELECTOR, ".panel-body")
    DATA_TABLE = (By.CSS_SELECTOR, ".panel.panel-default")
    PERMISSIONS_TABLE_ROWS = (By.CSS_SELECTOR, "div.panel-group>div.panel.panel-default:nth-of-type(1) tr")
    DATA_TABLE_ROWS = (By.CSS_SELECTOR, "div.panel-group>div.panel.panel-default:nth-of-type(2) tr")
    ACCESS = (By.XPATH, "//*[contains(text(),'Access')]")
    RECTIFY = (By.XPATH, "//*[contains(text(),'Rectify')]")
    ERASE = (By.XPATH, "//*[contains(text(),'Erase')]")
    MENU = (By.CSS_SELECTOR, ".dropdown-menu")
    SPINNER = (By.CSS_SELECTOR, ".icon-spin1.animate-spin.loadingIcon")
    MY_DATA = (By.CSS_SELECTOR, ".panel.panel-default:nth-of-type(2) a.collapsed")
    REASONS_POPUP = (By.CSS_SELECTOR, ".blueDiv.alert.alert-info")
    REASON_1 = (By.CSS_SELECTOR, "div:first-of-type>div.radio label")
    REASONS_SUBMIT = (By.CSS_SELECTOR, ".btn-block.btn.btn-default")
