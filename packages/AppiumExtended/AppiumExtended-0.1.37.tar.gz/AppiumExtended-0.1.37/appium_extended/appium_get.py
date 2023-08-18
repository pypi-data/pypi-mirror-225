# coding: utf-8
import logging
import time
from typing import Union, Dict, List, Tuple

import numpy as np
from PIL import Image

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from appium.webdriver import WebElement
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.appiumby import AppiumBy

from appium_extended.appium_base import AppiumBase


class AppiumGet(AppiumBase):
    """
    Класс расширяющий Appium.
    Обеспечивает получение чего-либо со страницы.
    """

    def __init__(self, logger: logging.Logger):
        super().__init__(logger=logger)

    def _get_element(self,
                     locator: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str] = None,
                     by: Union[MobileBy, AppiumBy, By, str] = None,
                     value: Union[str, Dict, None] = None,
                     timeout_elem: int = 10,
                     timeout_method: int = 600,
                     elements_range: Union[Tuple, List[WebElement], Dict[str, str], None] = None,
                     contains: bool = False
                     ) -> \
            Union[WebElement, None]:
        """
        Метод обеспечивает поиск элемента в текущей DOM структуре.
        Должен принимать либо локатор, либо значения by и value.

        Usage:
            element = app._get_element(locator=("id", "foo")).
            element = app._get_element(element).
            element = app._get_element(locator={'text': 'foo'}).
            element = app._get_element(locator='/path/to/file/pay_agent.png').
            element = app._get_element(locator=part_image, elements_range={'class':'android.widget.FrameLayout', 'package':'ru.app.debug'}).
            element = app._get_element(by="id", value="ru.sigma.app.debug:id/backButton").
            element = app._get_element(by=MobileBy.ID, value="ru.sigma.app.debug:id/backButton").
            element = app._get_element(by=AppiumBy.ID, value="ru.sigma.app.debug:id/backButton").
            element = app._get_element(by=By.ID, value="ru.sigma.app.debug:id/backButton").

        Args:
            locator: tuple / WebElement / dict / str, определяет локатор элемента.
                tuple - локатор в виде ('атрибут', 'значение')
                WebElement - объект веб элемента
                dict - словарь, содержащий пары атрибут: значение
                str - путь до файла с изображением элемента.
            by: MobileBy, AppiumBy, By, str, тип локатора для поиска элемента (всегда в связке с value)
            value: str, dict, None, значение локатора или словарь аргументов, если используется AppiumBy.XPATH.
            timeout_elem: int, время ожидания элемента.
            timeout_method: int, время ожидания метода поиска элемента.
            elements_range: tuple, list, dict, None, ограничивает поиск элемента в указанном диапазоне
            (для поиска по изображению).
            contains: для поиска по dict, ищет элемент содержащий фрагмент значения

        Returns:
            WebElement или None, если элемент не был найден.
        """
        # Проверка и подготовка аргументов
        if (not locator) and (not by or not value):
            self.logger.error(f"Некорректные аргументы!\n"
                              f"{locator=}\n"
                              f"{by=}\n"
                              f"{value=}\n"
                              f"{timeout_elem=}\n")
            return None
        if not locator and (by and value):
            locator = (by, value)
        if locator is None:
            return None

        # Объявление стратегии поиска элементов
        locator_handler = {
            # возвращает себя же
            WebElement: self.helper.handle_webelement_locator,
            # возвращает себя же
            'WebElementExtended': self.helper.handle_webelement_locator,
            # составляет локатор типа tuple из словаря с атрибутами искомого элемента
            dict: self.helper.handle_dict_locator,
            # производит поиск элементов по фрагменту изображения, возвращает список элементов
            str: self.helper.handle_string_locator,
        }

        # Цикл подготовки локатора и поиска элементов
        start_time = time.time()
        while not isinstance(locator, WebElement) and time.time() - start_time < timeout_method:
            # Выявление типа данных локатора для его подготовки
            locator_type = type(locator)
            # Если локатор типа tuple, то выполняется извлечение элементов
            if isinstance(locator, tuple):
                wait = WebDriverWait(driver=self.driver, timeout=timeout_elem)
                try:
                    element = wait.until(EC.presence_of_element_located(locator))
                    return element
                except NoSuchElementException:
                    return None
                except TimeoutException:
                    # self.logger.error(f"Элемент не обнаружен!\n"
                    #                   f"{locator=}\n"
                    #                   f"{timeout_elem=}\n\n" +
                    #                   "{}\n".format(e))
                    # self.logger.error("page source ", self.driver.page_source)
                    return None
                except WebDriverException:
                    # self.logger.error(f"Элемент не обнаружен!\n"
                    #                   f"{locator=}\n"
                    #                   f"{timeout_elem=}\n\n" +
                    #                   "{}\n".format(e))
                    # self.logger.error("page source ", self.driver.page_source)
                    return None
            # Выполнение подготовки локатора
            handler = locator_handler.get(locator_type)
            if locator is None:
                return None
            locator = handler(locator=locator, timeout=timeout_elem, elements_range=elements_range, contains=contains)
        # Подбирает результат после поиска по изображению
        if isinstance(locator, WebElement):
            return locator
        self.logger.error(f"Что-то пошло не так\n"
                          f"{locator=}\n"
                          f"{by=}\n"
                          f"{value=}\n"
                          f"{timeout_elem=}\n"
                          f"{timeout_method=}\n")
        return None

    def _get_elements(self,
                      locator: Union[Tuple, List[WebElement], Dict[str, str], str] = None,
                      by: Union[MobileBy, AppiumBy, By, str] = None,
                      value: Union[str, Dict, None] = None,
                      timeout_elements: int = 10,
                      timeout_method: int = 600,
                      elements_range: Union[Tuple, List[WebElement], Dict[str, str], None] = None,
                      contains: bool = True) -> \
            Union[List[WebElement], None]:
        """
        Метод обеспечивает поиск элементов в текущей DOM структуре.
        Должен принять либо локатор, либо by и value.
        При locator:str настоятельно рекомендуется использовать диапазон поиска elements_range.

        Usage:
            elements = app.get_elements(locator=("id", "foo")).
            elements = app.get_elements(locator={'text': 'foo'}).
            elements = app.get_elements(locator='/path/to/file/pay_agent.png').
            elements = app.get_elements(by="id", value="ru.sigma.app.debug:id/backButton").
            elements = app.get_elements(by=MobileBy.ID, value="ru.sigma.app.debug:id/backButton").
            elements = app.get_elements(by=AppiumBy.ID, value="ru.sigma.app.debug:id/backButton").
            elements = app.get_elements(by=By.ID, value="ru.sigma.app.debug:id/backButton").

        Args:
            locator: tuple or WebElement or Dict[str, str], str, локатор tuple или Веб Элемент или словарь {'атрибут': 'значение'} или str как путь до файла с изображением элемента.
            by:[MobileBy, AppiumBy, By, str], тип локатора для поиска элемента (всегда в связке с value)
            value: Union[str, Dict, None], значение локатора или словарь аргументов, если используется AppiumBy.XPATH
            timeout_elements: #TODO fill me
            timeout_method: #TODO fill me
            elements_range: #TODO fill me

        Returns:
            Список WebElement'ов, или пустой список в случае их отсутствия.
        """
        # Проверка и подготовка аргументов
        if not locator and (not by or not value):
            self.logger.error(f"Некорректные аргументы!\n"
                              f"{locator=}\n"
                              f"{by=}\n"
                              f"{value=}\n"
                              f"{timeout_elements=}\n"
                              f"{timeout_method=}\n")
            return None
        if not locator and (by and value):
            locator = (by, value)
        if locator is None:
            return None

        # Объявление стратегии поиска элементов
        locator_handler = {
            # подразумевается список элементов, возвращает себя же
            list: self.helper.handle_webelement_locator_elements,
            # составляет локатор типа tuple из словаря с атрибутами искомого элемента
            dict: self.helper.handle_dict_locator_elements,
            # производит поиск элементов по фрагменту изображения, возвращает список элементов
            str: self.helper.handle_string_locator_elements,
        }

        # Цикл подготовки локатора и поиска элементов
        start_time = time.time()
        while not isinstance(locator, list) and time.time() - start_time < timeout_method:
            # Выявление типа данных локатора для его подготовки
            locator_type = type(locator)
            # Если локатор типа tuple, то выполняется извлечение элементов
            if isinstance(locator, tuple):
                wait = WebDriverWait(driver=self.driver, timeout=timeout_elements)
                try:
                    element = wait.until(EC.presence_of_all_elements_located(locator))
                    return element
                except WebDriverException:
                    # self.logger.error(f"Элемент не обнаружен!\n"
                    #                   f"{locator=}\n"
                    #                   f"{by=}\n"
                    #                   f"{value=}\n"
                    #                   f"{timeout_elements=}\n"
                    #                   f"{timeout_method=}\n\n" +
                    #                   "{}\n".format(e))
                    return None
            # Выполнение подготовки локатора
            handler = locator_handler.get(locator_type)
            locator = handler(locator=locator,
                              timeout=timeout_elements,
                              elements_range=elements_range,
                              contains=contains)
        # Подбирает результат после поиска по изображению
        if isinstance(locator, list):
            return locator
        self.logger.error(f"\nЧто-то пошло не так\n"
                          f"{locator=}\n"
                          f"{by=}\n"
                          f"{value=}\n"
                          f"{timeout_elements=}\n"
                          f"{timeout_method=}\n")
        return None

    def _get_image_coordinates(self,
                               image: Union[bytes, np.ndarray, Image.Image, str],
                               full_image: Union[bytes, np.ndarray, Image.Image, str] = None,
                               threshold: float = 0.7,
                               ) -> Union[Tuple[int, int, int, int], None]:
        return self.helper.get_image_coordinates(image=image, full_image=full_image, threshold=threshold)

    def _get_inner_image_coordinates(self,
                                     outer_image_path: Union[bytes, np.ndarray, Image.Image, str],
                                     inner_image_path: Union[bytes, np.ndarray, Image.Image, str],
                                     threshold: float = 0.9) -> \
            Union[Tuple[int, int, int, int], None]:
        return self.helper.get_inner_image_coordinates(outer_image_path=outer_image_path,
                                                      inner_image_path=inner_image_path,
                                                      threshold=threshold)

    def _get_text_coordinates(self,
                              text: str,
                              language: str = 'rus',
                              image: Union[bytes, str, Image.Image, np.ndarray] = None, ) -> Tuple[int, int, int, int]:
        return self.helper.get_text_coordinates(text=text, language=language, image=image)

    def _get_screenshot_as_base64_decoded(self):
        return self.helper.get_screenshot_as_base64_decoded()
