from setuptools import setup, find_packages

# Общее описание пакета
long_description = '''
An extension library for adding ease of use to Appium-Python-Client.

appium_extended is a collection of utilities and convenience functions designed to enhance the usage of Appium-Python-Client for mobile app automation testing. It provides additional functionalities and abstractions to simplify the testing process.
'''

setup(
    name='AppiumExtended',
    version='0.1.25',
    description='An extension library for adding ease of use Appium-Python-Client',
    author='molokov-klim',
    packages=find_packages(),
    install_requires=[
        'Appium-Python-Client>=2.11.1',
        'allure-pytest>=2.13.2',
        'zlib-compress>=0.0.1',
        'zlib-decompress>=0.0.2',
        'pylibjpeg>=1.4.0',
        'Pillow>=9.5.0',
        'requests>=2.31.0',
        'pyserial>=3.5',
        'opencv-python>=4.8.0.74',
        'pytesseract>=0.3.10',
        'numpy>=1.25.1',
        'selenium>=4.10.0',
    ],
    # Добавляем описание в setup()
    long_description=long_description,
    long_description_content_type='text/plain',  # Указываем тип контента (обычный текст)
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    url='https://github.com/molokov-klim/appium_extended',
)
