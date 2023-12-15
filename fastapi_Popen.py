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
from typing import Optional
import platform
import time
import shlex, subprocess
from batchrunworker import BatchWorker
from string import ascii_uppercase
import threading

console_encoding = "utf-8"
uvicorn_subprocess=None
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

async def do_tasks(BATCH_SIZE=3):
    tasks = [task(name) for name in TASK_NAMES]
    worker = BatchWorker(tasks,BATCH_SIZE=BATCH_SIZE)
    await worker.run()

def do_tasks_wrap(i=0):
    print('55555555555555',i)
    asyncio.run(do_tasks(BATCH_SIZE=i))
def start(lang, root=None):
    global mainwindow, canvas

    # root.resizable(width=True, height=True)
    root.iconbitmap("assets/icon.ico")
    root.title('popen demo')
    Button(master=root, text="Asyncio Tasks", command=lambda:threading.Thread(target=do_tasks_wrap, args=(5,)).start()).pack()


    Button(master=root, text="Start Server", command=lambda:threading.Thread(target=start_fastapi_server).start()).pack(side=tk.LEFT)

    Button(master=root, text="Stop Server", command=stop).pack(side=tk.LEFT)

    root.update_idletasks()






def quit_window(icon, item):
    print('prepare to quit uploader genius program')

    print('cancel all waiting tasks')

    # threading.Thread(
    #             target=cancerlall()
    #         ).start()
    cancel_all_waiting_tasks(frame=None)
    # print('Shutdown icon')
    icon.stop()

    print('Shutdown thumbnail genius server')
    if uvicorn_subprocess is not None:
        uvicorn_subprocess.terminate()
        time.sleep(0.5)
        done=uvicorn_subprocess.poll()
        if done==None:
            print(f'server shutdown error :{done}')

        else:
            print('server shutdown')
    else:
        print('server not started')
    try:
        uvicorn_subprocess
        if uvicorn_subprocess.returncode is  None:
            print('check result server is there ')
            parent = psutil.Process(uvicorn_subprocess.pid)
            for child in parent.children(recursive=True):
                child.terminate()
            parent.terminate()
        else:
            print('check result server is shutdown already')
    except:
        print('check result server is shutdown already')


    # print(' check what threads are still open at the end of your program.')
    # print(threading.enumerate())
    # main_thread = threading.current_thread()

    # for t in threading.enumerate():
    #     if t is main_thread:
    #         continue
    #     print(f"joining {t.getName()} ")
    #     logger.debug('joining %s', t.getName())
    #     threading.Event().set()

    # print('here')
    print('quit uploader genius program now')


    # windows and mac act differently
    if sys.platform == 'win32':
        current_system_pid = os.getpid()

        ThisSystem = psutil.Process(current_system_pid)
        ThisSystem.terminate()
        os._exit(1)
    elif  sys.platform=='darwin':

        print('Shutdown root')
        # https://github.com/insolor/async-tkinter-loop/issues/10

        root.quit()

        root.destroy()

    else:
        import signal

        os.kill(os.getpid(), signal.SIGINT)




def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)


def withdraw_window():
    root.withdraw()
    iconfile = os.path.join(ROOT_DIR, iconfilename)

    image = Image.open(iconfile)
    menu = (item("Quit", quit_window), item("Show", show_window))
    icon = pystray.Icon("name", image, "title", menu)
    icon.run_detached()
    # icon.run()


def start_fastapi_server():
    global uvicorn_subprocess
    print('start thumbnail template editor server',ROOT_DIR)
    lib_folder = os.path.join(ROOT_DIR, 'lib')

    uvicorn_command = ["uvicorn", "src.app.fastapiserver:app", "--host", "0.0.0.0", "--port", "8000"]
    # uvicorn_subprocess = subprocess.Popen(uvicorn_command)
    uvicorn_subprocess = subprocess.Popen(uvicorn_command, cwd=lib_folder if getattr(sys, "frozen", False) else None)

    # fastapiserver.app.mount("/static", StaticFiles(directory=os.path.join(ROOT_DIR,"static")), name="static")


    try:
        outs, errs = uvicorn_subprocess.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        # uvicorn_subprocess.kill()
        outs, errs = uvicorn_subprocess.communicate()
    if outs:
        print(f'stdout:{outs}')
    if errs:
        print(f'stdout:{errs}')

def stop():
    if uvicorn_subprocess is not None:
        uvicorn_subprocess.terminate() 
        time.sleep(0.5)
        done=uvicorn_subprocess.poll()
        if done==None:
            print(f'server shutdown error :{done}')

        else:
            print('server shutdown')

def start_tkinter_app():
    global root, settings, db, canvas, locale
    root = tk.Tk()

    locale = 'en'
    start(locale, root)

    root.protocol('WM_DELETE_WINDOW', withdraw_window)

    root.mainloop()




if __name__ == "__main__":
    start_tkinter_app()
