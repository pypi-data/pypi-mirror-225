# coding: utf-8
import base64
import logging
import os
from typing import Union, List, Tuple, Optional

import cv2
import numpy as np
from PIL import Image
from pytesseract import pytesseract

from selenium.common.exceptions import WebDriverException

from appium_extended_helpers import helpers_decorators
from appium_extended_terminal.terminal import Terminal


class AppiumImage:
    """
    Класс работы с Appium.
    Обеспечивает работу с изображениями
    """

    def __init__(self, driver, logger: logging.Logger):
        self.logger = logger
        self.driver = driver
        self.terminal = Terminal(driver=self.driver, logger=logger)


    def get_screenshot_as_base64_decoded(self):
        screenshot = self.driver.get_screenshot_as_base64().encode('utf-8')
        screenshot = base64.b64decode(screenshot)
        return screenshot

    @helpers_decorators.retry
    def get_image_coordinates(self,
                              image: Union[bytes, np.ndarray, Image.Image, str],
                              full_image: Union[bytes, np.ndarray, Image.Image, str] = None,
                              threshold: Optional[float] = 0.7,
                              ) -> Union[Tuple[int, int, int, int], None]:
        """
        Находит координаты наиболее вероятного совпадения частичного изображения в полном изображении.
        Предназначен для поиска координат наиболее вероятного совпадения частичного изображения в полном изображении.

        Args:
            image (Union[bytes, np.ndarray, Image.Image, str]): путь к файлу частичного изображения, которое
            нужно найти внутри полного изображения.
            full_image (Union[bytes, np.ndarray, Image.Image, str]): путь к файлу полного изображения.
            threshold (float, optional): минимальный порог совпадения, необходимый для считывания совпадения допустимым.
                По умолчанию равно 0.7.

        Returns:
            tuple or None: кортеж с координатами наиболее вероятного совпадения (x1, y1, x2, y2) или None, если совпадение не найдено.
            :param threshold:
            :param full_image:
        """
        if full_image is None:
            screenshot = self.get_screenshot_as_base64_decoded()
            big_image = self.to_ndarray(image=screenshot, grayscale=True)
        else:
            big_image = self.to_ndarray(image=full_image, grayscale=True)  # Загрузка полного изображения

        small_image = self.to_ndarray(image=image, grayscale=True)  # Загрузка частичного изображения

        result = cv2.matchTemplate(big_image, small_image, cv2.TM_CCOEFF_NORMED)  # Поиск совпадений методом шаблона

        _, max_val, _, max_loc = cv2.minMaxLoc(
            result)  # Получение наименьшего и наибольшего значения, а также соответствующих координат

        if not max_val >= threshold:  # Если наибольшее значение совпадения не превышает порога, возвращаем None
            self.logger.error("find_coordinates_by_image(): Совпадений не найдено")
            return None

        # Вычисляем координаты левого верхнего и правого нижнего углов найденного совпадения
        left = int(max_loc[0])
        top = int(max_loc[1])
        width = small_image.shape[1]
        height = small_image.shape[0]
        right = left + width
        bottom = top + height

        return int(left), int(top), int(right), int(bottom)  # Возвращаем координаты наиболее вероятного совпадения

    @helpers_decorators.retry
    def get_inner_image_coordinates(self,
                                    outer_image_path: Union[bytes, np.ndarray, Image.Image, str],
                                    inner_image_path: Union[bytes, np.ndarray, Image.Image, str],
                                    threshold: float = 0.9) -> Union[Tuple[int, int, int, int], None]:
        """
        Находит изображение на экране и внутри него находит другое изображение (внутреннее).
        Предназначен для поиска изображения на экране и затем нахождения другого изображения (внутреннего)
        внутри этого обнаруженного изображения.

        Параметры:
            outer_image_path (str): Путь к файлу с изображением, которое нужно найти на экране.
            inner_image_path (str): Путь к файлу с изображением, которое нужно найти внутри внешнего изображения.
            threshold (float, optional): Пороговое значение сходства для шаблонного сопоставления. По умолчанию 0.9.

        Возвращает:
            tuple: Координаты внутреннего изображения относительно экрана в формате ((x1, y1), (x2, y2)).
                   Если внутреннее изображение не найдено, возвращает None.
        """
        # Получаем разрешение экрана
        screen_width, screen_height = self.terminal.get_screen_resolution()

        # Захватываем скриншот
        screenshot = base64.b64decode(self.driver.get_screenshot_as_base64())

        # Читаем скриншот
        full_image = self.to_ndarray(image=screenshot, grayscale=True)

        # Прочитать внешнее изображение
        outer_image = self.to_ndarray(image=outer_image_path, grayscale=True)

        # Прочитать внутреннее изображение
        inner_image = self.to_ndarray(image=inner_image_path, grayscale=True)

        # Вычисляем коэффициенты масштабирования
        width_ratio = screen_width / full_image.shape[1]
        height_ratio = screen_height / full_image.shape[0]

        # ...
        inner_image = cv2.resize(inner_image, None, fx=width_ratio, fy=height_ratio)
        outer_image = cv2.resize(outer_image, None, fx=width_ratio, fy=height_ratio)

        # Применить шаблонное сопоставление для поиска внешнего изображения
        outer_result = cv2.matchTemplate(full_image, outer_image, cv2.TM_CCOEFF_NORMED)

        # Найти максимальное значение сходства и его положение для внешнего изображения
        _, outer_max_val, _, outer_max_loc = cv2.minMaxLoc(outer_result)

        # Проверить, превышает ли максимальное значение сходства для внешнего изображения пороговое значение
        if outer_max_val >= threshold:
            # Получить размеры внешнего изображения
            outer_height, outer_width = outer_image.shape

            # Вычислить координаты внешнего изображения на экране
            outer_top_left = outer_max_loc
            outer_bottom_right = (outer_top_left[0] + outer_width, outer_top_left[1] + outer_height)

            # Извлечь область интереса (ROI), содержащую внешнее изображение
            outer_roi = full_image[outer_top_left[1]:outer_bottom_right[1], outer_top_left[0]:outer_bottom_right[0]]

            # Применить шаблонное сопоставление для поиска внутреннего изображения внутри ROI
            inner_result = cv2.matchTemplate(outer_roi, inner_image, cv2.TM_CCOEFF_NORMED)

            # Найти максимальное значение сходства и его положение для внутреннего изображения внутри ROI
            _, inner_max_val, _, inner_max_loc = cv2.minMaxLoc(inner_result)

            # Проверить, превышает ли максимальное значение сходства для внутреннего изображения пороговое значение
            if inner_max_val >= threshold:
                # Получить размеры внутреннего изображения
                inner_height, inner_width = inner_image.shape

                # Вычислить координаты внутреннего изображения относительно экрана
                inner_top_left = (outer_top_left[0] + inner_max_loc[0], outer_top_left[1] + inner_max_loc[1])
                inner_bottom_right = (inner_top_left[0] + inner_width, inner_top_left[1] + inner_height)

                # Вернуть координаты внутреннего изображения относительно экрана
                return inner_top_left + inner_bottom_right

        # Вернуть None, если внутреннее изображение не найдено
        return None

    def is_image_on_the_screen(self,
                               image: Union[bytes, np.ndarray, Image.Image, str],
                               threshold: float = 0.9) -> bool:
        """
        Сравнивает, присутствует ли заданное изображение на экране.

        Args:
            image: Строка, содержащая имя файла частичного изображения для поиска.
            threshold: Пороговое значение схожести части изображения со снимком экрана

        Returns:
            Логическое значение, указывающее, было ли частичное изображение найдено на экране.
        """
        try:
            screenshot = self.get_screenshot_as_base64_decoded()

            # Чтение снимка экрана и частичного изображения
            full_image = self.to_ndarray(image=screenshot, grayscale=True)
            small_image = self.to_ndarray(image=image, grayscale=True)

            # Проверка размеров изображений
            if small_image.shape[0] > full_image.shape[0] or small_image.shape[1] > full_image.shape[1]:
                self.logger.error("Частичное изображение больше снимка экрана.")
                return False

            # Сопоставление частичного изображения и снимка экрана
            result = cv2.matchTemplate(full_image, small_image, cv2.TM_CCOEFF_NORMED)

            # Извлечение коэффициента схожести и координат схожего участка
            _, max_val, _, _ = cv2.minMaxLoc(result)

            # Логирование
            self.logger.debug(f"Коэффициент схожести изображения: {max_val}")

            # Сравнение коэффициента схожести и порогового значения
            return max_val >= threshold

        except cv2.error as e:
            self.logger.error(f"is_image_on_the_screen(): {e}")
            return False
        except AssertionError as e:
            self.logger.error(f"is_image_on_the_screen(): {e}")
            return False
        except Exception as e:
            self.logger.error(f"is_image_on_the_screen(): {e}")
            return False

    def is_text_on_ocr_screen(self,
                              text: str,
                              screen: Union[bytes, np.ndarray, Image.Image, str] = None,
                              language: str = 'rus') -> bool:
        """
        Проверяет, присутствует ли заданный текст на экране.
        Распознавание текста производит с помощью библиотеки pytesseract.

        Аргументы:
        - text (str): Текст, который нужно найти на экране.
        - screen (bytes, optional): Скриншот в формате bytes. Если не указан, будет захвачен скриншот с помощью `self.driver`.
        - language (str): Язык распознавания текста. Значение по умолчанию: 'rus'.

        Возвращает:
        - bool: True, если заданный текст найден на экране. False в противном случае.
        """
        try:
            if screen is None:
                screenshot = self.get_screenshot_as_base64_decoded()
                image = self.to_ndarray(screenshot)
            else:
                image = self.to_ndarray(screen)

            # Бинаризация изображения
            _, image_bin = cv2.threshold(image, 0, 255,
                                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Применение бинаризации для получения двоичного изображения

            # Преобразование двоичного изображения в текст
            custom_config = r'--oem 3 --psm 6'
            ocr_text = pytesseract.image_to_string(image_bin, lang=language, config=custom_config)

            # Проверка наличия заданного текста в распознанном тексте
            return text.lower() in ocr_text.lower()

        except cv2.error as e:
            self.logger.error(f"is_text_on_ocr_screen(): {e}")
            return False
        except pytesseract.TesseractError as e:
            self.logger.error(f"is_text_on_ocr_screen(): {e}")
            return False
        except AssertionError as e:
            self.logger.error(f"is_text_on_ocr_screen(): {e}")
            return False
        except Exception as e:
            self.logger.error(f"is_text_on_ocr_screen(): {e}")
            return False

    @helpers_decorators.retry
    def get_many_coordinates_of_image(self,
                                      image: Union[bytes, np.ndarray, Image.Image, str],
                                      full_image: Union[bytes, np.ndarray, Image.Image, str] = None,
                                      cv_threshold: float = 0.7,
                                      coord_threshold: int = 5) -> Union[List[Tuple], None]:
        """
        Находит все вхождения частичного изображения внутри полного изображения.

        Args:
            full_image (str): путь к файлу полного изображения.
            image (str): путь к файлу частичного изображения, которое нужно найти внутри полного изображения.
            cv_threshold (float, optional): минимальный порог совпадения, необходимый для считывания совпадения допустимым.
                По умолчанию равно 0.7.
            coord_threshold (int, optional): целое число, представляющее максимальное различие между значениями x и y двух
                кортежей, чтобы они считались слишком близкими друг к другу. По умолчанию равно 5.

        Returns:
            list of tuples or None: список кортежей, содержащий расположение каждого найденного совпадения.
                Если совпадений не найдено, возвращается None.
        """

        if full_image is None:
            screenshot = self.get_screenshot_as_base64_decoded()
            big_image = self.to_ndarray(image=screenshot, grayscale=True)
        else:
            big_image = self.to_ndarray(image=full_image, grayscale=True)  # Загрузка полного изображения

        small_image = self.to_ndarray(image=image, grayscale=True)  # Загрузка частичного изображения

        # Найти частичное изображение в полном изображении
        result = cv2.matchTemplate(big_image, small_image, cv2.TM_CCOEFF_NORMED)  # Поиск совпадений методом шаблона

        # Получить все совпадения выше порога
        locations = np.where(result >= cv_threshold)  # Нахождение всех совпадений выше порога
        matches = list(zip(*locations[::-1]))  # Преобразование координат в список кортежей

        # Фильтрация слишком близких совпадений
        unique_list = []  # Создаем пустой список для хранения уникальных кортежей
        for (x1_coordinate, y1_coordinate) in matches:  # Итерируемся по списку кортежей
            exclude = False  # Инициализируем флаг exclude значением False
            for (x2_coordinate, y2_coordinate) in unique_list:  # Итерируемся по уникальным кортежам
                if abs(x1_coordinate - x2_coordinate) <= coord_threshold and abs(
                        y1_coordinate - y2_coordinate) <= coord_threshold:
                    # Если различие между значениями x и y двух кортежей меньше или равно порогу,
                    # помечаем exclude как True и выходим из цикла
                    exclude = True
                    break
            if not exclude:  # Если exclude равно False, добавляем кортеж в unique_list
                unique_list.append((x1_coordinate, y1_coordinate))
        matches = unique_list

        if not matches:
            self.logger.error(f"_find_many_coordinates_by_image() NO MATCHES, {image=}")
            return None

        # Добавляем правый нижний угол к каждому найденному совпадению
        matches_with_corners = []
        for match in matches:
            x_coordinate, y_coordinate = match
            width, height = small_image.shape[::-1]
            top_left = (x_coordinate, y_coordinate)
            bottom_right = (x_coordinate + width, y_coordinate + height)
            matches_with_corners.append((top_left + bottom_right))

        return matches_with_corners

    @helpers_decorators.retry
    def get_text_coordinates(
            self,
            text: str,
            image: Union[bytes, str, Image.Image, np.ndarray] = None,
            language: str = 'rus'
    ) -> Optional[tuple[int, ...]]:
        """
        Возвращает координаты области с указанным текстом на предоставленном изображении или снимке экрана.

        Аргументы:
        - text (str): Искомый текст.
        - image (bytes, str, Image.Image, np.ndarray, опционально): Изображение, на котором осуществляется поиск текста.
          Если не указано, будет использован снимок экрана. По умолчанию None.
        - language (str, опционально): Язык для распознавания текста. По умолчанию 'rus'.

        Возвращает:
        - Union[Tuple[int, int, int, int], None]: Координаты области с текстом или None, если текст не найден.
        """

        if not image:
            # Получаем снимок экрана, если изображение не предоставлено
            screenshot = self.get_screenshot_as_base64_decoded()  # Получение снимка экрана в формате base64
            image = self.to_ndarray(image=screenshot,
                                    grayscale=True)  # Преобразование снимка экрана в массив numpy и преобразование в оттенки серого
        else:
            # Если предоставлено, то преобразуем
            image = self.to_ndarray(image=image,
                                    grayscale=True)  # Преобразование изображения в массив numpy и преобразование в оттенки серого

        # Бинаризация изображения
        _, threshold = cv2.threshold(image, 0, 255,
                                     cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Применение бинаризации для получения двоичного изображения

        # Выполнение OCR с помощью PyTesseract
        data = pytesseract.image_to_data(threshold, lang=language,
                                         output_type=pytesseract.Output.DICT)  # Использование PyTesseract для распознавания текста и получения информации о распознанных словах

        formatted_data = {}
        for i in range(len(data['text'])):
            word_text = data['text'][i]  # Текст слова
            left = int(data['left'][i])  # Координата левой границы слова
            top = int(data['top'][i])  # Координата верхней границы слова
            width = int(data['width'][i])  # Ширина слова
            height = int(data['height'][i])  # Высота слова
            coordinates = [left, top, left + width, top + height]  # Координаты рамки слова

            if word_text:
                if i not in formatted_data:
                    formatted_data[i] = {}
                formatted_data[i] = {'text': word_text,
                                     'coordinates': coordinates}  # Сохранение информации о слове и его координатах

        # Разбить искомый текст на отдельные слова
        words = text.split(' ')  # Разделение искомого текста на отдельные слова

        # Инициализировать переменные для последовательности слов и соответствующих координат
        current_sequence = []  # Текущая последовательность слов
        result_coordinates = []  # Координаты текущей последовательности слов

        for word_data in formatted_data.values():
            word = word_data['text']  # Текущее слово
            coordinates = word_data['coordinates']  # Координаты слова

            if word in words:
                current_sequence.append(word)  # Добавление слова в текущую последовательность
                result_coordinates.append(coordinates)  # Добавление координат слова в результат
            else:
                if current_sequence == words:
                    # Если найдена последовательность слов, вернуть соответствующие координаты
                    top_left = tuple(map(int, result_coordinates[0][:2]))  # Верхний левый угол рамки
                    bottom_right = tuple(map(int, result_coordinates[-1][2:]))  # Нижний правый угол рамки
                    return top_left + bottom_right
                current_sequence = []  # Сброс текущей последовательности слов
                result_coordinates = []  # Сброс координат последовательности слов

        return None

    def draw_by_coordinates(self,
                            image: Union[bytes, str, Image.Image, np.ndarray] = None,
                            coordinates: Tuple[int, int, int, int] = None,
                            top_left: Tuple[int, int] = None,
                            bottom_right: Tuple[int, int] = None,
                            path: str = None) -> bool:
        """
        Рисует прямоугольник на предоставленном изображении или снимке экрана с помощью драйвера.
        Прямоугольник определяется либо координатами, либо верхней левой и нижней правой точками.
        Результирующее изображение с нарисованным прямоугольником сохраняется по указанному пути.

        Аргументы:
            image (Union[bytes, str, Image.Image], опционально): Изображение, на котором будет рисоваться.
                Может быть представлено в виде bytes, str (путь до файла) или PIL Image.
                Если не указано, используется снимок экрана. По умолчанию None.
            coordinates (Tuple[int, int, int, int], опционально): Координаты прямоугольника (x1, y1, x2, y2).
                По умолчанию None.
            top_left (Tuple[int, int], опционально): Верхняя левая точка прямоугольника (x, y). По умолчанию None.
            bottom_right (Tuple[int, int], опционально): Нижняя правая точка прямоугольника (x, y). По умолчанию None.
            path (str, опционально): Путь для сохранения результирующего изображения. По умолчанию None.

        Usage:
            image = self.driver.get_screenshot_as_base64().encode('utf-8')
            draw_by_coordinates(image=image, coordinates=(123, 123, 123, 123), path='pictures')

        Возвращает:
            bool: True, если операция выполнена успешно, False в противном случае.
        """
        try:
            if image is None:
                # Если изображение не предоставлено, получаем снимок экрана с помощью драйвера
                screenshot = self.get_screenshot_as_base64_decoded()
                image = self.to_ndarray(screenshot)
            else:
                image = self.to_ndarray(image)

            # Если верхняя левая и нижняя правая точки не предоставлены, используем координаты для определения
            # прямоугольника
            if not top_left and not bottom_right:
                top_left = (coordinates[0], coordinates[1])
                bottom_right = (coordinates[2], coordinates[3])

            # Сохраняем снимок экрана с нарисованным прямоугольником
            if path is None:
                path = "screenshot_with_text_coordinates.png"
            path = os.path.join(path)
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            cv2.imwrite(path, image)

            return True
        except WebDriverException as e:
            # Обрабатываем исключение WebDriverException и записываем ошибку в журнал
            self.logger.error(f'draw_by_coordinates() WebDriverException {e}')
            return False
        except cv2.error as e:
            # Обработка исключения cv2.error
            self.logger.error(f'draw_by_coordinates() cv2.error: {e}')
            return False

    @staticmethod
    def is_rgb(image: np.ndarray) -> bool:
        """
        Проверяет, является ли изображение цветным (RGB).

        Аргументы:
        - image: np.ndarray - Входное изображение в формате NumPy ndarray.

        Возвращает:
        - bool - True, если изображение является цветным (RGB), False - в противном случае.
        """
        return len(image.shape) == 3 and image.shape[2] == 3 or image.ndim == 3 or image.ndim == '3'

    @staticmethod
    def is_grayscale(image: np.ndarray) -> bool:
        """
        Проверяет, является ли изображение оттенков серого.

        Аргументы:
        - image: np.ndarray - Входное изображение в формате NumPy ndarray.

        Возвращает:
        - bool - True, если изображение является оттенков серого, False - в противном случае.
        """
        return len(image.shape) == 2 or (
                len(image.shape) == 3 and image.shape[2] == 1) or image.ndim == 2 or image.ndim == '2'

    def to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """
        Преобразует изображение в оттенки серого.

        Аргументы:
        - image: np.ndarray - Входное изображение в формате ndarray.

        Возвращает:
        - np.ndarray - Преобразованное изображение в оттенках серого.
        """
        # Проверяем, является ли изображение в формате RGB
        if self.is_rgb(image):
            # Если да, то преобразуем его в оттенки серого
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Приводим значения пикселей к диапазону от 0 до 255
            gray_image = cv2.convertScaleAbs(gray_image)
            return gray_image
        # Иначе, возвращаем изображение без изменений
        return image

    def to_ndarray(self, image: Union[bytes, np.ndarray, Image.Image, str], grayscale: bool = True) -> np.ndarray:
        """
        Преобразует входные данные из различных типов в ndarray (NumPy array).

        Аргументы:
        - image: Union[bytes, np.ndarray, Image.Image, str] - Входные данные,
          представляющие изображение. Может быть типами bytes, np.ndarray, PIL Image или str.

        Возвращает:
        - np.ndarray - Преобразованный массив NumPy (ndarray) представляющий изображение.
        """
        # Если входные данные являются массивом байтов, преобразовать их в массив NumPy
        if isinstance(image, bytes):
            image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

        # Если входные данные являются строкой с путем к файлу, открыть изображение и преобразовать в массив NumPy
        if isinstance(image, str):
            # image = np.array(Image.open(image))
            image = cv2.imread(image, cv2.IMREAD_COLOR)

        # Если входные данные являются объектом PIL Image, преобразовать его в массив NumPy
        if isinstance(image, Image.Image):
            image = np.array(image)

        # Вернуть преобразованный массив NumPy
        if grayscale:
            return self.to_grayscale(image=image)
        return image
