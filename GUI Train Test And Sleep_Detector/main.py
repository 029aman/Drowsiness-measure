#---------------------------------------------------------------------------LIBRARY------------------------------------------------------------------------------
from re import M
import tensorflow as tf
import cv2 as cv 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import pathlib
import threading

from textwrap import fill
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from h5py._hl import dataset
from scipy.sparse.construct import random
from PIL import ImageTk, Image
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.layers.pooling import MaxPooling2D
from tensorflow.python.ops.gen_array_ops import expand_dims, pad
#---------------------------------------------------------------------------LIBRARY------------------------------------------------------------------------------


root = Tk()
root.title("GUI Train Test")
# root.iconbitmap()
root.geometry("750x440")
# root.minsize(height=440, width=750)

#--------------------------------------------------------------------------FUNCTIONS------------------------------------------------------------------------------

def skip():
    pass

def url_browse():
    url_frame.foldername = filedialog.askdirectory()
    url_entry.delete(0, END)
    url_entry.insert(0, url_frame.foldername)

def model_train():
    dataset_path = url_entry.get()
    dataset_path = pathlib.Path(dataset_path)

    open = list(dataset_path.glob('open/*'))
    closed = list(dataset_path.glob('closed/*'))

    eye_status = {
       'open' : open,
       'closed' : closed
    }

    eye_status_label = {
       'open' : 1,
       'closed' : 0
    }


    x, y = [] , []
    for eye_folder, eye_status_img in eye_status.items():
        for image in eye_status_img:
            img = cv.imread(str(image))
            img_resized = cv.resize(img, (100, 100))
            x.append(img_resized)
            y.append(eye_status_label[eye_folder])
    
    
    x = np.array(x)
    y = np.array(y)


    
    x_train_scaled = x/255.0
    
    model = Sequential([
        layers.Conv2D(32, 4, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 4, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(128, 4, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(10, activation='relu'),
        layers.Dense(2, activation='softmax')
    ])
    
    model.compile(
        optimizer=optimizer_comboBox.get(),
        loss=loss_comboBox.get(),
        metrics=['accuracy']
    )
    model.fit(x_train_scaled, y, epochs=int(epoches_input.get()))

#--------------------------------------------------------------------------FUNCTIONS------------------------------------------------------------------------------

#---------------------------------------------------------------------------MENU BAR-------------------------------------------------------------------------------- 
menu_bar = Menu(root)

File = Menu(root)
menu_bar.add_cascade(label="File", menu=File)
File.add_command(label="Open Code", command=skip)
File.add_command(label="Settings", command=skip)
File.add_separator()
File.add_command(label="Exit", command=skip)


Help = Menu()
menu_bar.add_cascade(label="Help", menu=Help)
Help.add_command(label="Get Started", command=skip)
Help.add_command(label="View Licence", command=skip)
Help.add_command(label="Privacy Statement", command=skip)
Help.add_separator()
Help.add_command(label="About", command=skip)

root.config(menu=menu_bar)

#----------------------------------------------------------------------------MENU BAR--------------------------------------------------------------------------------
outermost_frame =Frame(root).pack(fill=BOTH, expand=1)
workspace_frame = Frame(outermost_frame).pack(fill=BOTH, anchor=N, side=TOP)

#------------------------------------------------------------------------------TABS----------------------------------------------------------------------------------- 
tabs = ttk.Notebook(workspace_frame)

#-----------TAB 1-----------#
frame_train = Frame(tabs)
frame_train.pack(fill=BOTH, expand=1)
img_train = cv.imread("images/img_train.png")
img_train = cv.cvtColor(img_train, cv.COLOR_RGB2BGR)
img_train = cv.resize(img_train, (96,38))
img_train = ImageTk.PhotoImage(Image.fromarray(img_train))
tabs.add(frame_train, image=img_train)
#-----------TAB 1-----------#

#-----------TAB 2-----------#
frame_test = Frame(tabs)
frame_test.pack(fill=BOTH, expand=1)
img_test = cv.imread("images/img_test.png")
img_test = cv.cvtColor(img_test, cv.COLOR_RGB2BGR)
img_test = cv.resize(img_test, (96,38))
img_test = ImageTk.PhotoImage(Image.fromarray(img_test))
tabs.add(frame_test, image=img_test)
#-----------TAB 2-----------#

#-----------TAB 3-----------#
frame_preview = Frame(tabs)
frame_preview.pack(fill=BOTH, expand=1)
img_preview = cv.imread("images/img_preview.png")
img_preview = cv.cvtColor(img_preview, cv.COLOR_RGB2BGR)
img_preview = cv.resize(img_preview, (96,38))
img_preview = ImageTk.PhotoImage(Image.fromarray(img_preview))
tabs.add(frame_preview, image=img_preview)
#-----------TAB 3-----------#

#-----------TAB 4-----------#
frame_main = Frame(tabs)
frame_main.pack(fill=BOTH, expand=1)
img_main = cv.imread("images/img_main.png")
img_main = cv.cvtColor(img_main, cv.COLOR_RGB2BGR)
img_main = cv.resize(img_main, (96,38))
img_main = ImageTk.PhotoImage(Image.fromarray(img_main))
tabs.add(frame_main, image=img_main)
#-----------TAB 4-----------#

tabs.pack(fill=BOTH)
#------------------------------------------------------------------------------TABS----------------------------------------------------------------------------------- 

#----------------------------------------------------------------------------Status Bar------------------------------------------------------------------------------------
statusBar_frame = Frame(outermost_frame).pack(fill=BOTH, anchor=S)
status_info_frame = Frame(statusBar_frame, bg="#A7ACB0", height=10)



status_info_frame.pack(fill=BOTH, anchor=S, side=BOTTOM)
#----------------------------------------------------------------------------Status Bar------------------------------------------------------------------------------------

#---------------------------------------------------------------------------TAB 1 FRAME(Train)----------------------------------------------------------------------------

#------------Train Frame URL--------------

frame_train_url = LabelFrame(frame_train, text="Path")
url_frame = Frame(frame_train_url)

url = Label(url_frame, text="Sample Folder  :  ")
url.pack(side=LEFT, anchor=W, padx=(15, 5))

url_entry_frame =Frame(url_frame)
url_entry = Entry(url_entry_frame)
url_entry.pack(side=LEFT, anchor="center", fill=X, expand=1)
url_entry_frame.pack(side=LEFT, fill=X, expand=1)
#using expand here to make it reponsive ###########just to remember 


img_browse = cv.imread("images/img_browse.png")
img_browse = cv.resize(img_browse, (100, 30))
img_browse = ImageTk.PhotoImage(Image.fromarray(img_browse))
url_btn = Button(url_frame, image=img_browse, command=url_browse)
url_btn.pack(side=RIGHT, anchor=E, padx=15, pady=25)

url_frame.pack(fill=BOTH)
frame_train_url.pack(fill=BOTH, padx=20, pady=10)
#------------Train Frame URL-----------------



#------------Train Frame Compiler--------------

frame_train_compiler = LabelFrame(frame_train, text="Compile")
compiler_frame = Frame(frame_train_compiler)

compiler_optimizer_frame=Frame(compiler_frame)
optimizer_label = Label(compiler_optimizer_frame, text="Optimizer :  ")
optimizer_label.pack(side=LEFT)

optimizer_options = [
    "--select--",
    "adam",
    "SGD"
]

optimizer_comboBox = ttk.Combobox(compiler_optimizer_frame, values=optimizer_options)
optimizer_comboBox.current(0)
optimizer_comboBox.bind("<<ComboboxSelected>>", skip)
optimizer_comboBox.pack(side=LEFT)
compiler_optimizer_frame.pack(side=LEFT, anchor=W, expand=1, fill=X, padx=(15, 0), pady=(25, 70))

#--------------------------

compiler_loss_frame = Frame(compiler_frame)
loss_label = Label(compiler_loss_frame, text="Loss  :  ")
loss_label.pack(side=LEFT)

loss_options = [
    "--select--",
    "sparse_categorical_crossentropy",
    "categorical_crossentropy"
]

loss_comboBox = ttk.Combobox(compiler_loss_frame, values=loss_options)
loss_comboBox.current(0)
loss_comboBox.bind("<<ComboboxSeleceted>>", skip)
loss_comboBox.pack(side=LEFT)
compiler_loss_frame.pack(side=LEFT, anchor=CENTER, expand=1, fill=X, padx=(15, 0), pady=(25, 70))
#-------------------------

compiler_metrics_frame = Frame(compiler_frame)
metrics_label = Label(compiler_metrics_frame, text="Metrics  :  ")
metrics_label.pack(side=LEFT)

metrics_options = [
    "--select--",
    "accuracy",
    "unknown"
]

metrics_comboBox = ttk.Combobox(compiler_metrics_frame, values=metrics_options)
metrics_comboBox.current(0)
metrics_comboBox.bind("<<ComboboxSelected>>", skip)
metrics_comboBox.pack(side=LEFT)
compiler_metrics_frame.pack(side=RIGHT, expand=1, fill=X, pady=(25, 70), padx=(15, 15))
#---------------------------

compiler_frame.pack(fill=BOTH, expand=1)
frame_train_compiler.pack(fill=BOTH, padx=20, pady=10, expand=1)

#------------Train Frame Compiler--------------



#------------Train Frame Fit--------------
frame_train_fit = LabelFrame(frame_train, text="Fit")
fit_frame = Frame(frame_train_fit)

fit_epoches_frame = Frame(fit_frame)
fit_label = Label(fit_epoches_frame, text="Epoches  :  ")
fit_label.pack(side=LEFT)
epoches_input = Spinbox(fit_epoches_frame, from_=1, to=30)
epoches_input.pack(side=LEFT)
fit_epoches_frame.pack(pady=25, side=LEFT, padx=(15, 15))

fit_start_frame = Frame(fit_frame)
img_start = cv.imread("images/img_start.png")
img_start = ImageTk.PhotoImage(Image.fromarray(img_start))
Start_btn = Button(fit_start_frame, image=img_start, command=lambda : threading.Thread(target=model_train).start())
Start_btn.pack()
fit_start_frame.pack(side=RIGHT, padx=15, pady=10)

fit_frame.pack(side=LEFT ,fill=BOTH, expand=1)
frame_train_fit.pack(fill=BOTH, padx=20, pady=10, expand=1)
#------------Train Frame Fit--------------


#------------Train Frame LOGs--------------
frame_train_log = LabelFrame(frame_train, text="Log")
log_frame = Frame(frame_train_log)

textbox_train_log = Text(log_frame, height=30)

textbox_train_log.pack(fill=BOTH, padx=10, pady=10, expand=1)


log_frame.pack(fill=BOTH, expand=1)
frame_train_log.pack(expand=1, fill=BOTH, padx=20, pady=10, side=LEFT)

#------------Train Frame LOGs--------------
info_frame = LabelFrame(frame_train, text="Info")
frame_info =Frame(info_frame)


frame_info.pack(fill=BOTH, expand=1)
info_frame.pack(fill=BOTH, expand=1, side=RIGHT, padx=20, pady=10)
#---------------------------------------------------------------------------TAB 1 FRAME(Train)----------------------------------------------------------------------------


#---------------------------------------------------------------------------TAB 2 FRAME(Test)----------------------------------------------------------------------------

#-------------------Model Url---------------
frame_test_model_url = LabelFrame(frame_test, text="Model")
model_url_frame = Frame(frame_test_model_url)

model_url = Label(model_url_frame, text="Model Location  :  ")
model_url.pack(side=LEFT, anchor=W, padx=(15, 5))

model_url_entry_frame =Frame(model_url_frame)
model_url_entry = Entry(model_url_entry_frame)
model_url_entry.pack(side=LEFT, anchor="center", fill=X, expand=1)
model_url_entry_frame.pack(side=LEFT, fill=X, expand=1)


img_browse1 = cv.imread("images/img_browse.png")
img_browse1 = cv.resize(img_browse1, (100, 30))
img_browse1 = ImageTk.PhotoImage(Image.fromarray(img_browse1))
model_url_btn = Button(model_url_frame, image=img_browse1, command=skip)
model_url_btn.pack(side=RIGHT, anchor=E, padx=15, pady=25)

model_url_frame.pack(fill=BOTH)
frame_test_model_url.pack(fill=BOTH, padx=20, pady=10)
#-------------------Model Url---------------

#-------------------Sample Test Url---------------
frame_test_sample_url = LabelFrame(frame_test, text="Sample Data")
sample_url_frame = Frame(frame_test_sample_url)

sample_url = Label(sample_url_frame, text="Sample Folder   :  ")
sample_url.pack(side=LEFT, anchor=W, padx=(15, 5))

sample_url_entry_frame =Frame(sample_url_frame)
sample_url_entry = Entry(sample_url_entry_frame)
sample_url_entry.pack(side=LEFT, anchor="center", fill=X, expand=1)
sample_url_entry_frame.pack(side=LEFT, fill=X, expand=1)


img_browse2 = cv.imread("images/img_browse.png")
img_browse2 = cv.resize(img_browse2, (100, 30))
img_browse2 = ImageTk.PhotoImage(Image.fromarray(img_browse2))
sample_url_btn = Button(sample_url_frame, image=img_browse2, command=skip)
sample_url_btn.pack(side=RIGHT, anchor=E, padx=15, pady=25)

sample_url_frame.pack(fill=BOTH)
frame_test_sample_url.pack(fill=BOTH, padx=20, pady=10)
#-------------------Sample Test Url---------------

#----------------------Test Start-------------------
frame_test_start = Frame(frame_test)
start_test_frame = Frame(frame_test_start)


img_start1 = cv.imread("images/img_start.png")
img_start1 = ImageTk.PhotoImage(Image.fromarray(img_start1))
Start_btn_test = Button(start_test_frame, image=img_start1, command=skip)
Start_btn_test.pack()


start_test_frame.pack(fill=BOTH)
frame_test_start.pack(fill=BOTH, padx=20, pady=10)
#----------------------Test Start-------------------

#----------------------Result--------------------
result_frame = LabelFrame(frame_test, text="Result")
frame_result =Frame(result_frame)


frame_info.pack(fill=BOTH, expand=1)
result_frame.pack(fill=BOTH, expand=1, side=LEFT, padx=20, pady=10)
#----------------------Result--------------------

#-----------------------Test Log--------------------
frame_test_log = LabelFrame(frame_test, text="Log")
log_test_frame = Frame(frame_test_log)

textbox_test_log =Text(log_test_frame)

textbox_test_log.pack(fill=BOTH, padx=10, pady=10, expand=1)

log_test_frame.pack(fill=BOTH, expand=1)
frame_test_log.pack(fill=BOTH, padx=20, pady=10, expand=1, side=RIGHT)
#-----------------------Test Log--------------------
#---------------------------------------------------------------------------TAB 2 FRAME(Test)----------------------------------------------------------------------------

#---------------------------------------------------------------------------TAB 3 FRAME(Preview)----------------------------------------------------------------------------
#-------------------------------CAM-------------------------------------------
frame_preview_cam = Frame(frame_preview)
cam_img = Frame(frame_preview_cam)
label= Label(frame_preview_cam, text="am,an", height=55)

label.pack(anchor=CENTER, expand=1, fill=BOTH)
cam_img.pack(expand=1, fill=BOTH, padx=3)
frame_preview_cam.pack(expand=1, fill=BOTH, padx=10, side=TOP, anchor=N)
#--------------------------------CAM-------------------------------------------

#--------------------------------OPTION CAM-------------------------------------------
frame_cam_options = Frame(frame_preview)
#----------------ON/OFF-----------------------
cam_option_on = Frame(frame_cam_options)
img_on_off = cv.imread("images/img_on_off.png")
img_on_off = ImageTk.PhotoImage(Image.fromarray(img_on_off))
cam_on_off_btn = Button(cam_option_on, image=img_on_off, borderwidth=0)
cam_on_off_btn.pack()
cam_option_on.pack(anchor=W, side=LEFT, expand=1,padx=10)
#----------------ON/OFF-----------------------

#-------------CLICK/RECORD--------------------------
cam_option_click = Frame(frame_cam_options)
img_click = cv.imread("images/img_click.png")
img_click = ImageTk.PhotoImage(Image.fromarray(img_click))
cam_click_btn = Button(cam_option_click, image=img_click, borderwidth=0)
cam_click_btn.pack(side=LEFT, anchor=W, padx=8)

img_switch = cv.imread("images/img_switch.png")
img_switch = ImageTk.PhotoImage(Image.fromarray(img_switch))
cam_switch_btn = Button(cam_option_click, image=img_switch, borderwidth=0)
cam_switch_btn.pack(side=LEFT, anchor=CENTER, padx=8)

img_record = cv.imread("images/img_record.png")
img_record = ImageTk.PhotoImage(Image.fromarray(img_record))
cam_record_btn = Button(cam_option_click, image=img_record, borderwidth=0)
cam_record_btn.pack(side=LEFT, anchor=E, padx=8)
cam_option_click.pack(anchor=CENTER, side=LEFT, expand=1,padx=10)
#-------------CLICK/RECORD--------------------------

#---------------RECENT IMG----------------------
cam_option_recent = Frame(frame_cam_options)
img_recent = cv.imread("images/img_on_off.png")
img_recent = ImageTk.PhotoImage(Image.fromarray(img_recent))
cam_recent_btn = Button(cam_option_recent, image=img_recent, borderwidth=0)
cam_recent_btn.pack()
cam_option_recent.pack(anchor=E, side=RIGHT, expand=1,padx=10)
#---------------RECENT IMG----------------------
frame_cam_options.pack(expand=1, padx=10, fill=BOTH, side=BOTTOM, anchor=S)
#-------------------------------OPTION CAM--------------------------------------------
#---------------------------------------------------------------------------TAB 3 FRAME(Preview)----------------------------------------------------------------------------


#---------------------------------------------------------------------------TAB 4 FRAME(Main)----------------------------------------------------------------------------

# # frame_main_1 = LabelFrame(frame_main, text="1").pack()
# main_color_alert = LabelFrame(frame_main, text="State")
# label0 = Label(main_color_alert, text="aman").pack()
# main_color_alert.pack()

# main_cam = LabelFrame(frame_main, text="Display")
# label1 = Label(main_cam, text="aman").pack()
# main_cam.


# # frame_main_2 = LabelFrame(frame_main, text="2").pack()
# main_alert = LabelFrame(frame_main, text="Alert", width=90)
# label2 = Label(main_alert, text="aman").pack()
# main_alert.

# main_evaluation = LabelFrame(frame_main, text="Evaluation")
# label3 = Label(main_evaluation, text="aman").pack()
# main_evaluation.

main1 = Frame(frame_main)
color_alert = LabelFrame(main1, text="COLOR")

color_alert.pack(side=LEFT, anchor=W, fill=BOTH, expand=1, padx=20, pady=10)


cam_display = LabelFrame(main1, text="Display")
cam_display_frame = Frame(cam_display)
label = Label(cam_display_frame, image=img_browse, bg="beige").pack(expand=1, fill=BOTH)
cam_display_frame.pack(fill=BOTH, expand=1)
cam_display.pack(side=RIGHT, anchor=E, fill=BOTH, expand=1, padx=20, pady=10)
main1.pack(fill=BOTH, expand=1)

main2 = Frame(frame_main)
text_alert = LabelFrame(main2, text="Alert")

text_alert.pack(side=LEFT, anchor=W, fill=BOTH, expand=1, padx=20, pady=10)


score_alert = LabelFrame(main2, text="Score")

score_alert.pack(side=RIGHT, anchor=E, fill=BOTH, expand=1, padx=20, pady=10)
main2.pack(fill=BOTH, expand=1)
#---------------------------------------------------------------------------TAB 4 FRAME(Main)----------------------------------------------------------------------------
root.mainloop()