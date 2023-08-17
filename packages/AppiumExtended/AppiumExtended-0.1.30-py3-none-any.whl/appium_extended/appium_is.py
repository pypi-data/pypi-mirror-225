# coding: utf-8
import logging
from typing import Union, Dict, Tuple

from appium.webdriver import WebElement

from appium_extended.appium_get import AppiumGet


class AppiumIs(AppiumGet):
    """
    Класс расширяющий Appium.
    Обеспечивает ....
    """

    def __init__(self, logger: logging.Logger):
        super().__init__(logger=logger)

    def _is_element_within_screen(
            self,
            locator: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str],
            timeout: int = 10,
            contains: bool = True
    ) -> bool:
        """
        Метод проверяет, находится ли заданный элемент на видимом экране.

        Аргументы:
        - locator (Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str]):
            Локатор или элемент, который нужно проверить.
        - timeout (int): Время ожидания элемента. Значение по умолчанию: 10.
        - contains (bool): Допускает фрагмент текста.

        Возвращает:
        - bool: True, если элемент находится на экране, False, если нет.
        """
        screen_size = self.terminal.get_screen_resolution()  # Получаем размеры экрана
        screen_width = screen_size[0]  # Ширина экрана
        screen_height = screen_size[1]  # Высота экрана
        element = self._get_element(locator=locator, timeout_elem=timeout, contains=contains)  # Получаем элемент по локатору
        if element is None:
            return False
        if not element.get_attribute('displayed') == 'true':
            # Если элемент не отображается на экране
            return False
        element_location = element.location  # Получаем координаты элемента
        element_size = element.size  # Получаем размеры элемента
        if (
                element_location['y'] + element_size['height'] > screen_height or
                element_location['x'] + element_size['width'] > screen_width or
                element_location['y'] < 0 or
                element_location['x'] < 0
        ):
            # Если элемент находится за пределами экрана
            return False
        # Если элемент находится на экране
        return True
