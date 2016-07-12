
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
from classes.DownloaderHelper import DownloaderHelper
from classes.ThreadPool import ThreadPool
from classes.Worker import Worker
import settings
import Tasks


logfile='downloader.log'
################################################################################################################################################	
if __name__ == '__main__':

    settings.proxyenable=False
    settings.proxy_host='10.230.233.30'
    settings.proxy_port='5110'
    settings.proxy_username='mattia17'
    settings.proxy_password='VodaPass18'
    settings.init()
    #Thread pool for handling the images links
    pool = ThreadPool(settings.no_thread_link)
    logging.basicConfig(filename=logfile,level=logging.DEBUG)
    with open(logfile, 'w'):
        pass
    if os.path.exists(settings.DownloadedFolder):
        shutil.rmtree(settings.DownloadedFolder)
    print 'starting.....';
    logging.info('Starting..');
    lines = [line.rstrip('\n') for line in open('links.txt')]
    pool.map(Tasks.download, lines)
    pool.wait_completion()
    print 'Total files downloaded',settings.download_counter
    logging.info('Total files downloaded %d',settings.download_counter)    
