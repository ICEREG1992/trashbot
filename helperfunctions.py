import random
import time

def pick_string(set):
    return random.choice(set)

def bot_wait():
    time.sleep(1.5)

def bot_wait_long():
    time.sleep(3)

def bot_wait_short():
    time.sleep(.3)

def chance(rate):
    return random.uniform(0,100) < rate