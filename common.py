import os
import random
import string
from time import sleep
from tkinter import messagebox

import gspread
import requests
from selenium.webdriver import Keys
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


def get_profile_id(browser):
    browser.get("chrome://version/")
    sleep(1)
    chrome_profile_path = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//td[@id="profile_path"]')))
    path_split = chrome_profile_path.text.split("\\")
    profile_id = path_split[len(path_split) - 2]
    return str(profile_id)


def open_video_link(browser, video_link):
    print('opening ' + video_link)
    while True:
        try:
            browser.get(video_link)
            return
        except Exception as ex:
            print("open_video_link error: " + ex)
            sleep(2)


def random_click_video(browser, channel_id, is_scroll=True):
    """
    Phương thức tự động nhấn vào bất kỳ 1 video của kênh có ID là 'channel_id' \n
    LƯU Ý: ID của kênh phải có '@'

    :param browser: Biến trình duyệt
    :param channel_id: ID của kênh
    :param is_scroll: Tự động cuộn trang đến chỗ video, giá trị mặc định là True
    :return: True nếu chạy xong, False nếu gặp lỗi
    """
    print('random_click_video')
    index_error = 0
    while True:
        if index_error > 4:
            return False
        try:
            videos_xpath = f'//a[@href="/{channel_id}"]/../../../ytd-thumbnail/a[@id="thumbnail"]'
            video_list = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, str(videos_xpath))))
            random_video = video_list[random.randint(0, len(video_list) - 1)]
            if is_scroll:
                browser.execute_script("arguments[0].scrollIntoView();", random_video)
                sleep(random.uniform(1, 2.5))
            random_video.click()
            sleep(random.uniform(2, 3.5))
            return True
        except Exception as error:
            print(error)
            index_error = index_error + 1
            print("not click sleep 10s")
            html = browser.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.END)
            sleep(10)


def skip_ads(browser):
    """
    Phương thức tự động skip quảng cáo Youtube

    :param browser: Biến trình duyệt
    :return: None
    """
    print('skip_ads')
    error = 1
    ads = 1
    sleep(6)
    while True:
        if error > 2:
            return
        try:
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'ytp-ad-skip-button-container'))).click()
            print(f'Ad {ads} skipped')
            ads = ads + 1
            sleep(random.uniform(2, 3.5))
        except:
            print('no ads found, sleep 5s')
            error = error + 1
            sleep(5)


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
            # sleep(random.uniform(2.5, 3.5))
            # html = browser.find_element(By.TAG_NAME, 'html')
            # html.send_keys(Keys.HOME)
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
            # list_like = WebDriverWait(browser, 10).until(
            #     EC.presence_of_all_elements_located((By.XPATH, '//ytd-toggle-button-renderer[@id="like-button"]')))
            sleep(random.uniform(2.5, 4.2))
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//ytd-toggle-button-renderer[@id="like-button"]//button'))).click()
            # if len(list_like) > 2:
            #     if len(list_like) > 5:
            #         like_max = random.randint(0, 5)
            #     else:
            #         like_max = random.randint(0, len(list_like) - 2)
            #     for loop_like_cmt in range(like_max):
            #         view_like_cmt = list_like[random.randint(0, len(list_like) - 1)]
            #         browser.execute_script("arguments[0].scrollIntoView();", view_like_cmt)
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


def view_video(browser, time_views, rate_time_start):
    print("view_video")
    sleep(random.randint(5, 8))
    duration = browser.execute_script('return document.getElementsByTagName("video")[0].duration;')
    print("duration " + str(duration))

    time_start_split = str(rate_time_start).split('-')
    rate_time_tua = random.randint(int(time_start_split[0]), int(time_start_split[1]))
    print("rate_time_tua " + str(rate_time_tua))
    time_tua = int(duration) * rate_time_tua / 100
    print("time_tua " + str(time_tua))

    time_view_split = str(time_views).split('-')
    rate_time_view = random.randint(int(time_view_split[0]), int(time_view_split[1]))
    print("rate_time_view " + str(rate_time_view))
    time_view = int(duration) * rate_time_view / 100
    time_view = time_view - 10
    print("time_view " + str(time_view))
    try:
        print("choose chat luong")
        qua = ["144p", "240p", "360p", "480p", "144p", "240p", "360p", "480p", "720p"]
        e = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[@title='Settings']")))
        browser.execute_script("arguments[0].click();", e)
        sleep(2)
        e = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Quality')]")))
        browser.execute_script("arguments[0].click();", e)
        sleep(2)
        e = WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, f"//span[contains(string(),'{qua[random.randint(0, 8)]}')]")))
        browser.execute_script("arguments[0].click();", e)
    except:
        sleep(0.2)
    try:
        sleep(5)
        print("skip ad")
        if EC.presence_of_element_located(
                (By.XPATH, "//button[@class='ytp-ad-skip-button ytp-button']")):
            skipAd = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@class='ytp-ad-skip-button ytp-button']")))
            sleep(5)
            skipAd.click()
    except Exception as ex:
        print("boqua " + str(ex))
        sleep(0.5)
    # max_count = random.randint(1, 2)
    # for count in range(max_count):
    try:
        # time_tua = random.randint(10, 40)
        browser.execute_script('document.getElementsByTagName("video")[0].currentTime += ' + str(time_tua) + ';')
        sleep(random.uniform(5, 9))
    except Exception as ex:
        sleep(0.5)
    # like
    if random.choice([True]):
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                             "//ytd-menu-renderer[@class='style-scope "
                                                                             "ytd-watch-metadata']//div["
                                                                             "@id='segmented-like-button']"))).click()
            # thongbao.insert(INSERT, f'Mail {i}: Đã like\n')
        except Exception as ex:
            print("like " + str(ex))
            sleep(0.5)
        sleep(3)

    ##### Subscribe
    if random.choice([False, True]):
        print("Subscribe")
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='owner']//div[@id='subscribe-button']"))).click()
            # thongbao.insert(INSERT, f'Mail {i}: Đã subscribe\n')
            sleep(1)
            html = browser.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.ESCAPE)
        except:
            sleep(0.5)
    ########### cmt
    if random.choice([False, True]):
        print("cmt")
        try:
            sleep(random.uniform(1.5, 2.2))
            html = browser.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.HOME)
            sleep(random.uniform(1.2, 2.2))
            WebDriverWait(browser, 5).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer"))).click()
            sleep(random.uniform(1.2, 2.2))
            el_input = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='contenteditable-root']")))
            el_input.click()
            sleep(random.uniform(0.2, 0.8))
            linkfile = dir_path + fr"\input\cmt.txt"
            with open(linkfile, encoding="utf-8") as f:
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
        except Exception as ex:
            print("error " + str(ex))
    # like cmt
    if random.choice([False, True]):
        print("like cmt")
        try:
            list_like = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//ytd-toggle-button-renderer[@id="like-button"]')))
            if len(list_like) > 2:
                if len(list_like) > 5:
                    like_max = random.randint(0, 5)
                else:
                    like_max = random.randint(0, len(list_like) - 2)
                for loop_like_cmt in range(like_max):
                    view_like_cmt = list_like[random.randint(0, len(list_like) - 1)]
                    browser.execute_script("arguments[0].scrollIntoView();", view_like_cmt)
        except:
            pass
    while time_view > 0:
        time_sleep = random.randint(10, 30)
        if time_sleep > time_view:
            sleep(time_view)
            break
        else:
            time_view = time_view - time_sleep
            print("view " + str(time_sleep))
            sleep(time_sleep)
            value_scroll = random.randint(150, 220)
            if random.choice([True, False]):
                browser.execute_script("window.scrollTo(0, window.scrollY -" + str(value_scroll) + ")")
                sleep(random.randint(2, 6))
            else:
                browser.execute_script("window.scrollTo(0, window.scrollY + " + str(value_scroll) + ")")
                sleep(random.randint(2, 6))
    print("view done")


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


def get_data_origin(name_sheet, name_tab):
    sa = gspread.service_account(filename="./gspread/acquired-sunup-382409-0952606e62c1.json")
    sh = sa.open(name_sheet)
    wks = sh.worksheet(name_tab)
    index_record = 1
    list_data = []
    for sock_item in wks.get_all_records():
        index_record = index_record + 1
        if len(str(sock_item.get("ID"))) < 2:
            data = {
                "index": index_record,
                "id": "",
                "password": "",
                "2fa": "",
                "profileIDs": "",
                "status": "",
                "list_cookies": ""
            }
            list_data.append(data)
            continue
        data = {
            "index": index_record,
            "id": sock_item.get("ID"),
            "password": sock_item.get("Password"),
            "2fa": sock_item.get("2FA"),
            "profileIDs": sock_item.get("Profile ID"),
            "status": sock_item.get("Status"),
            "api": sock_item.get("API proxy"),
            "list_cookies": sock_item.get("Cookie")
        }
        list_data.append(data)
    return list_data


def set_zoom(driver, zoom):
    # current_tab_index = driver.window_handles.index(driver.current_window_handle)
    # driver.execute_script("window.open('');")
    # driver.switch_to.window(driver.window_handles[-1])
    sleep(2)
    driver.get('chrome://settings/')
    # print(current_tab_index)
    sleep(2)

    def expand_shadow_element(element):
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root

    # process to set zoom level of browser
    root1 = driver.find_element(By.XPATH, "*//settings-ui")
    shadow_root1 = expand_shadow_element(root1)
    sleep(1)
    container = shadow_root1.find_element(By.ID, "container")

    root2 = container.find_element(By.CSS_SELECTOR, "settings-main")
    shadow_root2 = expand_shadow_element(root2)
    sleep(1)
    root3 = shadow_root2.ZAfind_element(By.CSS_SELECTOR, "settings-basic-page")

    shadow_root3 = expand_shadow_element(root3)
    basic_page = shadow_root3.find_element(By.ID, "basicPage")

    settings_section = basic_page.find_element(By.XPATH, ".//settings-section[@section='appearance']")

    root4 = settings_section.find_element(By.CSS_SELECTOR, "settings-appearance-page")
    shadow_root4 = expand_shadow_element(root4)
    sleep(1)
    settings_animated_pages = shadow_root4.find_element(By.ID, "pages")
    zoom_select = settings_animated_pages.find_element(By.ID, "zoomLevel")
    zoom_select.find_element(By.CSS_SELECTOR, f"option[value='{zoom}']").click()
    sleep(1)
    # driver.close()
    # driver.switch_to.window(driver.window_handles[current_tab_index])
    driver.refresh()


def random_file(path_folder):
    files = os.listdir(path_folder)
    if len(files) == 1:
        index_video = 0
    elif len(files) > 0:
        index_video = random.randint(0, len(files) - 1)
    else:
        messagebox.showerror("Info", "Folder avatar empty!!,")
        sleep(5)
        return
    path_video = path_folder + "\\" + files[index_video]
    print("path video " + str(path_video))
    return path_video


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


def open_link(browser):
    print("open_link")
    list_link = open("input/list_link_web.txt", 'r').readlines()
    print("len " + str(len(list_link)))
    len_list_link = len(list_link) * 5
    if len_list_link == 0:
        return
    for link in list_link:
        print(link)
        browser.execute_script("window.open('" + link.strip() + "');")
        sleep(0.2)
    print("sleep wait 2p")
    sleep(len_list_link)
    while True:
        browser.switch_to.window(browser.window_handles[0])
        sleep(2)
        scroll_random(browser, random.randint(4, 8))
        if len(browser.window_handles) == 1:
            break
        sleep(1)
        browser.close()
        sleep(1)
