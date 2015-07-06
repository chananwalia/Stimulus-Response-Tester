import winsound
import os
import sys
from time import clock
from Tkinter import *
import random
import msvcrt
import cPickle as pickle
import subprocess
from operator import itemgetter

def cls(): print "\n" * 30

cls()
print 'Welcome to Buzz!'
raw_input()
cls()
print 'How many players are present?'
players = int(raw_input())
cls()
print 'Grab a buzzer. On the left side of the buzzer,'
print 'take a look at the player number.'
raw_input()
cls()
print 'To begin, I will present three test stimuli.'
raw_input()
cls()

colors = ['blue', 'OrangeRed', 'green', 'yellow']
player_keys = ['asdf', 'qwer', 'zxcv', 'hjkl'][:players]
keys_players = {}
for p, k in enumerate(player_keys):
    keys_players.update(dict(zip(list(k), [p]*4)))
keys_colors = [dict(zip(list(x), colors)) for x in player_keys]
results = []

def collect_result(title, color, answer_times):
    results.append((title, color, answer_times))

def display_sort_result(answer_times):
    print '\n' * 2
    for p, t in sorted(answer_times.items(), key=itemgetter(1)):
        print "\tPlayer %s: %s ms" % (p+1, int(t * 1000))

def display_result(title, answer_times):
    if answer_times:
        print '\n' * 2
        print "%s" % (title)
        for p, t in answer_times.items():
            print "\tPlayer %s: %s ms" % (p+1, int(t * 1000))
        print "\tAverage of all players: %s ms" % (int(sum(answer_times.values())*1000/len(answer_times)))

def display_results():

    def avg(answer_times_list):
        n = len(answer_times_list)
        if n == 0:
            return None
        all_answer_times = dict(zip(range(players), [0]*players))
        for answer_times in answer_times_list:
            for k, v in answer_times.items():
                all_answer_times[k] += v
        for k in all_answer_times:
            all_answer_times[k] /= n
        return all_answer_times

    for type in set([x[0] for x in results]):
        display_result("Average for %s stimulus:" % type, avg([x[2] for x in results if x[0] == type]))
    display_result("Average for all stimuli:", avg([x[2] for x in results]))

 

def image(collect=True):
    pickle.dump((players, colors, keys_players, keys_colors), open("py_data.txt", 'wb'))
    subprocess.call([sys.executable, "imgDraw.py"])
    color, answer_times = pickle.load(open("py_data.txt", 'rb'))
    display_sort_result(answer_times)
    if (collect):
        collect_result("visual", color, answer_times)

def text(collect=True):
    pickle.dump((players, colors, keys_players, keys_colors), open("py_data.txt", 'wb'))
    subprocess.call([sys.executable, "textDraw.py"])
    color, answer_times = pickle.load(open("py_data.txt", 'rb'))
    display_sort_result(answer_times)
    if (collect):
        collect_result("textual", color, answer_times)
    
def sound(collect=True):
    sounds = {"blue.wav": 'blue', "OrangeRed.wav": 'OrangeRed', "green.wav": 'green', "yellow.wav": 'yellow'}
    soundfile, color = random.choice(sounds.items())
    pickle.dump(soundfile, open("py_data.txt", 'wb'))
    proc = subprocess.Popen([sys.executable, "playSound.py"])
    if (proc):
        start_time = clock()
    answer_times = {}
    while (len(answer_times) != players):
        if msvcrt.kbhit():
            k = msvcrt.getch()
            if k in keys_players:
                p = keys_players[k]
                if keys_colors[p][k] == color:
                    if p not in answer_times:
                        answer_times[p] = clock() - start_time - 0.2
            else:
                print 'Please use the correct buzzers.'
                raw_input()
    proc.communicate()
    display_sort_result(answer_times)
    if (collect):
        collect_result("auditory", color, answer_times)

def test():
    image(False)
    print
    print 'That was a visual stimulus.'
    raw_input()
    cls()
    text(False)
    print
    print 'That was a textual stimulus.'
    raw_input()
    cls()
    sound(False)
    print
    print 'That was an auditory stimulus.'
    raw_input()

test()

cls()
print 'Now, actual data will be collected.'
print 'Hit enter when ready...'
raw_input()

testers = [image, sound, text, image, sound, text, image, sound, text, image, sound, text]

myround = len(testers)

while myround > 0 :
    
    cls()
    y = random.choice(testers)
    y()
    i = testers.index(y)
    del testers [i] 
    myround=len(testers)
    print
    print 'Hit enter when ready...'
    raw_input()
    
cls()

print 'The game has ended. Hit enter to display results.'
raw_input()
cls()

display_results()
print
print
print 'Thanks for playing!'
print 'Hit y to quit.'
y = 'u'
while y != 'y' :
    y = msvcrt.getch()
