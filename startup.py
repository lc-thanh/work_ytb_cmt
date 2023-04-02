
from time import sleep

import gspread
import undetected_chromedriver as UC
from undetected_chromedriver import ChromeOptions

from login.gmail import login_email
from common import close_browser, get_account_first, check_login_ytb, cmt_video, get_update_close, get_random_string

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
    list_info_video_view = get_link_videos(name_sheet)
    index_loop = 0

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
                    comment_times =int(info_video_view.get("comment_times"))
                    like_times = int(info_video_view.get("like_times"))
                    rep_cmt_times = int(info_video_view.get("rep_cmt_times"))

                    if (comment_times < rep_cmt_times) or (comment_times < like_times):
                        print('comment_times < like_times/rep_cmt_times => Skip this link')
                        continue

                    # find_video(browser, video_link)
                    browser.get(video_link)
                    sleep(4)
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
            index_loop = index_loop + 1
            get_update_close(name_sheet, "accounts")
            if index_loop > 2:
                break

