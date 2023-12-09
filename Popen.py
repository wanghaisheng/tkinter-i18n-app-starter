import sys
from tkinter import *
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import asyncio
import tkinter as tk
from asyncio import CancelledError
from contextlib import suppress
import random
from async_tkinter_loop import async_handler, async_mainloop
from asyncio.subprocess import Process
from typing import Optional
import platform

uvicorn_subprocess: Optional[Process] = None


console_encoding = "utf-8"

if platform.system() == "Windows":
    from ctypes import windll

    console_code_page = windll.kernel32.GetConsoleOutputCP()
    if console_code_page != 65001:
        console_encoding = f"cp{console_code_page}"



async def one_url(url):
    """One task."""
    print(f'run one_url: {url}')  # for debug
    sec = random.randint(1, 8)
    await asyncio.sleep(sec)
    return "url: {}\tsec: {}".format(url, sec)


async def do_urls():
    """Creating and starting 10 tasks."""
    tasks = [one_url(url) for url in range(10)]
    completed, pending = await asyncio.wait(tasks)
    results = [task.result() for task in completed]
    print("\n".join(results))



def start(lang, root=None):
    global mainwindow, canvas

    # root.resizable(width=True, height=True)
    root.iconbitmap("assets/icon.ico")
    root.title('tkinter asyncio demo')
    Button(master=root, text="Asyncio Tasks", command=async_handler(do_urls)).pack()
    Button(master=root, text="Start Server", command=start_fastapi_server).pack(side=tk.LEFT)

    Button(master=root, text="Stop Server", command=stop).pack(side=tk.LEFT)

    root.update_idletasks()


def quit_window(icon):

    print('Shutdown icon')
    icon.stop()

    print('Shutdown server')
    if uvicorn_subprocess is not None:
        uvicorn_subprocess.terminate() 
        time.sleep(0.5)
        uvicorn_subprocess.poll()

    print('Shutdown root')
    # https://github.com/insolor/async-tkinter-loop/issues/10
    root.quit()
    root.destroy()




def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)


def withdraw_window():
    root.withdraw()
    image = Image.open("assets/icon.ico")

    menu = (item("Quit", lambda icon:quit_window(icon)),
            item("Show", show_window))

    
    icon = pystray.Icon("name", image, "title", menu)
    icon.run()

# https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true

def start_fastapi_server():
    global uvicorn_subprocess
    uvicorn_command = ["uvicorn", "fastapiserver:app", "--host", "0.0.0.0", "--port", "8000"]
    uvicorn_subprocess = Popen(uvicorn_command) 



def stop():
    if uvicorn_subprocess is not None:
        uvicorn_subprocess.terminate() 
        time.sleep(0.5)
        uvicorn_subprocess.poll()



def start_tkinter_app():
    global root, settings, db, canvas, locale
    root = tk.Tk()

    locale = 'en'
    start(locale, root)

    root.protocol('WM_DELETE_WINDOW', withdraw_window)

    async_mainloop(root)




if __name__ == "__main__":
    start_tkinter_app()
