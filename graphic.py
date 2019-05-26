import tkinter as tk
import mahjong as mj

mjhai_img = {}

def load_image(mjhai_list):
    for hai in mjhai_list:
        file_img = "image/" + hai.name + ".gif"
        mjhai_img[hai.name] = tk.PhotoImage(file=file_img)

def show_tehai(master, tehai):
    for i, hai in enumerate(tehai):
        label = tk.Label(master, image=mjhai_img[hai.name])
        label.grid(row=0, column=i)
