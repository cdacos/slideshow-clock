# -*- coding: utf-8 -*-
import argparse
import datetime
from itertools import cycle
import os
try: # Python2
    import Tkinter as tk
    import tkFont as tkf
except ImportError: # Python3
    import tkinter as tk
    import tkinter.font as tkf
from PIL import Image, ImageTk
from random import shuffle
from time import sleep

IMAGE_DELAY = 10 # Seconds

def image_paths(input_dir='.'):
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpg', 'png', 'gif')): 
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths

def display_image(path, canvas, max_width, max_height):
    canvas.delete("all")

    # Image
    image = Image.open(path)
    width, height = image.size
    # print([max_width, max_height])
    # print([width, height])
    width_ratio = max_width / float(width)
    height_ratio = max_height / float(height)
    # print([width_ratio, height_ratio])
    if width_ratio > height_ratio:
        width = height_ratio * width
        height = height_ratio * height
    else:
        width = width_ratio * width
        height = width_ratio * height
    # print([width, height])
    image = image.resize((int(width), int(height)), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(int((max_width - width) / 2), 0, image=photo, anchor='nw')

    # Time
    now = datetime.datetime.now()
    hour = now.hour
    color = get_hour_color(hour)
    time = now.strftime('%-I:%M')
    sans_serif = tkf.Font(family='Sans-serif', size=64, weight='bold')
    canvas.create_text(max_width - 150, max_height - 100, text=time, font=sans_serif, fill=color, anchor='center')

    # Morning indicator
    sans_serif = tkf.Font(family='Sans-serif', size=32, weight='bold')
    inc = int(max_height / 25)
    for i in range(24):
        hour_mark = (i + 19) % 24
        color = get_hour_color(hour_mark)
        mark = '- ←' if hour_mark == hour else '-'
        canvas.create_text(20, inc * i, text=mark, font=sans_serif, fill=color, anchor='nw')

    canvas.update()

def get_hour_color(hour):
    return 'blue' if hour > 18 or hour < 7 else 'yellow'

def files_loop(paths, canvas, max_width, max_height):
    # print([max_width, max_height])
    walk = list(range(len(paths)))
    shuffle(walk)
    for i in walk:
        path = paths[i]
        print([i, path])
        display_image(path, canvas, max_width, max_height)
        sleep(IMAGE_DELAY)

def main_loop(dir='.'):
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.overrideredirect(True)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    canvas = tk.Canvas(root, width=width, height=height, highlightthickness=0)
    canvas.pack(side='top', fill='both', expand='yes')
    canvas.configure(background='black')
    while True:
        files_loop(image_paths(dir), canvas, canvas.winfo_screenwidth(), canvas.winfo_screenheight())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory of images', nargs='?', default=os.getcwd())
    args = parser.parse_args()

    main_loop(args.dir)
