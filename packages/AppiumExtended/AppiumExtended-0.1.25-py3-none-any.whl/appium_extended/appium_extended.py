# coding: utf-8
import inspect
import logging
import sys
import time
import traceback
from typing import Union, Tuple, Dict, List, Optional, cast, Any
import numpy as np
from PIL import Image

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver import WebElement

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

from appium_extended.appium_swipe import AppiumSwipe
from appium_extended.appium_wait import AppiumWait
from appium_extended.appium_tap import AppiumTap
from appium_extended.appium_is import AppiumIs

from appium_extended_web_element.web_element_extended import WebElementExtended

from appium_extended_utils import utils


class AppiumExtended(AppiumIs, AppiumTap, AppiumSwipe, AppiumWait):
    """
    Класс работы с Appium.
    Обеспечивает работу с устройством
    """

    def __init__(self, logger: logging.Logger = None, log_level: int = logging.INFO, log_path: str = ''):
        if logger is None:
            logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        if bool(log_path):
            if not log_path.endswith('.log'):
                log_path = log_path + '.log'
            file_handler = logging.FileHandler(log_path)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        super().__init__(logger=logger)

    def get_element(self,
                    locator: Union[Tuple, WebElementExtended, Dict[str, str], str] = None,
                    by: Union[MobileBy, AppiumBy, By, str] = None,
                    value: Union[str, Dict, None] = None,
                    timeout_elem: int = 10,
                    timeout_method: int = 600,
                    elements_range: Union[Tuple, List[WebElementExtended], Dict[str, str], None] = None,
                    contains: bool = True,
                    ) -> Union[WebElementExtended, None]:
        """
        Получает элемент на странице, используя указанный локатор или параметры.

        Аргументы:
        - locator (Union[Tuple, WebElementExtended, Dict[str, str], str], optional):
            Локатор или элемент для поиска. По умолчанию None.
        - by (Union[MobileBy, AppiumBy, By, str], optional): Метод поиска элемента.
            По умолчанию None.
        - value (Union[str, Dict, None], optional): Значение для поиска элемента.
            По умолчанию None.
        - timeout_elem (int, optional): Время ожидания появления элемента.
            По умолчанию 10.
        - timeout_method (int, optional): Время ожидания выполнения метода.
            По умолчанию 600.
        - elements_range (Union[Tuple, List[WebElementExtended], Dict[str, str], None], optional):
            Диапазон элементов для выбора. По умолчанию None.
        - contains (bool, optional): Флаг, указывающий на необходимость использования частичного совпадения текста.
            По умолчанию True.

        Возвращает:
        - Union[WebElementExtended, None]: Расширенный элемент WebElementExtended или None, если элемент не найден.
        """
        element = self._get_element(locator=locator,
                                    by=by,
                                    value=value,
                                    timeout_elem=timeout_elem,
                                    timeout_method=timeout_method,
                                    elements_range=elements_range,
                                    contains=contains)
        return WebElementExtended(driver=element.parent, element_id=element.id, logger=self.logger)

    def get_elements(self,
                     locator: Union[Tuple, List[WebElement], Dict[str, str], str] = None,
                     by: Union[MobileBy, AppiumBy, By, str] = None,
                     value: Union[str, Dict, None] = None,
                     timeout_elements: int = 10,
                     timeout_method: int = 600,
                     elements_range: Union[Tuple, List[WebElement], Dict[str, str], None] = None,
                     contains: bool = True,
                     ) -> Union[List[WebElementExtended], List]:
        """
        Получает элементы на странице, используя указанный локатор или параметры.

        Args:
        - locator (Union[Tuple, List[WebElement], Dict[str, str], str], optional): Локатор или элементы для поиска.
            По умолчанию None.
        - by (Union[MobileBy, AppiumBy, By, str], optional): Метод поиска элементов.
            По умолчанию None.
        - value (Union[str, Dict, None], optional): Значение для поиска элементов.
            По умолчанию None.
        - timeout_elements (int, optional): Время ожидания появления элементов.
            По умолчанию 10.
        - timeout_method (int, optional): Время ожидания выполнения метода.
            По умолчанию 600.
        - elements_range (Union[Tuple, List[WebElement], Dict[str, str], None], optional): Диапазон элементов для выбора.
            По умолчанию None.
        - contains (bool, optional): Флаг, указывающий на необходимость использования частичного совпадения текста.
            По умолчанию True.

        Returns:
        - Union[List[WebElementExtended], List]: Список расширенных элементов WebElementExtended или обычных элементов WebElement в случае ошибки.
        """
        elements = super()._get_elements(locator=locator,
                                         by=by,
                                         value=value,
                                         timeout_elements=timeout_elements,
                                         timeout_method=timeout_method,
                                         elements_range=elements_range,
                                         contains=contains)
        elements_ext = []
        for element in elements:
            elements_ext.append(WebElementExtended(driver=element.parent, element_id=element.id, logger=self.logger))
        return elements_ext

    def get_image_coordinates(self,
                              image: Union[bytes, np.ndarray, Image.Image, str],
                              full_image: Union[bytes, np.ndarray, Image.Image, str] = None,
                              threshold: float = 0.7,
                              ) -> Union[Tuple, None]:
        return self._get_image_coordinates(full_image=full_image,
                                           image=image,
                                           threshold=threshold)

    def get_inner_image_coordinates(self,
                                    outer_image_path: Union[bytes, np.ndarray, Image.Image, str],
                                    inner_image_path: Union[bytes, np.ndarray, Image.Image, str],
                                    threshold: Optional[float] = 0.9
                                    ) -> Union[Tuple[int, int, int, int], None]:
        """
        Возвращает координаты x y (относительно экрана) по изображению внутри другого изображения
        """
        return self._get_inner_image_coordinates(outer_image_path=outer_image_path,
                                                 inner_image_path=inner_image_path,
                                                 threshold=threshold)

    def get_many_coordinates_of_image(self,
                                      image: Union[bytes, np.ndarray, Image.Image, str],
                                      full_image: Union[bytes, np.ndarray, Image.Image, str] = None,
                                      cv_threshold: Optional[float] = 0.7,
                                      coord_threshold: Optional[int] = 5,
                                      ) -> Union[List[Tuple], None]:
        return self.helper.get_many_coordinates_of_image(full_image=full_image,
                                                        image=image,
                                                        cv_threshold=cv_threshold,
                                                        coord_threshold=coord_threshold)

    def get_text_coordinates(self,
                             text: str,
                             language: Optional[str] = 'rus',
                             image: Union[bytes, str, Image.Image, np.ndarray] = None,
                             ocr: Optional[bool] = True,
                             ) -> Union[Tuple[int, int, int, int], None]:  # TODO реализовать None
        """
        # TODO fill
        """
        if ocr:
            return self._get_text_coordinates(text=text, language=language, image=image)
        return self.get_element(locator={'text': text, 'displayed': 'true', 'enabled': 'true'}).get_coordinates()

    # DOM

    def get_element_contains(self,
                             ) -> Any:
        """
        Возвращает элемент содержащий определенный элемент
        """
        raise NotImplementedError("This method is not implemented yet.")  # TODO implement

    def get_elements_contains(self,
                              ) -> Any:
        """
        Возвращает элементы содержащие определенный(е) элемент(ы)
        """
        raise NotImplementedError("This method is not implemented yet.")  # TODO implement

    def get_screenshot_as_base64_decoded(self) -> bytes:
        return self._get_screenshot_as_base64_decoded()

    def find_and_get_element(self,
                             locator: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str],
                             timeout: int = 10,
                             ) -> Union[WebElementExtended, None]:
        """
        Ищет элемент на странице, если нет то скроллит все что скроллится и ищет там
        """
        if self.is_element_within_screen(locator=locator, timeout=1):
            return self.get_element(locator=locator, timeout_elem=timeout)
        recyclers = self.get_elements(locator={'scrollable': 'true', 'enabled': 'true', 'displayed': 'true'})
        for recycler in recyclers:
            try:
                if recycler.scroll_until_find(locator=locator):
                    return self.get_element(locator=locator, timeout_elem=timeout)
            except StaleElementReferenceException as e:
                current_function_name = inspect.currentframe().f_globals['__name__']
                self.logger.error(f"{current_function_name} ERROR: {e}")
                self.logger.error(f"arg {recycler=}")
                self.logger.error(f"arg {locator=}")
                traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
                self.logger.error(traceback_info)
        return None

    def is_element_within_screen(self,
                                 locator: Union[Tuple, WebElement, 'WebElementExtended', Dict[str, str], str],
                                 timeout: int = 10,
                                 ) -> bool:
        """
        Метод проверяет, находится ли заданный элемент на видимом экране.

        Аргументы:
        - locator (Union[tuple, WebElement]): Локатор или элемент, который нужно проверить.
        - timeout (int): Время ожидания элемента. Значение по умолчанию: 10.

        Возвращает:
        - bool: True, если элемент находится на экране, False, если нет.
        """
        return self._is_element_within_screen(locator=locator, timeout=timeout)

    def is_text_on_screen(self,
                          text: str,
                          language: str = 'rus',
                          ocr: bool = True,
                          contains: bool = True
                          ) -> bool:
        """
        Проверяет, присутствует ли заданный текст на экране.
        Если ocr=True:
            Распознавание текста производит с помощью библиотеки pytesseract.
        Если ocr=False:
            Производится поиск элемента по xpath.

        Аргументы:
        - text (str): Текст, который нужно найти на экране.
        - ocr (bool): Производить поиск по изображению или DOM.
        - language (str): Язык распознавания текста. Значение по умолчанию: 'rus'.
        - contains (bool): Только для ocr=False. Допускает фрагмент текста

        Возвращает:
        - bool: True, если заданный текст найден на экране. False в противном случае.
        """
        if ocr:
            return self.helper.is_text_on_ocr_screen(text=text, language=language)
        return self._is_element_within_screen(locator={'text': text}, contains=contains)

    def is_image_on_the_screen(self,
                               image: Union[bytes, np.ndarray, Image.Image, str],
                               threshold: float = 0.9,
                               ) -> bool:
        return self.helper.is_image_on_the_screen(image=image,
                                                  threshold=threshold)

    def tap(self,
            locator: Union[Tuple[str, str], WebElementExtended, WebElement, Dict[str, str], str] = None,
            x: int = None,
            y: int = None,
            image: Union[bytes, np.ndarray, Image.Image, str] = None,
            duration: Optional[int] = None,
            timeout: int = 5,
            ) -> Union['appium_extended', None]:
        """
        Тап по координатам / элементу / изображению
        """
        if locator is not None:
            # Извлечение координат
            x, y = self._extract_point_coordinates_by_typing(locator)
        if image is not None:
            start_time = time.time()
            while not self.is_image_on_the_screen(image=image) and time.time() - start_time < timeout:
                time.sleep(1)
            # Извлечение координат
            x, y = self._extract_point_coordinates_by_typing(image)

        assert self._tap(x=x, y=y,
                         duration=duration)
        # Возвращаем экземпляр класса appium_extended
        return cast('appium_extended', self)

    # SWIPE

    def swipe(self,
              start_position: Union[
                  Tuple[int, int], str, bytes, np.ndarray, Image.Image, WebElement, WebElementExtended, Tuple[str, str],
                  Dict[str, str]],
              end_position: Optional[Union[
                  Tuple[int, int], str, bytes, np.ndarray, Image.Image, WebElement, WebElementExtended, Tuple[str, str],
                  Dict[str, str]]] = None,
              direction: Optional[int] = None,
              distance: Optional[int] = None,
              duration: Optional[int] = 0,
              ) -> 'appium_extended':
        """
        Выполняет свайп (перетаскивание) элемента или изображения на экране.

        Параметры:
        - start_position: Позиция начала свайпа. Может быть задана в различных форматах:
            - Если `start_position` является кортежем и оба его элемента являются строками, то он представляет собой
              локатор элемента. В этом случае будет выполнен поиск элемента и используется его позиция.
            - Если `start_position` является словарем, то считается, что это локатор элемента, основанный на атрибутах.
              Например, {'text': 'some text'} или {'class': 'SomeClass', 'visible': 'true'}. В этом случае будет
              выполнен поиск элемента по указанным атрибутам, и используется его позиция.
            - Если `start_position` является экземпляром класса WebElement или WebElementExtended, то используется его
              позиция.
            - Если `start_position` является строкой, массивом байтов (bytes), массивом NumPy (np.ndarray) или объектом
              класса Image.Image, то считается, что это изображение. В этом случае будет вычислен центр изображения и
              используется его позиция.
            - Если `start_position` является кортежем, и оба его элемента являются целыми числами, то считается, что это
              координаты в формате (x_coordinate, y_coordinate).

        - end_position: Позиция конца свайпа. Принимает те же форматы, что и `start_position`. По умолчанию None.
        - direction (опционально): Направление свайпа. Принимает значения от 0 до 360 градусов.
          Если указано направление, то будет вычислена конечная точка свайпа на основе текущего размера окна и
          указанного расстояния. По умолчанию None.
        - distance (опционально): Расстояние свайпа. Принимается в пикселях. Используется только в сочетании с параметром
          `direction`. По умолчанию None.
        - duration (опционально): Продолжительность свайпа в миллисекундах. По умолчанию 0.

        Возвращает:
        - self: Экземпляр класса appium_extended.

        Примечания:
        - В качестве конечной позиции свайпа должен быть указан end_position или пара direction, distance.
        - str принимается как путь к изображению на экране и вычисляется его центр, а не как локатор элемента

        """
        # Извлечение координат начальной точки свайпа
        start_x, start_y = self._extract_point_coordinates_by_typing(start_position)

        if end_position is not None:
            # Извлечение координат конечной точки свайпа
            end_x, end_y = self._extract_point_coordinates_by_typing(end_position)
        else:
            # Извлечение координат конечной точки свайпа на основе направления и расстояния
            end_x, end_y = self._extract_point_coordinates_by_direction(direction, distance, start_x, start_y,
                                                                        screen_resolution=self.terminal.get_screen_resolution())

        # Выполнение свайпа
        assert self._swipe(start_x=start_x, start_y=start_y,
                           end_x=end_x, end_y=end_y,
                           duration=duration)

        # Возвращаем экземпляр класса appium_extended
        return cast('appium_extended', self)

    def swipe_right_to_left(self):
        window_size = self.terminal.get_screen_resolution()
        width = window_size[0]
        height = window_size[1]
        left = int(width * 0.1)
        right = int(width * 0.9)
        self.swipe(start_position=(right, height // 2),
                   end_position=(left, height // 2))

    def swipe_left_to_right(self):
        window_size = self.terminal.get_screen_resolution()
        width = window_size[0]
        height = window_size[1]
        left = int(width * 0.1)
        right = int(width * 0.9)
        self.swipe(start_position=(left, height // 2),
                   end_position=(right, height // 2))

    def swipe_top_to_bottom(self):
        window_size = self.terminal.get_screen_resolution()
        height = window_size[1]
        top = int(height * 0.1)
        bottom = int(height * 0.9)
        self.swipe(start_position=(top, height // 2),
                   end_position=(bottom, height // 2))

    def swipe_bottom_to_top(self):
        window_size = self.terminal.get_screen_resolution()
        height = window_size[1]
        top = int(height * 0.1)
        bottom = int(height * 0.9)
        self.swipe(start_position=(bottom, height // 2),
                   end_position=(top, height // 2))

    # WAIT

    def wait_for(self,
                 locator: Union[Tuple[str, str], WebElement, 'WebElementExtended', Dict[str, str], str,
                 List[Tuple[str, str]], List[WebElement], List['WebElementExtended'], List[Dict[str, str]], List[
                     str]] = None,
                 image: Union[bytes, np.ndarray, Image.Image, str,
                 List[bytes], List[np.ndarray], List[Image.Image], List[str]] = None,
                 timeout: int = 10,
                 contains: bool = True,
                 full_image: Union[bytes, np.ndarray, Image.Image, str] = None,
                 ):
        return self._wait_for(locator=locator,
                              image=image,
                              timeout=timeout,
                              contains=contains)

    def wait_for_not(self,
                     locator: Union[Tuple[str, str], WebElement, 'WebElementExtended', Dict[str, str], str,
                     List[Tuple[str, str]], List[WebElement], List['WebElementExtended'], List[Dict[str, str]], List[
                         str]] = None,
                     image: Union[bytes, np.ndarray, Image.Image, str,
                     List[bytes], List[np.ndarray], List[Image.Image], List[str]] = None,
                     timeout: int = 10,
                     contains: bool = True,
                     ):
        return self._wait_for_not(locator=locator, image=image, timeout=timeout, contains=contains)

    def wait_return_true(self, method, timeout: int = 10):
        return self._wait_return_true(method=method, timeout=timeout)

    # KEYBOARD

    def input_by_virtual_keyboard(self) -> 'appium_extended':  # TODO реализовать возврат cast('appium_extended', self)
        """
        Вводит с помощью виртуально клавиатуры
        """
        raise NotImplementedError("This method is not implemented yet.")

    # OTHER

    def draw_by_coordinates(self,
                            image: Union[bytes, str, Image.Image, np.ndarray] = None,
                            coordinates: Tuple[int, int, int, int] = None,
                            top_left: Tuple[int, int] = None,
                            bottom_right: Tuple[int, int] = None,
                            path: str = None,
                            ) -> 'appium_extended':
        assert self.helper.draw_by_coordinates(image=image,
                                              coordinates=coordinates,
                                              top_left=top_left,
                                              bottom_right=bottom_right,
                                              path=path)
        return cast('appium_extended', self)

    # PRIVATE

    def _extract_point_coordinates_by_typing(self,
                                             position:
                                             Union[Tuple[int, int], str, bytes, np.ndarray, Image.Image,
                                             Tuple[str, str], Dict, WebElement, WebElementExtended]
                                             ) -> Tuple[int, int]:
        """
        Извлекает координаты точки на основе типа переданной позиции.

        Параметры:
            position (
            Union[Tuple[int, int], str, bytes, np.ndarray, Image.Image, Dict, WebElement, WebElementExtended]
            ):
                Позиция, для которой нужно извлечь координаты.
                Либо локатор элемента, либо изображение, либо кортеж из координат.

        Возвращает:
            Tuple[int, int]: Кортеж координат точки, в формате (x, y).
        """
        x, y = 0, 0
        # Вычисление позиции начала свайпа
        if (isinstance(position, Tuple) and
                isinstance(position[0], int) and
                isinstance(position[1], int)):
            # Если position является кортежем с двумя целыми числами, то считаем, что это координаты
            x, y = position
        elif (isinstance(position, Tuple) and
              isinstance(position[0], str) and
              isinstance(position[1], str)) or \
                isinstance(position, WebElement) or \
                isinstance(position, WebElementExtended) or \
                isinstance(position, Dict):
            # Если position является кортежем с двумя строковыми элементами или экземпляром WebElement,
            # WebElementExtended или словарем, то получаем координаты центра элемента
            x, y = utils.calculate_center_of_coordinates(
                self.get_element(locator=position).get_coordinates())
        elif isinstance(position, (bytes, np.ndarray, Image.Image, str)):
            # Если position является строкой, байтами, массивом NumPy или объектом Image.Image,
            # то получаем координаты центра изображения
            x, y = utils.calculate_center_of_coordinates(
                self.get_image_coordinates(image=position))
        return x, y

    @staticmethod
    def _extract_point_coordinates_by_direction(direction: int, distance: int,
                                                start_x: int, start_y: int,
                                                screen_resolution: tuple
                                                ) -> Tuple[int, int]:
        """
        Извлекает координаты точки на заданном расстоянии и в заданном направлении относительно начальных координат.

        Параметры:
            direction (str): Направление движения в пределах 360 градусов.
            distance (int): Расстояние, на которое нужно переместиться относительно начальных координат в пикселях.
            start_x (int): Начальная координата X.
            start_y (int): Начальная координата Y.

        Возвращает:
            Tuple[int, int]: Координаты конечной точки в формате (x, y).
        """
        width = screen_resolution[0]
        height = screen_resolution[1]
        end_x, end_y = utils.find_coordinates_by_vector(width=width, height=height,
                                                        direction=direction, distance=distance,
                                                        start_x=start_x, start_y=start_y)
        return end_x, end_y
