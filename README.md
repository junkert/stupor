Stupor
======

Stupor is a duplicate file detector written in Python 3.4 that is able to detect
duplicate files on any mounted file system under Linux or Unix variants such as
OS X and BSD. To use stupor please see below for examples.

Design
======

Stupor is a combination of single threaded and multithreaded algorithms used to
detect duplicate files.

The first algorithm is contained in the crawler class and is located in the
crawler library under stupor_lib/crawler.py. This class wraps the 'find' command
which is one of the more efficient methods in building a list of files under a
specific location. Once the class is instantiated we call the 'crawl_path'
method which crawls the filesystem and returns a list of files.

Once we have a list of files we can then start processing each file separately
and in parallel. To do this we create a thread pool to calculate the MD5 value
of each file. To calculate the MD5 we first read in a "chunk" (or block) of the
file into a character list and then use the MD5 library to calculate the file's
checksum.

After the checksum is calculated the thread returns the path to the file and the
calculated checksum. If the file and checksum are not located in the duplicate
files dictionary we add it to the dictionary with the key as the checksum and
file path as the value. If the key exists already then we have detected a
duplicate. In this case we append the path of the file to the other value. Each
value stored in the dictionary is stored inside the value list for that key. If
there is only one path for a key then we assume there are no duplicates to this
file. Therefore any key's value that has a length greater than one is assumed to
be a duplicate file.


Requirements
============

Python >= 3.4


Examples
========

Set chunk size of 1GB:
./stupor -p /tmp -o ~/duplicates.txt -c 1024

Set thread count to 16 (default is 4):
./stupor -p /tmp -o ~/duplicates.txt -t 16

Defaults:
./stupor -p /tmp -o ~/duplicates.txt
