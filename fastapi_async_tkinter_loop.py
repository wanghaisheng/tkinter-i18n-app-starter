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
from batchrunworker import BatchWorker
from string import ascii_uppercase
import time,os
import psutil
import threading
uvicorn_subprocess: Optional[Process] = None
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
path=ROOT_DIR+os.sep+'assets/icon.ico'

console_encoding = "utf-8"
process_name=None
if platform.system() == "Windows":
    from ctypes import windll

    console_code_page = windll.kernel32.GetConsoleOutputCP()
    if console_code_page != 65001:
        console_encoding = f"cp{console_code_page}"

async def task(name: str):
    print(f"Task '{name}' is running...")
    if name=='A':
        print('task failed')
    else:
        print('task ok')
    await asyncio.sleep(3)  # Pretend to do something
TASK_NAMES = ascii_uppercase  # 26 fake tasks in total

async def do_tasks():
    tasks = [task(name) for name in TASK_NAMES]
    worker = BatchWorker(tasks)
    await worker.run()

def start(lang, root=None):
    global mainwindow, canvas

    # root.resizable(width=True, height=True)
    root.iconbitmap(path)
    root.title('tkinter async_tkinter_loop demo')
    Button(master=root, text="async_handler Asyncio Tasks", command=async_handler(do_tasks)).pack()


    Button(master=root, text="Start Server", command=start_fastapi_server).pack(side=tk.LEFT)

    Button(master=root, text="Stop Server", command=stop).pack(side=tk.LEFT)

    root.update_idletasks()


def quit_window(icon):

    print('Shutdown icon')
    icon.stop()

    print('Shutdown server')
    try:
        print('server is  there')
    # We need to make sure we won't kill different process
    # https://stackoverflow.com/questions/71814738/asyncio-terminate-subprocess-on-wait-for-timeout
    # https://python.readthedocs.io/en/stable/library/asyncio-subprocess.html#asyncio.asyncio.subprocess.Process
    # returncode
    # Return code of the process when it exited. A None value indicates that the process has not terminated yet.

    # A negative value -N indicates that the child was terminated by signal N (Unix only).
        if uvicorn_subprocess.returncode is None:
            parent = psutil.Process(uvicorn_subprocess.pid)
            for child in parent.children(recursive=True): 
                child.terminate()
            parent.terminate()
        # uvicorn_subprocess.kill()
        print('server is shutdown now')

    except:
        print('server is shutdown already')
    if uvicorn_subprocess.returncode is not None:
        print('check result server is there ')

    else:
        print('check result server is shutdown already')

    print('Shutdown root')
    # https://github.com/insolor/async-tkinter-loop/issues/10
    root.quit()
    root.destroy()




def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)


def withdraw_window():
    root.withdraw()
    image = Image.open(path)

    menu = (item("Quit", lambda icon:quit_window(icon)),
            item("Show", show_window))

    
    icon = pystray.Icon("name", image, "title", menu)
    icon.run()


@async_handler
async def start_fastapi_server():
    global uvicorn_subprocess
    uvicorn_command = ["uvicorn", "fastapiserver:app", "--host", "0.0.0.0", "--port", "8000"]

    uvicorn_subprocess = await asyncio.create_subprocess_exec(
        *uvicorn_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    while uvicorn_subprocess.returncode is None:
        stdout = asyncio.create_task(uvicorn_subprocess.stdout.readline())
        stderr = asyncio.create_task(uvicorn_subprocess.stderr.readline())

        done, pending = await asyncio.wait({stdout, stderr}, return_when=asyncio.FIRST_COMPLETED)

        if stdout in done:
            result_text = stdout.result().decode(console_encoding)
            print(f'stdout:{result_text}')

        if stderr in done:
            result_text = stderr.result().decode(console_encoding)
            print(f'stderr:{result_text}')

        for item in pending:
            item.cancel()

    uvicorn_subprocess = None

async def is_running():
    # https://stackoverflow.com/questions/65874648/python-asyncio-subprocess-how-to-see-whether-it-is-still-running
    with suppress(asyncio.TimeoutError):
        await asyncio.wait_for(uvicorn_subprocess.wait(), 1e-6)
    return uvicorn_subprocess.returncode is None    
def stop_notworking_demo():

    print('Shutdown server')
    # we should use uvicorn_subprocess.returncode
    if uvicorn_subprocess is not None:


        time.sleep(0.5)
        uvicorn_subprocess.terminate() 

    else:
        print('server not started')

def stop():
#  this can not kill all the process and thread so you can not remove any exe files
    print('Shutdown server')
    if uvicorn_subprocess is not None:


        time.sleep(0.5)
        uvicorn_subprocess.terminate() 

    else:
        print('server not started')



def start_tkinter_app():
    global root, settings, db, canvas, locale
    root = tk.Tk()

    locale = 'en'
    start(locale, root)

    root.protocol('WM_DELETE_WINDOW', withdraw_window)

    async_mainloop(root)




if __name__ == "__main__":
    start_fastapi_server()
    start_tkinter_app()
