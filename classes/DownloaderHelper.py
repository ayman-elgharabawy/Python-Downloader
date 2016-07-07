
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
import settings

    
class DownloaderHelper(object):
    
    @staticmethod
    def progress_bar(progress, length=20):
        '''
        Function creates a textual progress bar.
        @param progress: Float number between 0 and 1 describes the progress.
        @param length: The length of the progress bar in chars. Default is 20.
        '''
        length -= 2 # The bracket are 2 chars long.
        return "[" + "#"*int(progress*length) + "-"*(length-int(progress*length)) + "]"
    
    
    @staticmethod
    def Is_ServerSupportHTTPRange(url, timeout=20):
        '''
        Function checks if a server allows HTTP Range.
        @param url: url address.
        @param timeout: Timeout in seconds.
    
        @return bool: Does server support HTTPRange?
    
        May raise urllib2.HTTPError, urllib2.URLError.
        '''
        url = url.replace(' ', '%20')
    
        fullsize = self.get_filesize(url)
        if not fullsize:
            return False
    
        #headers = {'Range': 'bytes=0-3'}
        headers={'User-Agent' : "Magic Browser"}
        req = urllib2.Request(url, headers=headers)
        urlObj = urlopen_with_retry(req)
    
        meta = urlObj.info()
        filesize = int(meta.getheaders("Content-Length")[0])
    
        urlObj.close()
        return (filesize != fullsize)
    
    @staticmethod    
    def combine_files(parts, path):
        '''
        Function combines file parts.
        @param parts: List of file paths.
        @param path: Destination path.
        '''
        destination=settings.DownloadedFolder+'/'+path
        if not os.path.exists(os.path.dirname(destination)):
            try:
                os.makedirs(os.path.dirname(destination))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise    
        with open(destination,'wb') as output:
            for part in parts:
                with open(part,'rb') as f:
                    output.writelines(f.readlines())	
                os.remove(part)
        settings.download_counter+=1	    
    
    
    @staticmethod
    def createFilename(url, name, folder):
        dotSplit = url.split('.')
        if name == None:
            # use the same as the url
            slashSplit = dotSplit[-2].split('/')
            name = slashSplit[-1]
        ext = dotSplit[-1]
        file = '{}{}.{}'.format(folder, name, ext)
        return file  
    
    @staticmethod
    def get_filesize(url):
        '''
        Function fetches filesize of a file over HTTP.
        @param url: url address.
        @param timeout: Timeout in seconds.
    
        @return bool: Size in bytes.
        '''
        #if isinstance(url, utils.classes.MetaUrl):
            #url = url.url
    
        url = url.replace(' ', '%20')
        try:
            u = urlopen_with_retry(url)
        except (urllib2.HTTPError, urllib2.URLError) as e:
            logging.error(e)
            return 0
        meta = u.info()
        try:
            file_size = int(meta.getheaders("Content-Length")[0])
        except IndexError:
            return 0
    
        return file_size	
    
    @staticmethod
    def _initProcess(x):
        multiprocessing.dummy.shared_bytes_var = x    
    
    @staticmethod
    def get_rand_filename(dir_=os.getcwd()):
        
        #"Function returns a non-existent random filename."
        name=tempfile.mkstemp('.tmp', '', dir_)[1]
        if name in settings.templist:
                #os.path.exists(os.environ['temp']+name):
            self.get_rand_filename(os.environ['temp'])
        settings.templist.append(name)	
        return name
    
    @staticmethod
    @retry(stop_max_attempt_number=7)
    def urlopen_with_retry(url):
        return urllib2.urlopen(url,timeout=20)    