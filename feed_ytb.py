import json
import random
import threading
from time import sleep

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common import scroll_random, view_video
from common_element import input_type_char


def ytb_search(browser, search_keyword):
    print('Search Youtube: ' + search_keyword)
    try:
        sleep(random.uniform(3.5, 4.5))
        is_enter = random.choice([True, False])
        input_type_char(browser, '//input[@id="search"]', str(search_keyword.lower()), is_enter=is_enter)
        if not is_enter:
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@id="search-icon-legacy"]'))).click()
        sleep(random.uniform(2.5, 3.5))
    except Exception as ex:
        print('Youtube search error: ' + ex)


def search_ytb(browser, key_search):
    print("search_ytb")
    browser.get("https://www.youtube.com/")
    sleep(random.uniform(3, 5))
    input_type_char(browser, '//input[@id="search"]', str(key_search))
    sleep(random.uniform(2, 4))
    scroll_random(browser, random.randint(4, 8))


def find_channel(browser, channel_id, time_view, rate_time_start):
    print("search_channel")
    try:
        is_find_channel = False
        index_find = 0
        while True:
            index_find = index_find + 1
            if index_find > 10:
                return False
            list_channel = browser.find_elements(By.XPATH, '//a[@id="main-link"]')
            for channel in list_channel:
                if channel_id in str(channel.get_attribute("href")):
                    scroll_random(browser, random.randint(5, 10))
                    sleep(random.uniform(1, 2))
                    browser.execute_script("arguments[0].scrollIntoView();", channel)
                    sleep(random.uniform(1, 2))
                    value_scroll = random.randint(190, 250)
                    browser.execute_script("window.scrollTo(0, window.scrollY - " + str(value_scroll) + ")")
                    sleep(random.uniform(1, 2))
                    channel.click()
                    is_find_channel = True
                    break
            if is_find_channel:
                break
            else:
                for index in range(5):
                    value_scroll = random.randint(160, 220)
                    browser.execute_script("window.scrollTo(0, window.scrollY +" + str(value_scroll) + ")")
                    sleep(1)
        sleep(random.uniform(2, 4))
        scroll_random(browser, random.randint(5, 10))
        browser.get(browser.current_url + "/videos")
        sleep(random.randint(2, 4))
        scroll_random(browser, random.randint(4, 8))
        index_media = 0
        index_media_max = random.randint(1, 3)
        print("view video in channel")
        while True:
            index_media = index_media + 1
            if index_media > index_media_max:
                break
            list_media = browser.find_elements(By.TAG_NAME, 'ytd-rich-grid-media')
            media = list_media[random.randint(0, len(list_media) - 1)]
            browser.execute_script("arguments[0].scrollIntoView();", media)
            sleep(random.uniform(1, 3))
            browser.execute_script("window.scrollTo(0, window.scrollY - 200)")
            sleep(random.uniform(0.5, 1.5))
            media.click()
            sleep(random.uniform(2, 4))
            view_video(browser, time_view, rate_time_start)
            if random.choice([False, True]) and random.choice([False, True]):
                find_video_random_in_list_view(browser, 0, 1)
                browser.execute_script("window.history.go(-1)")
                sleep(random.uniform(0.5, 1.5))
            browser.execute_script("window.history.go(-1)")
            sleep(1)
            if len(list_media) < 4:
                break
    except Exception as ex:
        print("error " + str(ex))
        sleep(5)


def find_video(browser, video_id, time_view, rate_time_start):
    print("find_video")
    linkvideo = "https://www.youtube.com/watch?v=" + str(video_id)
    try:
        scroll_random(browser, random.randint(4, 8))
        for q in range(3):
            if q < 2:
                try:
                    sleep(1)
                    view_video_el = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                        (By.XPATH, f"//*[@href = '/watch?v={video_id}']")))
                    browser.execute_script("arguments[0].scrollIntoView();", view_video_el)
                    sleep(random.uniform(0.5, 2))
                    view_video_el.click()
                    break
                except:
                    html = browser.find_element(By.TAG_NAME, 'html')
                    html.send_keys(Keys.END)
            else:
                browser.get(linkvideo)
        sleep(random.uniform(2.5, 4.5))
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@class='ytp-large-play-button ytp-button']"))).click()
        except:
            sleep(0.5)
        # view_video(browser, time_view, rate_time_start)
        # find_video_random_in_list_view(browser, 0, random.randint(1, 2))
    except Exception as ex:
        print("ex " + str(ex))
        sleep(100)


def find_video_random_in_list_view(browser, loop, max_loop):
    print("find_video_random_in_list_view")
    if loop > max_loop - 1:
        return
    sleep(3)
    scroll_random(browser, random.randint(4, 8))
    list_audio = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located(
        (By.TAG_NAME, 'ytd-compact-video-renderer')))
    list_video_display = []
    index_video_display = -1
    for item_view in list_audio:
        index_video_display = index_video_display + 1
        if item_view.is_displayed():
            list_video_display.append(index_video_display)
    if len(list_video_display) > 2:
        item_view = list_audio[random.choice(list_video_display)]
        browser.execute_script("arguments[0].scrollIntoView();", item_view)
        sleep(random.uniform(0.2, 0.8))
        browser.execute_script("window.scrollTo(0, window.scrollY - " + str(random.randint(200, 300)) + ")")
        sleep(random.uniform(0.5, 1))
        item_view.click()
        sleep(random.uniform(5, 10))
        find_video_random_in_list_view(browser, loop + 1, max_loop)


def random_scroll_and_watch_video_home(browser, list_key_propose):
    print('start functions random_scroll_and_watch_video')
    time_watch = random.randint(15, 60)
    time_view = "0-20"
    time_start = "20-40"

    browser.get("https://www.youtube.com/")
    sleep(random.uniform(2, 4))
    scroll_random(browser, random.randint(5, 10))
    time_watch = time_watch - 6
    try:
        for index in range(random.randint(0, 1)):
            videos = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//div[@id="dismissible"]')))
            print('len = ' + str(len(videos)))
            index_video = random.randint(0, len(videos) - 5)
            print('play index ' + str(index_video))
            browser.execute_script("arguments[0].scrollIntoView();", videos[index_video])
            sleep(random.uniform(0.5, 1))
            browser.execute_script("window.scrollTo(0, window.scrollY - 200)")
            sleep(1)
            videos[index_video].click()
            sleep(random.uniform(2, 3.5))
            print('time watch = ' + str(time_watch))
            sleep(int(time_watch / 2))
            scroll_random(browser, random.randint(2, 5))
            sleep(int(time_watch / 2))
            if len(browser.current_url) > 28:
                browser.execute_script("window.history.go(-1)")
    except Exception as ex:
        print("error " + str(ex))
        pass
    print("de xuat ")
    print("len " + str(len(list_key_propose)))
    index_video = 0
    for video_id in list_key_propose:
        video_id = str(video_id).strip()
        print(video_id)
        index_video = index_video + 1
        scroll_random(browser, random.randint(0, 2))
        try:
            sleep(1)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, f"//*[@href = '/watch?v={video_id}']"))).click()
        except Exception as ex:
            print("error " + str(ex))
            continue
        sleep(5)
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@class='ytp-large-play-button ytp-button']"))).click()
        except:
            sleep(0.5)
        view_video(browser, time_view, time_start)
        if len(browser.current_url) > 28:
            browser.get("https://www.youtube.com/")
            sleep(random.uniform(2.2, 3.3))
