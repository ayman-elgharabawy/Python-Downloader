# Python-Downloader

You have to download retying package 

pip install retrying


##Algorithm:

the program has pool of threads that handle the downloading Tasks for each link in the file

for each thread which download the file has a a pool of thread to handle download file chunks

-the downloaded files are stores in /downloaded folder.
-Classes folder contains the worker and hread pool classthat handle any task
There is Task file where i define the methods to be executed by worker thread
 - settings.py contains all the global variables and initialized bymainmethod

