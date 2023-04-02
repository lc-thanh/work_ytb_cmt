import os
import random
from time import sleep

from undetected_chromedriver import ChromeOptions

import gspread
import undetected_chromedriver as UC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from login.gmail import login_email
from common_element import input_type_char
from common import random_click_video, skip_ads, cmt_video
from common import *

options = ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\Admin\Desktop\tool_ytb\tool_ytb\profile")
options.add_argument('--force-dark-mode')
options.add_argument('--blink-settings=imagesEnabled=false')
browser = UC.Chrome(options=options)
browser.implicitly_wait(20)
browser.set_page_load_timeout(30)
sleep(5)

# Lấy ID Chrome
get_profile_id(browser)

# Đăng nhập Gmail
# login_email(browser, "Emiliocap502@nonconduct.org", "jfHKDBec", "pappp@gmail.com")
sleep(1)
browser.get('https://youtube.com')

sleep(100)
