import os
import random
import string
from time import sleep

import gspread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dir_path = os.getcwd()


def get_random_string(length):
    # With combination of lower and upper case
    characters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(characters) for i in range(length))

    return result_str


def scroll_random(browser, count_scroll, is_random=1):
    print("scroll_random")
    step_scroll = random.randint(4, 6)
    for scroll in range(int(count_scroll)):
        value_scroll = random.uniform(100, 300)
        if is_random == 1 and count_scroll > 10 and scroll % step_scroll == 0:
            is_random = -1
        if is_random == -1 or (random.choice([False, True]) and is_random == 0):
            browser.execute_script("window.scrollTo(0, window.scrollY - " + str(value_scroll) + ")")
        else:
            browser.execute_script("window.scrollTo(0, window.scrollY + " + str(value_scroll) + ")")
        sleep(random.uniform(0.2, 0.8))


def cmt_video(browser, like_cmt=True, rep_cmt=True):
    """
    Phương thức tự động comment vào video đang xem

    :param browser: Biến trình duyệt
    :param like_cmt: Tự like comment vừa đăng, giá trị mặc định là True
    :param rep_cmt: Tự rep lại comment vừa đăng, giá trị mặc định là True
    :return: True nếu chạy xong, False nếu gặp lỗi
    """
    print("cmt_video")
    while True:
        try:
            sleep(random.uniform(1.5, 2.2))
            browser.execute_script("window.scrollTo(0, " + str(random.randint(450, 650)) + ")")
            sleep(random.uniform(1.2, 2.2))
            cmt_box = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer")))
            browser.execute_script('arguments[0].scrollIntoView({behavior: "smooth", block: "center"});', cmt_box)
            sleep(random.uniform(1.2, 2.5))
            cmt_box.click()
            sleep(random.uniform(1.2, 2.2))
            el_input = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="contenteditable-root"]')))
            el_input.click()
            sleep(random.uniform(0.2, 0.8))
            linkFile = dir_path + fr"\input\cmt-tool-pre.txt"
            with open(linkFile, encoding="utf-8") as f:
                text = f.readlines()
                b = len(text)
                while True:
                    a = text[random.randint(0, b - 1)].strip()
                    if len(a) > 0:
                        break
            print("cmt value " + str(a))
            el_input.send_keys(a)
            sleep(random.uniform(1.2, 2.2))
            click_object = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ytd-button-renderer[@id='submit-button']")))
            click_object.click()
            sleep(random.uniform(2.0, 3.2))
            break
        except Exception as ex:
            print("error " + str(ex))
            print('cmt error, sleep 5s and try again')

    if like_cmt:
        print("like_cmt")
        try:
            sleep(random.uniform(2.5, 4.2))
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//ytd-toggle-button-renderer[@id="like-button"]//button'))).click()
        except:
            print('like_cmt error')
            return False

    if rep_cmt:
        print('rep_cmt')
        try:
            sleep(random.uniform(1.5, 2.2))
            browser.execute_script("window.scrollTo(0, window.scrollY + " + str(random.randint(100, 200)) + ")")
            sleep(random.uniform(2.5, 4.2))
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="reply-button-end"]//button'))).click()
            sleep(random.uniform(1.5, 2.2))

            el_input = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//ytd-comment-renderer//div[@id="contenteditable-root"]')))
            el_input.click()
            sleep(random.uniform(0.2, 0.8))
            linkFile = dir_path + fr"\input\cmt-tool-pre.txt"
            with open(linkFile, encoding="utf-8") as f:
                text = f.readlines()
                b = len(text)
                while True:
                    a = text[random.randint(0, b - 1)].strip()
                    if len(a) > 0:
                        break
            print("rep_cmt value: " + str(a))
            el_input.send_keys(a)
            sleep(random.uniform(1.2, 2.2))
            click_object = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//ytd-comment-renderer//ytd-button-renderer[@id="submit-button"]')))
            click_object.click()
            sleep(random.uniform(2.0, 3.2))
        except:
            print('rep_cmt error')
            return False

    return True


def close_browser(browser):
    print("close_browser")
    for i in range(2):
        try:
            sleep(0.5)
            browser.close()
            print("close ")
        except Exception as ex:
            print("close again" + str(i))
            sleep(0.5)


def check_login_ytb(browser):
    print("check_login_ytb")
    if "youtube.com" not in str(browser.current_url):
        browser.get("https://www.youtube.com/")
        sleep(4)
    try:
        avatar = browser.find_element(By.ID, 'avatar-btn')
        print("dda login " + str(avatar.text))
        return True
    except:
        print("chua login")
        return False


def get_account_first(name_sheet, name_tab):
    print("get_account_first")
    sleep(random.uniform(0.2, 2.5))
    index_error = 0
    while True:
        try:
            sa = gspread.service_account(filename="./gspread/acquired-sunup-382409-0952606e62c1.json")
            sh = sa.open(name_sheet)
            wks = sh.worksheet(name_tab)
            index_record = 1
            for sock_item in wks.get_all_records():
                index_record = index_record + 1
                status = sock_item.get("Status")
                if "GOOD" in status or "FAIL Login" in status or "LOADING" in status:
                    continue
                wks.update("G" + str(index_record), "LOADING")
                return index_record, sock_item
            return None, None
        except Exception as ex:
            print("ex " + str(ex))
            index_error = index_error + 1
            print("load tryagin " + str(index_error * 5))
            sleep(index_error * 5)
            pass


def get_update_close(name_sheet, name_tab):
    print("get_update_close")
    index_error = 0
    sa = gspread.service_account(filename="./gspread/acquired-sunup-382409-0952606e62c1.json")
    sh = sa.open(name_sheet)
    wks = sh.worksheet(name_tab)
    while True:
        if index_error > 10:
            return False
        try:
            index_record = 1
            for sock_item in wks.get_all_records():
                index_record = index_record + 1
                status = sock_item.get("Status")
                if "LOADING" in status:
                    wks.update("G" + str(index_record), "")
                    sleep(random.uniform(0.2, 0.5))
            return True
        except Exception as ex:
            print("ex " + str(ex))
            index_error = index_error + 1
            print("load try again " + str(index_error * 5))
            sleep(index_error * 0.1)
            pass
