import os
import random
from time import sleep

import gspread
import undetected_chromedriver as UC
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from login.gmail import login_email
from feed_ytb import search_ytb, find_video, find_channel
from common_element import input_type_char
from common import close_browser, get_account_first, check_login_ytb, \
    get_profile_id, open_video_link, cmt_video, get_update_close, get_random_string

name_sheet = ""
name_tab = ""
wks = None


def start_sheet(name_sheet, name_tab):
    sa = gspread.service_account(filename="./gspread/acquired-sunup-382409-0952606e62c1.json")
    sh = sa.open(name_sheet)
    wks = sh.worksheet(name_tab)
    return wks


def get_link_videos(name_sheet):
    print("get_link_video")
    wks_links = start_sheet(name_sheet, "links")
    index_record = 1
    list_info_video = []
    for sock_item in wks_links.get_all_records():
        index_record = index_record + 1
        video_link = sock_item.get("Videos Link")
        comment_times = sock_item.get("Comment times")
        like_times = sock_item.get("Like times")
        rep_cmt_times = sock_item.get("Rep cmt times")
        info_video = {
            "video_link": video_link,
            "comment_times": comment_times,
            "like_times": like_times,
            "rep_cmt_times": rep_cmt_times
        }
        list_info_video.append(info_video)
    return list_info_video


def start_tool_view(name_sheet, profile_path):
    print("start")
    global wks
    wks = start_sheet(name_sheet, "accounts")

    # channel_name = "Huta Regame"
    # channel_id = '@HungTamReview'
    # group = "ytb"
    # name_tab = "accounts"
    # key_search = "Những bài hát hay nhất của Đen Vâu 2021"
    # search_id = "Yxnu2gdCbms"

    list_info_video_view = get_link_videos(name_sheet)

    while True:
        index_profile, account = get_account_first(name_sheet, "accounts")
        if account is not None:
            profile_id = account.get("Profile IDs")
            email = account.get("Email")
            password = account.get("Password")
            email_restore = account.get("Email Recover")
            status_account = account.get("Status Account")
            try:
                if len(profile_id) < 2:
                    """Nếu trên sheets chưa có đường dẫn Profile thì tạo Profile Chrome mới"""
                    options = ChromeOptions()
                    profile_id = get_random_string(10)  # Tạo profile ngẫu nhiên
                    print('new profile: ' + profile_id)
                    options.add_argument("--user-data-dir=" + profile_path + "\\" + profile_id)
                    options.add_argument('--force-dark-mode')
                    # options.add_argument('--blink-settings=imagesEnabled=false')
                    browser = UC.Chrome(options=options)
                    # browser.implicitly_wait(20)
                    browser.set_page_load_timeout(30)
                    # profile_id = get_profile_id(browser)
                    wks.update("D" + str(index_profile), profile_id)

                else:
                    """ Nếu có đường dẫn Profile rồi thì vào Profile đấy """
                    options = ChromeOptions()
                    options.add_argument("--user-data-dir=" + profile_path + "\\" + profile_id)
                    options.add_argument('--force-dark-mode')
                    # options.add_argument('--blink-settings=imagesEnabled=false')
                    browser = UC.Chrome(options=options)
                    # browser.implicitly_wait(20)
                    browser.set_page_load_timeout(30)

                if browser is None:
                    print("browser error")
                    sleep(5)
                    close_browser(browser)
                    continue

                if not check_login_ytb(browser):
                    # Login gmail
                    if not login_email(browser, email, password, email_restore):
                        wks.update("F" + str(index_profile), "FAIL Login")
                        close_browser(browser)
                        continue
                    wks.update("F" + str(index_profile), "Login Success")

                elif len(status_account) == 0:
                    wks.update("F" + str(index_profile), "Login Success")

                for info_video_view in list_info_video_view:
                    video_link = info_video_view.get("video_link")
                    comment_times: int = info_video_view.get("comment_times")
                    like_times: int = info_video_view.get("like_times")
                    rep_cmt_times: int = info_video_view.get("rep_cmt_times")

                    if (comment_times < rep_cmt_times) or (comment_times < like_times):
                        print('comment_times < like_times/rep_cmt_times => Skip this link')
                        continue

                    # find_video(browser, video_link)
                    open_video_link(browser, video_link)
                    index_like = 1
                    index_rep_cmt = 1
                    for index_cmt in range(comment_times):
                        print('comment lan ' + str(index_cmt + 1))

                        if index_like <= like_times:
                            if index_rep_cmt <= rep_cmt_times:
                                cmt_video(browser, True, True)
                            else:
                                cmt_video(browser, True, False)
                        else:
                            if index_rep_cmt <= rep_cmt_times:
                                cmt_video(browser, False, True)
                            else:
                                cmt_video(browser, False, False)

                        index_like = index_like + 1
                        index_rep_cmt = index_rep_cmt + 1
                close_browser(browser)
                sleep(1)
                wks.update("G" + str(index_profile), "GOOD")
            except Exception as e:
                print("error : " + str(e))
                wks.update("G" + str(index_profile), "FAIL")
        else:
            get_update_close(name_sheet, "accounts")
            break


def begin_tool_view(name_sheet, screen_size, thread_count, group):
    print("begin")
    name_tab = "accounts"
    global wks
    wks = start_sheet(name_sheet, name_tab)
    # max_page = 0
    # data = get_data_origin(name_sheet, name_tab)
    # chunks = np.array_split(data, int(thread_count))
    threads = []
    # height = 980 - 60
    # width = 1920
    # height = int(str(screen_size).split("x")[1]) - 60
    # width = int(str(screen_size).split("x")[0])
    # line = round(thread_count / 2)
    # column_browser = round(width / 512)
    # row_browser = round(height / 345)

    # if line > 0:
    # width_window = width / column_browser
    # height_window = height / row_browser
    # else:
    #     width_window = width / 2
    #     height_window = height

    # y = 0
    # index_window = -1
    # for l in range(thread_count):
    #     index_window = index_window + 1
    #     if l % column_browser == 0 and l > 0 and line > 1:
    #         y = y + height_window
    #         index_window = 0
    #     x = index_window * (width_window + 0)
    #     threads += [
    #         threading.Thread(target=start_tool_view,
    #                          args=(l, name_sheet, name_tab, width_window, height_window, y, x))]
    # for t in threads:
    #     sleep(3)
    #     t.start()
    #
    # for t in threads:
    #     t.join()

    data = get_account_first(name_sheet, name_tab)
    if data != 0:
        print("try again " + str(data))
        begin_tool_view(name_sheet, screen_size, thread_count, group)
    else:
        sleep(50)
