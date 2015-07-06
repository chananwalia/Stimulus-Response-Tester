import winsound
import os
import sys
import PIL
from time import clock
from Tkinter import *
import random
import msvcrt
import cPickle as pickle
from PIL import Image, ImageTk


soundfile = pickle.load(open("py_data.txt", 'rb'))

winsound.PlaySound(soundfile, winsound.SND_FILENAME)

