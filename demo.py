from tkinter import *
from tkinter import messagebox
import asyncio
import threading
import random

def _asyncio_thread(async_loop):
    async_loop.run_until_complete(do_urls())


def do_tasks(async_loop):
    """ Button-Event-Handler starting the asyncio part. """
    threading.Thread(target=_asyncio_thread, args=(async_loop,)).start()

    
async def one_url(url):
    """ One task. """
    sec = random.randint(1, 8)
    await asyncio.sleep(sec)
    return 'url: {}\tsec: {}'.format(url, sec)

async def do_urls():
    """ Creating and starting 10 tasks. """
    tasks = [one_url(url) for url in range(10)]
    completed, pending = await asyncio.wait(tasks)
    results = [task.result() for task in completed]
    print('\n'.join(results))


def do_freezed():
    messagebox.showinfo(message='Tkinter is reacting.')

def main(async_loop):
    root = Tk()
    Button(master=root, text='Asyncio Tasks', command= lambda:do_tasks(async_loop)).pack()
    Button(master=root, text='Freezed???', command=do_freezed).pack()
    root.mainloop()

if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    main(async_loop)
Share
Improve this answer
Follow
edited Sep 1, 2021 at 13:01
TheLizzard's user avatar
TheLizzard
7,36322 gold badges1111 silver badges3131 bronze badges
answered Dec 21, 2017 at 7:40
bhaskarc's user avatar
bhaskarc
9,3001010 gold badges6565 silver badges8787 bronze badges
3
What is the reason for calling asyncio.get_event_loop() in the main thread instead of in the worker thread? – 
Brent
 Nov 11, 2020 at 1:58
Why did you use buttonX = Button(...).pack()? Please look at this to see the problem. – 
TheLizzard
 Aug 31, 2021 at 9:13
1
@TheLizzard - Yes you are right about it. However since we do not use buttonX variable after that line, it really doesn't mater in this example. – 
bhaskarc
 Sep 1, 2021 at 12:32
2
@bhaskarc It can confuse people that see this in the future. It's better to just use Button(...).pack(). So many new people make this mistake. – 
TheLizzard
 Sep 1, 2021 at 13:01
Add a comment
4

I'm a bit late to the party but if you are not targeting Windows you can use aiotkinter to achieve what you want. I modified your code to show you how to use this package:

from tkinter import *
from tkinter import messagebox
import asyncio
import random

import aiotkinter

def do_freezed():
    """ Button-Event-Handler to see if a button on GUI works. """
    messagebox.showinfo(message='Tkinter is reacting.')

def do_tasks():
    task = asyncio.ensure_future(do_urls())
    task.add_done_callback(tasks_done)

def tasks_done(task):
    messagebox.showinfo(message='Tasks done.')

async def one_url(url):
    """ One task. """
    sec = random.randint(1, 15)
    await asyncio.sleep(sec)
    return 'url: {}\tsec: {}'.format(url, sec)

async def do_urls():
    """ Creating and starting 10 tasks. """
    tasks = [
        one_url(url)
        for url in range(10)
    ]
    completed, pending = await asyncio.wait(tasks)
    results = [task.result() for task in completed]
    print('\n'.join(results))

if __name__ == '__main__':
    asyncio.set_event_loop_policy(aiotkinter.TkinterEventLoopPolicy())
    loop = asyncio.get_event_loop()
    root = Tk()
    buttonT = Button(master=root, text='Asyncio Tasks', command=do_tasks)
    buttonT.pack()
    buttonX = Button(master=root, text='Freezed???', command=do_freezed)
    buttonX.pack()
    loop.run_forever()
