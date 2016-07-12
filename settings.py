
''' 
Created on July 7, 2016

@author: Ayman Elgharabawy
'''
import time
import os
import multiprocessing
from ctypes import c_int
import types
import multiprocessing
import urllib2


def init():
    global status
    status=''
    global DownloadedFolder
    DownloadedFolder='downloaded'
    global templist
    templist=[]
    global download_counter
    download_counter=0
    global no_thread_link
    global no_thread_per_file
    no_thread_link=4
    no_thread_per_file=4 
    global shared_bytes_var
    shared_bytes_var = multiprocessing.Value(c_int, 0) # a ctypes var that counts the bytes already downloaded
