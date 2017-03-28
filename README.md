# Python-Downloader

You have to download retying package 

pip install retrying


##Algorithm:

<img src='https://github.com/ayman-elgharabawy/Python-Downloader/blob/master/Downloader.jpeg' />

the program has pool of threads (4 threads) that handle the downloading Tasks for each link in the file

for each thread which download the file has a a pool of thread (4 threads) to handle download file chunks.

-the downloaded files are stores in /downloaded folder.
-Classes folder contains the worker and hread pool classthat handle any task
There is Task file where i define the methods to be executed by worker thread
 - settings.py contains all the global variables and initialized bymainmethod
 - If reading/writting exception in chunk file due to remote server close connection , the worker will have delay 0.1 second and retry to download the chunk again.
 - if the random file name of chunk is repeated in another thread m it will choose another name

