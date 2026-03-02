from db_mongo.banco_mongo import Banco_Mongo
import datetime
from typing import Dict, List
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoAlertPresentException,
    NoSuchElementException,
    ElementNotInteractableException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webdriver import WebDriver
from re import findall
from os import getenv, path, remove, getcwd
from bson import ObjectId


def rodar_js(self: WebDriver, js: str) -> any:
    """
    Adiciona um helper ao WebDriver para executar JavaScript.
    Uso: driver.rodar_js(\"alert('oi')\")
    """
    return self.execute_script(js)


WebDriver.rodar_js = rodar_js


class Padrao:

    def __init__(self) -> None:
        self.banco = Banco_Mongo()

