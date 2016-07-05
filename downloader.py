
from multiprocessing import Pool, TimeoutError
from StringIO import StringIO
import time
import os
import urllib2
import time
import multiprocessing
import string
from random import choice
import socket
from ctypes import c_int
import tempfile
import socket
import thread
import time
from time import sleep
from csv import DictReader
from Queue import Queue
from threading import Thread
from functools import partial
import pickle
import itertools
from multiprocessing import Pool
import time
import logging 
import copy_reg
import types
import multiprocessing



shared_bytes_var = multiprocessing.Value(c_int, 0) # a ctypes var that counts the bytes already downloaded

def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    if func_name.startswith('__') and not func_name.endswith('__'): #deal with mangled names
	cls_name = cls.__name__.lstrip('_')
	func_name = '_' + cls_name + func_name
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.__mro__:
	try:
	    func = cls.__dict__[func_name]
	except KeyError:
	    pass
	else:
	    break
    return func.__get__(obj, cls)

import copy_reg
import types
copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)


def progress_bar(progress, length=20):
    '''
    Function creates a textual progress bar.
    @param progress: Float number between 0 and 1 describes the progress.
    @param length: The length of the progress bar in chars. Default is 20.
    '''
    length -= 2 # The bracket are 2 chars long.
    return "[" + "#"*int(progress*length) + "-"*(length-int(progress*length)) + "]"






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
	    finally:
		# Mark this task as done, whether an exception happened or not
		self.tasks.task_done()


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads):
	self.tasks = Queue(num_threads)
	for _ in range(num_threads):
	    Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
	""" Add a task to the queue """
	self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
	""" Add a list of tasks to the queue """
	for args in args_list:
	    self.add_task(func, args)

    def wait_completion(self):
	""" Wait for completion of all the tasks in the queue """
	self.tasks.join()


def Is_ServerSupportHTTPRange(url, timeout=8):
    '''
    Function checks if a server allows HTTP Range.
    @param url: url address.
    @param timeout: Timeout in seconds.

    @return bool: Does server support HTTPRange?

    May raise urllib2.HTTPError, urllib2.URLError.
    '''
    url = url.replace(' ', '%20')

    fullsize = get_filesize(url)
    if not fullsize:
	return False

    headers = {'Range': 'bytes=0-3'}
    req = urllib2.Request(url, headers=headers)
    urlObj = urllib2.urlopen(req, timeout=timeout)

    meta = urlObj.info()
    filesize = int(meta.getheaders("Content-Length")[0])

    urlObj.close()
    return (filesize != fullsize)

def combine_files(parts, path):
    '''
    Function combines file parts.
    @param parts: List of file paths.
    @param path: Destination path.
    '''
    with open(path,'wb') as output:
	for part in parts:
	    with open(part,'rb') as f:
		output.writelines(f.readlines())
	    os.remove(part)



def createFilename(url, name, folder):
    dotSplit = url.split('.')
    if name == None:
	# use the same as the url
	slashSplit = dotSplit[-2].split('/')
	name = slashSplit[-1]
    ext = dotSplit[-1]
    file = '{}{}.{}'.format(folder, name, ext)
    return file  
    
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
	u = urllib2.urlopen(url, timeout=8)
    except (urllib2.HTTPError, urllib2.URLError) as e:
	logging.error(e)
	return 0
    meta = u.info()
    try:
	file_size = int(meta.getheaders("Content-Length")[0])
    except IndexError:
	return 0

    return file_size	
    
def is_ServerSupportHTTPRange(url):
	'''
	Function checks if a server allows HTTP Range.
	@param url: url address.
	@param timeout: Timeout in seconds.
	
	@return bool: Does server support HTTPRange?
	
	May raise urllib2.HTTPError, urllib2.URLError.
	'''
	url = url.replace(' ', '%20')
	fullsize = get_filesize(url)
	print 'fullsize ',fullsize
	if not fullsize:
		return False
	headers={'User-Agent' : "Magic Browser"} 
	#headers = {'Range': 'bytes=0-3'}
	req = urllib2.Request(url, headers=headers)
	urlObj = urllib2.urlopen(req, timeout=8)
		
	meta = urlObj.info()
	filesize = int(meta.getheaders("Content-Length")[0])
	
	urlObj.close()
	return (filesize != fullsize)
     
def _initProcess(x):
    multiprocessing.dummy.shared_bytes_var = x    

def get_rand_filename(dir_=os.getcwd()):  
    #"Function returns a non-existent random filename."
    return tempfile.mkstemp('.tmp', '', dir_)[1]


	
if __name__ == '__main__':
    
    downloader_no_thread=4
    #Thread pool for handling the images links
    pool = ThreadPool(downloader_no_thread)
    #Thread pool for handling download image chunk file
    pool2 = ThreadPool(downloader_no_thread)    
    
	
	
    def DownloadChunk(url, path, startByte=0, endByte=None):
    
	'''
	    Function downloads file.
	    @param url: File url address.
	    @param path: Destination file path.
	    @param startByte: Start byte.
	    @param endByte: End byte. Will work only if server supports HTTPRange headers.
	    @return path: Destination file path.
	     '''
	
	ShowProgress=True
	url = url.replace(' ', '%20')
	headers={'User-Agent' : "Magic Browser"}
	if endByte is not None:
	    headers['Range'] = 'bytes=%d-%d' % (startByte,endByte)
	req = urllib2.Request(url, headers=headers)
	try:
	    urlObj = urllib2.urlopen(req, timeout=8)
	except urllib2.HTTPError, e:
    
	    if "HTTP Error 416" in str(e):
		# HTTP 416 Error: Requested Range Not Satisfiable. Happens when we ask
		# for a range that is not available on the server. It will happen when
		# the server will try to send us a .html page that means something like
		# "you opened too many connections to our server". If this happens, we
		# will wait for the other threads to finish their connections and try again.
    
		#log.warning("Thread didn't got the file it was expecting. Retrying...")
		print("Thread didn't got the file it was expecting. Retrying...")
		time.sleep(5)
		return DownloadChunk(url, path, startByte, endByte, ShowProgress)
	    else:
		raise e
    
	f = open(path, 'wb')
	meta = urlObj.info()
	try:	
	    filesize = int(meta.getheaders("Content-Length")[0])
	except IndexError:
	    print("Server did not send Content-Length.")
	    logging.error("Server did not send Content-Length.")
	    ShowProgress=False
    
	filesize_dl = 0
	block_sz = 8192
	while True:
    
	    try:
		buff = urlObj.read(block_sz)
	    except (socket.timeout, socket.error, urllib2.HTTPError), e:
		multiprocessing.dummy.shared_bytes_var.value -= filesize_dl
		raise e
    
	    if not buff:
		break
    
	    filesize_dl += len(buff)
	    try:
		multiprocessing.dummy.shared_bytes_var.value += len(buff)
	    except AttributeError:
		pass
	    f.write(buff)
    
	    if ShowProgress:
		status = r"%.2f MB / %.2f MB %s [%3.2f%%]" % (filesize_dl / 1024.0 / 1024.0,
		                                              filesize / 1024.0 / 1024.0, progress_bar(1.0*filesize_dl/filesize),
		                                              filesize_dl * 100.0 / filesize)
		status += chr(8)*(len(status)+1)
		print status,	
    
	if ShowProgress:
	    print "\n"
    
	f.close()
	logging.info('writtten file',path)
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


	processes=downloader_no_thread
	path=None;
	minChunkFile=512**2;
	nonBlocking=False;
	filename=url.split('/')[-1]
	shared_bytes_var.value = 0
	url = url.replace(' ', '%20')
	if not path:
	    path = get_rand_filename(os.environ['temp'])
	    if not os.path.exists(os.path.dirname(path)):
		os.makedirs(os.path.dirname(path))
    
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}); 
	urlObj = urllib2.urlopen(req, timeout=8)
	meta = urlObj.info()
	filesize = int(meta.getheaders("Content-Length")[0])
	tempfilelist=[]
    
	
	if( filesize/processes > minChunkFile) and Is_ServerSupportHTTPRange(url):
	    args1 = []

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
		tempfilelist.append(path+".000");
	
	print("Running %d processes..." % processes)
	logging.info("Running %d processes..." % processes)

	pool2.map(lambda x: DownloadChunk(*x) , args1)
	
	while not pool2.tasks.all_tasks_done:
	    status = r"%.2f MB / %.2f MB %s [%3.2f%%]" % (shared_bytes_var.value / 1024.0 / 1024.0,
		                                          filesize / 1024.0 / 1024.0, progress_bar(1.0*shared_bytes_var.value/filesize),
		                                          shared_bytes_var.value * 100.0 / filesize)
	    status = status + chr(8)*(len(status)+1)
	    print status,
	    time.sleep(0.1)
	pool2.wait_completion()
	
	file_parts = tempfilelist
	combine_files(file_parts, filename)
	return 1	

###################################################################################################
    # Instantiate a thread pool with 5 worker threads

    # Add the jobs in bulk to the thread pool. Alternatively you could use
    # makes it possible to cancel the thread pool with an exception when
    # the currently running batch of workers is finished.
    print 'starting.....';
    lines = [line.rstrip('\n') for line in open('links.txt')]    
    pool.map(download, lines)
    pool.wait_completion()
    
    import logging
    logging.basicConfig(filename='downloader.log',level=logging.DEBUG)
   

    
