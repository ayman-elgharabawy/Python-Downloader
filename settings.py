
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

def init():
     
    global DownloadedFolder
    DownloadedFolder='downloaded'
    global templist
    templist=[]
    global download_counter
    download_counter=0