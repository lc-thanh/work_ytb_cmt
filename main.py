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

    class thread(threading.Thread):
        def __init__(self, name_sheet, profile_path):
            super().__init__()
            self.profile_path = profile_path
            self.name_sheet = name_sheet

        def run(self):
            print("run")
            start_tool_view(self.name_sheet, self.profile_path)

    def start():
        print("start tool")
        name_sheet = txt_name_sheet.get()
        profile_path = txt_profile_path.get()

        if not name_sheet or name_sheet is None or \
                not profile_path or profile_path is None:
            # not rep_cmt_times or rep_cmt_times is None:
            messagebox.showerror("Error", "Input is empty!!")
        else:
            thread(name_sheet, profile_path).start()

    def save():
        print("save")
        name_sheet = txt_name_sheet.get()
        profile_path = txt_profile_path.get()
        if not name_sheet or name_sheet is None or \
                not profile_path or profile_path is None:
            messagebox.showerror("Error", "Input is empty!!")
        else:
            data = {
                "name_sheet": name_sheet,
                "profile_path": profile_path
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

    bt_start = Button(window, textvariable=text_button_start, font=("Arial", 19), width=15, bg="green", command=start)
    bt_start.grid(column=0, row=19)
    bt_start.grid(padx=10, pady=10)

    bt_save = Button(window, text="Save", font=("Arial", 19), width=15, bg="yellow", command=save)
    bt_save.grid(column=2, row=19, sticky=E)
    bt_save.grid(padx=10, pady=10)
    window.mainloop()


if __name__ == '__main__':
    main()
