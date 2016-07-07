
''' 
Created on July 7, 2016

@author: Ayman Elgharabawy
'''
from multiprocessing import Pool, TimeoutError
from StringIO import StringIO
import time
import os
import urllib2
import shutil
import multiprocessing
import string
from random import choice
import socket
from ctypes import c_int
import tempfile
import thread
from time import sleep
from Queue import Queue
from threading import Thread
import itertools
from multiprocessing import Pool
import logging 
import types
import multiprocessing


def init():
     
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