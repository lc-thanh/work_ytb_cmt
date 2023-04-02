import random
from time import sleep

import gspread
from common import close_browser, set_zoom, get_account_first
from selenium.webdriver import Keys, ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# is_random = 1 => scroll up
# is_random = -1 => scroll down
# is_random = 0 => scroll random
def scroll_random(browser, count_scroll, is_random=0):
    print("scroll_random")
    for scroll in range(int(count_scroll)):
        value_scroll = random.uniform(100, 400)
        if is_random == -1 or (random.choice([False, True]) and is_random == 0):
            browser.execute_script("window.scrollTo(0, window.scrollY - " + str(value_scroll) + ")")
        else:
            browser.execute_script("window.scrollTo(0, window.scrollY + " + str(value_scroll) + ")")
        sleep(random.uniform(0.5, 2))


def click_element(browser, element_xpath, is_scroll=False):
    index_error = 0
    while True:
        if index_error > 4:
            return False
        try:
            bt_add = browser.find_element(By.XPATH, element_xpath)
            if is_scroll:
                browser.execute_script("arguments[0].scrollIntoView();", bt_add)
                sleep(random.uniform(1, 2.5))
            bt_add.click()
            sleep(random.uniform(2, 3.5))
            return True
        except:
            index_error = index_error + 1
            print("not click sleep 10s")
            sleep(10)


def input_type_char(browser, xpath, values, is_enter=True):
    print("input_type_char")
    index_error = 0
    while True:
        if index_error > 2:
            return False
        try:
            el_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            el_input.click()
            sleep(random.uniform(0.5, 1))
            el_input.clear()
            sleep(random.uniform(0.5, 1))
            is_delete = 0
            for value in values:
                if random.choice([False, True]) and random.choice([False, True]):
                    is_delete = is_delete + 1
                    if is_delete < 3:
                        el_input.send_keys(
                            random.choice(['a', 'b', 'c', 'd', 'f', 'e', 'r', 't', 'm', 'n', 's', 'v', 'l']))
                        sleep(random.uniform(0.1, 0.3))
                        el_input.send_keys(Keys.BACKSPACE)
                        sleep(random.uniform(0.1, 0.3))
                el_input.send_keys(value)
                sleep(random.uniform(0.1, 0.3))
            if is_delete == 0:
                el_input.send_keys(random.choice(['a', 'b', 'c', 'd', 'f', 'e', 'r', 't', 'm', 'n', 's', 'v', 'l']))
                sleep(random.uniform(0.1, 0.3))
                el_input.send_keys(Keys.BACKSPACE)
                sleep(random.uniform(0.1, 0.3))
            if is_enter:
                el_input.send_keys(Keys.ENTER)
                sleep(random.uniform(0.5, 2))
            return True
        except Exception as ex:
            index_error = index_error + 1
            print("not input_type_char sleep 10s " + str(ex))
            sleep(10)
