import logging,os
import tkinter as tk
from tkinter import OptionMenu, filedialog,ttk
import tkinter.scrolledtext as ScrolledText



logging.basicConfig(filename='test.log',
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')        

# Add the handler to logger

logger = logging.getLogger()      


class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text
        self.max_length = 250


    def emit(self, record):
        msg = self.format(record)
        if len(msg) > self.max_length:
            lines = []
            while len(msg) > self.max_length:
                lines.append(msg[:self.max_length])
                msg = msg[self.max_length:]
            lines.append(msg)
            msg= '\n'.join(lines)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


def docView(frame,ttkframe,lang):
  
    
    sociallang = tk.StringVar()


    l_lang = tk.Label(ttkframe, text='display lang')
    # l_lang.place(x=10, y=90)
    l_lang.grid(row = 3, column = 0, columnspan = 3, padx=14, pady=15)    


    keeplang = sociallang.get()    
    box = ttk.Combobox(ttkframe, textvariable=keeplang, state='readonly')
    # box.place(x=10, y=120)
    box.grid(row = 4, column = 1, columnspan = 3, padx=14, pady=15)    

    def selectedlang(event):
        box = event.widget
        
        print('selected lang is :',box.get())
        changeDisplayLang(box.get())
    box['values'] = ('en', 'zh')
    box.current(0)
    box.bind("<<ComboboxSelected>>", selectedlang)
def render(root,window,log_frame,lang):
    global doc_frame
    tab_control = ttk.Notebook(window)
    
    doc_frame = ttk.Frame(tab_control)
    doc_frame.grid_rowconfigure(0, weight=1)
    doc_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    doc_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    doc_frame.columnconfigure((0,1), weight=1)
    
    doc_frame_left = tk.Frame(doc_frame)
    doc_frame_left.grid(row=0,column=0,sticky="nsew")
    doc_frame_right = tk.Frame(doc_frame)
    doc_frame_right.grid(row=0,column=1,sticky="nsew") 




    if lang=='en':
        print('1111')
        tab_control.add(doc_frame, text='help')
    else:
        tab_control.add(doc_frame, text='帮助')
        print('222')

    docView(doc_frame_left,doc_frame_right,lang)

    account_frame = ttk.Frame(tab_control)
    account_frame.grid_rowconfigure(0, weight=1)
    account_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    account_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    account_frame.columnconfigure((0,1), weight=1)
    
    account_frame_left = tk.Frame(account_frame, height = 240)
    account_frame_left.grid(row=0,column=0,sticky="nsew")
    account_frame_right = tk.Frame(account_frame, height = 240)
    account_frame_right.grid(row=0,column=1,sticky="nsew") 
    tab_control.add(account_frame, text='demo')
    docView(account_frame_right,account_frame_left,lang)

    # tab_control.pack(expand=1, fill='both')
    tab_control.grid(row=0,column=0)








def start(lang):

    global ROOT_DIR
    ROOT_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    global root,paned_window,log_frame,mainwindow,st

    # root.resizable(width=True, height=True)
    root.iconbitmap("assets/icon.ico")
    # Create a PanedWindow widget (vertical)
    paned_window = tk.PanedWindow(root, orient=tk.VERTICAL)
    paned_window.pack(expand=True, fill="both")

    # Configure weights for mainwindow and log_frame
    paned_window.grid_rowconfigure(0, weight=5)
    paned_window.grid_rowconfigure(1, weight=1)

    # Create the frame for the notebook
    mainwindow = ttk.Frame(paned_window)
    paned_window.add(mainwindow)
    mainwindow.grid_rowconfigure(0, weight=1)
    mainwindow.grid_columnconfigure(0, weight=1)


    


    log_frame =tk.Frame(paned_window)
    paned_window.add(log_frame)

    log_frame.grid_rowconfigure(0, weight=1)
    log_frame.grid_columnconfigure(0, weight=1)
    log_frame.columnconfigure(0, weight=1)
    log_frame.rowconfigure(0, weight=1)




    st = ScrolledText.ScrolledText(log_frame,                                      
                                # width = width, 
                                #     height = 5, 
                                    state='disabled')


    st.configure(font='TkFixedFont')
    st.grid(column=0, 
            row=0, 
            sticky='nwse',
            # columnspan=4
            )
    global text_handler
    text_handler = TextHandler(st)

    logger.addHandler(text_handler)    


    render(root,mainwindow,log_frame,lang)
    root.update_idletasks()

# # Set the initial size of the notebook frame (4/5 of total height)
    mainwindow_initial_percentage = 5 / 6  

    # Calculate the initial height of mainwindow based on the percentage
    initial_height = int(float(root.winfo_height()) * mainwindow_initial_percentage)
    mainwindow.config(height=initial_height)
    
def changeDisplayLang(lang):

    mainwindow.destroy()
    # st.destroy()
    del st
    log_frame.destroy()
    paned_window.destroy()
    # root.quit()    
    # del text_handler
    start(lang)
    logger.info(f'switch lang to locale:{lang}')
    
    root.mainloop()

if __name__ == '__main__':
    global root,st
    root = tk.Tk()
    start('en')
    root.mainloop()

