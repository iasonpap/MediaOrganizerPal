import os, re, sys
import time
import inspect

def uniqify(my_list):
	return list(dict.fromkeys(my_list))


def wait(prompt=""):
    print(prompt)
    input("PRESS ANY KEY TO CONTINUE...")

def debug(message):
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    print(f'{time.ctime()}:{info.function}:{info.lineno}: {message}')

def int2string(num):
    num = round(num)
    if num < 10:
        out = f"0{num}"
    else:
        out = f"{num}"
    return out
        


