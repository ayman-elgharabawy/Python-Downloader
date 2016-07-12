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

################################# Methods used as a task to be executed by worker ###############################################################

def DownloadChunk(url, path, startByte=0, endByte=None):

    '''
        Function downloads file.
        @param url: File url address.
        @param path: Destination file path.
        @param startByte: Start byte.
        @param endByte: End byte. Will work only if server supports HTTPRange headers.
        @return path: Destination file path.
         '''
    remotename=url.split('/')[-1]
    filename=path.split('\\')[-1]
    url = url.replace(' ', '%20')
    headers={'User-Agent' : "Magic Browser"}
    if endByte is not None:
        headers['Range'] = 'bytes=%d-%d' % (startByte,endByte)
    req = urllib2.Request(url, headers=headers)
    try:
        urlObj = DownloaderHelper.urlopen_with_retry(req)
    except urllib2.HTTPError, e:

        if "HTTP Error 416" in str(e):
            # HTTP 416 Error: Requested Range Not Satisfiable. Happens when we ask
            # for a range that is not available on the server. It will happen when
            # the server will try to send us a .html page that means something like
            # "you opened too many connections to our server". If this happens, we
            # will wait for the other threads to finish their connections and try again.

            #log.warning("Thread didn't got the file it was expecting. Retrying...")
            print "\n"
            print "Thread didn't got the file it was expecting. Retrying..."           
            time.sleep(5)
            return DownloadChunk(url, path, startByte, endByte)
        else:
            print "\n"
            print e            
            raise e

    f = open(path, 'wb')
    meta = urlObj.info()
    try:	
        filesize = int(meta.getheaders("Content-Length")[0])
    except IndexError:
        print "\n"
        print"Server did not send Content-Length."   
        logging.error("Server did not send Content-Length.")
        ShowProgress=False

    filesize_dl = 0
    block_sz = 8192
    while True:

        try:
            buff = urlObj.read(block_sz)
        except (socket.timeout, socket.error, urllib2.HTTPError), e:
            settings.shared_bytes_var.value -= filesize_dl
            print "\n"
            print 'Retrying to download chunk file..'
            time.sleep(5)
            DownloadChunk(url, path, startByte, endByte)             
            raise e
 

        if not buff:
            break

        filesize_dl += len(buff)
        try:
            settings.shared_bytes_var.value += len(buff)
        except AttributeError:
            print AttributeError
            pass
        try:
            f.write(buff)
        except:
            f.close()
            print "\n"
            print 'Retrying to download chunk file..' 
            DownloadChunk(url, path, startByte, endByte)

        
        settings.status = r"%.2f MB / %.2f MB %s [%3.2f%%]" % (filesize_dl / 1024.0 / 1024.0,
                                                           filesize / 1024.0 / 1024.0, DownloaderHelper.progress_bar(1.0*filesize_dl/filesize,remotename if (filesize_dl * 100.0 / filesize==100) else filename),
                                                           filesize_dl * 100.0 / filesize)
        settings.status += chr(8)*(len(settings.status)+1)
        print settings.status,	
    print "\n"
    f.close()
    logging.info(path)
    return path 



def download(url):
    '''
    Function downloads file parally.
    @param url: File url address.
    @param path: Destination file path.

    @param minChunkFile: Minimum chunk file in bytes.

    @return mapObj: Only if nonBlocking is True. A multiprocessing.pool.AsyncResult object.
    @return pool: Only if nonBlocking is True. A multiprocessing.pool object.
    '''	
    processes=settings.no_thread_per_file
    path=None;
    minChunkFile=1024**2;
    nonBlocking=False;
    filename=url.split('/')[-1]
    settings.shared_bytes_var.value = 0
    url = url.replace(' ', '%20')
    if not path:
        path = DownloaderHelper.get_rand_filename(os.environ['temp'])
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser","Connection": "keep-alive"});
    urlObj = DownloaderHelper.urlopen_with_retry(req)
    meta = urlObj.info()
    filesize = int(meta.getheaders("Content-Length")[0])


    if( filesize/processes > minChunkFile) and DownloaderHelper.Is_ServerSupportHTTPRange(url):
        args1 = []
        tempfilelist=[]
        pos = 0
        chunk = filesize/processes
        for i in range(processes):
            startByte = pos
            endByte = pos + chunk
            if endByte > filesize-1:
                endByte = filesize-1 
            args1.append([url, path+".%.3d" % i, startByte, endByte])
            tempfilelist.append(path+".%.3d" % i);
            pos += chunk+1
    else:
        args1 = [[url, path+".000", None, None]]
        tempfilelist=[path+".000"];

    #print 'Downloading... ',filename
    logging.info(url)
    logging.info(tempfilelist)
    #Thread pool for handling download image chunk file
    pool2 = ThreadPool(settings.no_thread_per_file)
    pool2.map(lambda x: DownloadChunk(*x) , args1)
    while not pool2.tasks.all_tasks_done:
        settings.status = r"%.2f MB / %.2f MB %s [%3.2f%%]" % (settings.shared_bytes_var.value / 1024.0 / 1024.0,
                                                      filesize / 1024.0 / 1024.0, DownloaderHelper.progress_bar(1.0*settings.shared_bytes_var.value/filesize ,filename),
                                                     settings.shared_bytes_var.value * 100.0 / filesize)
        settings.status = settings.status + chr(8)*(len(settings.status)+1)
        print settings.status,
        time.sleep(0.1)


    file_parts = tempfilelist
    pool2.wait_completion()
    settings.download_counter+=1
    DownloaderHelper.combine_files(file_parts, filename)
    return 1