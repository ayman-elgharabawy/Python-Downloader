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
import random
from retrying import retry
from DownloaderHelper import DownloaderHelper



shared_bytes_var = multiprocessing.Value(c_int, 0) # a ctypes var that counts the bytes already downloaded

class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                # An exception happened in this thread
                print(e)
                logging.error(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()

