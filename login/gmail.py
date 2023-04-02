import random
from time import sleep

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common_element import input_type_char


def input_email_restore(browser, email_restore):
    print("input_email_restore")
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/ul/li[3]'))).click()
        sleep(3)
        input_email = browser.find_element(By.XPATH, '//input[@type="email"]')
        input_email.click()
        input_email.send_keys(email_restore)
        sleep(2)
        input_email.send_keys(Keys.ENTER)
        sleep(4)
    except:
        print("not require")


def login_email(browser, email, password, email_restore):
    print("login_email")
    index_error = 0
    while True:
        try:
            browser.get("https://accounts.google.com/signin/v2/identifier")
            sleep(random.uniform(2.5, 3.5))
            check_success = browser.current_url
            if "myaccount.google.com" in check_success or "gds.google.com" in check_success:
                return True
            print(email)
            print(password)
            is_enter = random.choice([False, True])
            input_type_char(browser, '//input[@type="email"]', str(email), is_enter=is_enter)
            if not is_enter:
                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='identifierNext']"))).click()
            sleep(random.uniform(2.8, 3.5))
            is_enter = random.choice([False, True])
            input_type_char(browser, '//input[@type="password"]', str(password), is_enter=is_enter)
            if not is_enter:
                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='passwordNext']"))).click()
            sleep(random.uniform(4.5, 5.5))
            input_email_restore(browser, email_restore)
            try:
                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='confirm']"))).click()
                sleep(3)
            except:
                sleep(0.5)
            check_success = browser.current_url
            if "myaccount.google.com" in check_success or "gds.google.com" in check_success:
                return True
            return False
        except Exception as ex:
            print("error " + str(ex))
            index_error = index_error + 1
            try:
                input_email = browser.find_element(By.XPATH, '//input[@type="email"]')
                input_email.click()
                sleep(random.uniform(1.5, 2.5))
                input_email.send_keys("tes" + email)
                input_email.send_keys(Keys.ENTER)
                sleep(2)
            except:
                print("error")
        if index_error > 3:
            return False
