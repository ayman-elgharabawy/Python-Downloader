
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
    global proxyenable
    proxyenable=False
    global proxy_username
    global proxy_password
    global proxy_host
    global proxy_port
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
    ##############################################Init Methods ########################################
    shared_bytes_var = multiprocessing.Value(c_int, 0) # a ctypes var that counts the bytes already downloaded
    if proxyenable:
        proxy_handler = urllib2.ProxyHandler({'http': proxy_host+':'+proxy_port+'/'})
        proxy_auth_handler = urllib2.ProxyBasicAuthHandler()
        proxy_auth_handler.add_password('realm', proxy_host, proxy_username, proxy_password)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)    
