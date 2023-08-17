"""
Корневой класс AppiumExtended. Обеспечивает соединение с сервером и инициализацию драйвера.
"""

# coding: utf-8
import logging
import json
import time

from appium import webdriver

from appium_extended_helpers.appium_helpers import AppiumHelpers
from appium_extended_server.appium_server import AppiumServer
from appium_extended_terminal.terminal import Terminal
from appium_extended_terminal.aapt import Aapt
from appium_extended_terminal.adb import Adb


class AppiumBase:
    """
    Класс работы с Appium.
    Обеспечивает подключение к устройству
    """

    def __init__(self, logger: logging.Logger = None):
        self.server_log_level = None
        self.server_port = None
        self.server_ip = None
        self.server = None
        self.logger = logger
        self.driver = None
        self.terminal = None
        self.session_id = None
        self.helper: AppiumHelpers = None
        self.keep_alive_server = True
        self.aapt = Aapt()
        self.adb = Adb()

        aapt_logger = logging.getLogger('aapt')
        aapt_logger.setLevel(self.logger.level)
        adb_logger = logging.getLogger('adb')
        adb_logger.setLevel(self.logger.level)

    def connect(self,
                capabilities: dict,
                server_ip: str = '127.0.0.1',
                server_port: int = 4723,
                server_log_level: str = 'error',
                remote: bool = False,
                keep_alive_server: bool = True) -> None:
        """
        Подключение к устройству
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_log_level = server_log_level
        self.keep_alive_server = keep_alive_server
        self.server = AppiumServer(server_ip=self.server_ip,
                                   server_port=self.server_port,
                                   remote_log_level=self.server_log_level,
                                   logger=self.logger)
        self.logger.debug(
            f"connect(capabilities {capabilities}")
        if not remote:
            # запускаем локальный сервер Аппиум
            if not self.server.is_alive():
                self.server.start()
                time.sleep(10)
                self.server.wait_until_alive()

        url = f'http://{server_ip}:{str(server_port)}/wd/hub'
        self.logger.info(f"Подключение к серверу: {url}")
        self.driver = webdriver.Remote(command_executor=url,
                                       desired_capabilities=capabilities,
                                       keep_alive=True)
        self.session_id = self.driver.session_id
        # Инициализация объектов требующих драйвер
        self.terminal = Terminal(driver=self.driver, logger=self.logger)
        self.helper = AppiumHelpers(driver=self.driver, logger=self.logger)

        app_capabilities = json.dumps(capabilities)
        self.logger.info(f'Подключение установлено с  параметрами: {str(app_capabilities)}, {url}')
        self.logger.info(f'Сессия №: {self.driver.session_id}')

    def disconnect(self) -> None:
        """
        Отключение от устройства
        """
        if self.driver:
            self.logger.debug(f"Отключение от сессии №: {self.driver.session_id}")
            self.driver.quit()
            self.driver = None
        if not self.keep_alive_server:
            self.server.stop()

    def is_running(self) -> bool:
        """
        Проверяет, запущен сервер или нет
        """
        return self.driver.is_running()
