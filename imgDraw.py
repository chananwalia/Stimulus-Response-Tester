import winsound
import os
import sys
from time import clock
from Tkinter import *
import random
import msvcrt
import cPickle as pickle

players, colors, keys_players, keys_colors = pickle.load(open("py_data.txt", 'rb'))

def image():
    color = random.choice(colors)

    root = Tk()
    canvas = Canvas(width=600, height=200, bg=color)
    canvas.pack(expand=YES, fill=BOTH)

    def key(event):
        k = event.char
        if k in keys_players:
            p = keys_players[k]
            if keys_colors[p][k] == color:
                if p not in answer_times:
                    answer_times[p] = clock() - start_time
            if len(answer_times) == players:
                root.destroy()
        else:
            print 'Please use the correct buzzers.'

    root.bind_all('<Key>', key)

    answer_times = {}

    start_time = clock()
    root.mainloop()
    return (color, answer_times)

pickle.dump(image(), open("py_data.txt", 'wb'))
