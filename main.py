import datetime
import json
import threading
from tkinter import *
from tkinter import messagebox

from common import get_update_close
from startup import start_tool_view


def main():
    window = Tk()
    window.title("Tool view ytb")
    window.geometry("750x170")
    text_button_start = StringVar()
    text_button_start.set("Start")

    label_name_sheet = Label(window, text="Name sheet:  ", font=("Arial", 13))
    label_name_sheet.grid(column=0, row=1)
    label_name_sheet.grid(padx=20, pady=10)
    txt_name_sheet = Entry(window, font=("Arial", 13), width=50)
    txt_name_sheet.grid(column=1, row=1, columnspan=2)

    label_profile_path = Label(window, text="Profile path:  ", font=("Arial", 13))
    label_profile_path.grid(column=0, row=2)
    label_profile_path.grid(padx=20, pady=10)
    txt_profile_path = Entry(window, font=("Arial", 13), width=50)
    txt_profile_path.grid(column=1, row=2, columnspan=2)

    # label_comment_times = Label(window, text="Comment times:", font=("Arial", 13))
    # label_comment_times.grid(column=0, row=3)
    # label_comment_times.grid(padx=20, pady=10)
    # txt_comment_times = Entry(window, font=("Arial", 13), width=50)
    # txt_comment_times.grid(column=1, row=3, columnspan=2)
    #
    # label_like_times = Label(window, text="Like times:", font=("Arial", 13))
    # label_like_times.grid(column=0, row=4)
    # label_like_times.grid(padx=20, pady=10)
    # txt_like_times = Entry(window, font=("Arial", 13), width=50)
    # txt_like_times.grid(column=1, row=4, columnspan=2)
    #
    # label_rep_cmt_times = Label(window, text="Rep comment times:", font=("Arial", 13))
    # label_rep_cmt_times.grid(column=0, row=5)
    # label_rep_cmt_times.grid(padx=20, pady=10)
    # txt_rep_cmt_times = Entry(window, font=("Arial", 13), width=50)
    # txt_rep_cmt_times.grid(column=1, row=5, columnspan=2)

    # label_thread_count = Label(window, text="Count thread:", font=("Arial", 13))
    # label_thread_count.grid(column=0, row=12)
    # label_thread_count.grid(padx=20, pady=10)
    # txt_thread_count = Entry(window, font=("Arial", 13), width=50)
    # txt_thread_count.grid(column=1, row=12, columnspan=2)
    #
    # label_thread_count = Label(window, text="Count thread:", font=("Arial", 13))
    # label_thread_count.grid(column=0, row=12)
    # label_thread_count.grid(padx=20, pady=10)
    # txt_thread_count = Entry(window, font=("Arial", 13), width=50)
    # txt_thread_count.grid(column=1, row=12, columnspan=2)

    # cb_channel = BooleanVar()
    # Checkbutton(window, text="Channel", variable=cb_channel, padx=10, pady=10, font=("Arial", 13)).grid(column=2,
    #                                                                                                     row=15)
    # label_screen_size = Label(window, text="Screen size:", font=("Arial", 13))
    # label_screen_size.grid(column=0, row=16)
    # label_screen_size.grid(padx=20, pady=10)
    # txt_screen_size = Entry(window, font=("Arial", 13), width=50)
    # txt_screen_size.grid(column=1, row=16, columnspan=2)

    # class thread(threading.Thread):
    #     def __init__(self, name_sheet, screen_size, thread_count, group_gpm):
    #         super().__init__()
    #         self.thread_count = thread_count
    #         self.name_sheet = name_sheet
    #         self.screen_size = screen_size
    #         self.group_gpm = group_gpm
    #
    #     def run(self):
    #         print("run")
    #         begin_tool_view(self.name_sheet, self.screen_size, self.thread_count, self.group_gpm)

    def start():
        print("start tool")
        name_sheet = txt_name_sheet.get()
        profile_path = txt_profile_path.get()
        # comment_times = txt_comment_times.get()
        # like_times = txt_like_times.get()
        # rep_cmt_times = txt_rep_cmt_times.get()

        if not name_sheet or name_sheet is None or \
                not profile_path or profile_path is None:
                # not comment_times or comment_times is None or \
                # not like_times or like_times is None or \
                # not rep_cmt_times or rep_cmt_times is None:
            messagebox.showerror("Error", "Input is empty!!")
        else:
            start_tool_view(name_sheet, profile_path)


    def save():
        print("save")
        name_sheet = txt_name_sheet.get()
        profile_path = txt_profile_path.get()
        # comment_times = txt_comment_times.get()
        # like_times = txt_like_times.get()
        # rep_cmt_times = txt_rep_cmt_times.get()
        if not name_sheet or name_sheet is None or \
                not profile_path or profile_path is None:
                # not comment_times or comment_times is None or \
                # not like_times or like_times is None or \
                # not rep_cmt_times or rep_cmt_times is None:
            messagebox.showerror("Error", "Input is empty!!")
        else:
            data = {
                "name_sheet": name_sheet,
                "profile_path": profile_path
                # "comment_times": int(comment_times),
                # "like_times": int(like_times),
                # "rep_cmt_times": int(rep_cmt_times)
            }
            with open("cache.json", "w") as outfile:
                json.dump(data, outfile)
            messagebox.showinfo("Info", "Save Success!!")

    # handle close
    def on_closing():
        name_sheet = txt_name_sheet.get()
        try:
            if name_sheet is not None or name_sheet:
                get_update_close(name_sheet, "accounts")
        except Exception as ex:
            print("update " + str(ex))
            pass
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    import os.path
    file_exists = os.path.exists('cache.json')
    if file_exists:
        cache = open('cache.json')
        # a dictionary
        data_cache = json.load(cache)
        txt_name_sheet.delete(0, END)
        txt_name_sheet.insert(0, data_cache['name_sheet'])
        txt_profile_path.delete(0, END)
        txt_profile_path.insert(0, data_cache['profile_path'])
        # txt_comment_times.delete(0, END)
        # txt_comment_times.insert(0, data_cache['comment_times'])
        # txt_like_times.delete(0, END)
        # txt_like_times.insert(0, data_cache['like_times'])
        # txt_rep_cmt_times.delete(0, END)
        # txt_rep_cmt_times.insert(0, data_cache['rep_cmt_times'])

    bt_start = Button(window, textvariable=text_button_start, font=("Arial", 19), width=15, bg="green", command=start)
    bt_start.grid(column=0, row=19)
    bt_start.grid(padx=10, pady=10)

    bt_save = Button(window, text="Save", font=("Arial", 19), width=15, bg="yellow", command=save)
    bt_save.grid(column=2, row=19, sticky=E)
    bt_save.grid(padx=10, pady=10)
    window.mainloop()


if __name__ == '__main__':
    main()
