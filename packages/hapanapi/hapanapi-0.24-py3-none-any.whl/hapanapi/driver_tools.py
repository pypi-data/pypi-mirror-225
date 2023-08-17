import os
from selenium import webdriver
from contextlib import contextmanager


CHROME_PATH = os.path.abspath(os.path.join(os.path.dirname(__name__), 'driver', 'chromedriver'))
CHROME_BIN = None


def driver_init(CHROME_PATH, CHROME_BIN=None):
    options = webdriver.ChromeOptions()
    if CHROME_BIN:
        options.binary_location = CHROME_BIN
    options.add_argument('--window-size=1200,800')
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--incognito')
    driver = webdriver.Chrome(executable_path=CHROME_PATH, options=options)
    return driver


@contextmanager
def driver_context(type='chrome'):
    if type == 'chrome':
        driver = driver_init(CHROME_PATH, CHROME_BIN)
        yield driver
    else:               # Adding firefox executable path
        driver = webdriver.Firefox(executable_path=CHROME_PATH, service_args=['--load-images=no'])
        driver.set_window_size(1120, 550)
        yield driver
    driver.quit()