#!/usr/bin/env python3
import time
import os
import copy
from datetime import datetime
from sys import exit
from optparse import OptionParser
from concurrent import futures
from hashlib import md5
from stupor_lib.crawler import Crawler

file_list = []
chunk_size = 1 * 1024 * 1024

def opt_parse():
    parser = OptionParser()

    parser.add_option("-c",
                      "--chunk",
                      default=1,
                      type='int',
                      help="Chunk size in MB. [DEFAULT: 1]")
    parser.add_option("-p",
                      "--path",
                      default=None,
                      help="Path to crawl.")
    parser.add_option("-o",
                      "--output",
                      default=None,
                      help="File to store duplicate ")
    parser.add_option("-t",
                      "--threads",
                      default=4,
                      type='int',
                      help=("Number of threads to read concurrent files."
                            " [DEFAULT: 4]"))

    (opts, args) = parser.parse_args()

    if not opts.path and not opts.output:
        parser.error("Please add a -p and -o flag when executing or -h for "
                     "help.")
    return parser.parse_args()

def hash(file_path):
    global chunk_size
    if os.path.exists(file_path):
        f = open(file_path, 'rb+')
        file_hash = md5(f.read(chunk_size)).hexdigest()
        f.close()
    else:
        file_hash = None
    return (file_hash, file_path)

def main():
    global file_list, chunk_size
    duplicate_files = {}
    opts, args = opt_parse()
    chunk_size = 1024 * 1024 * opts.chunk # Number of MB to MD5

    # Start timers for performance tests
    start_time = time.time()
    print("Start time: %s" % datetime.now())
    print("")

    # Use a single thread to crawl the filesystem for file paths
    # and throw them into a set()
    print("Crawling filesystem and collecting a file list . . . ")
    crawler = Crawler()
    file_list = crawler.crawl(opts.path)
    crawler_time = time.time() - start_time
    print("Crawler time: %f seconds" % crawler_time)

    # Now execute in parallel MD5 jobs.
    # concurrency = 1 file : 1 process.
    duplicate_time = time.time()
    print("Identifying duplicates . . . ",)
    with futures.ThreadPoolExecutor(max_workers=opts.threads) as executor:
        try:
            for proc in zip(file_list,
                            executor.map(hash, file_list)):
                file_hash, file_path = proc[1]
                if not file_hash or not file_path:
                    continue
                # Used to debug threads
                # print("%s\n%s\n\n" % (file_hash, file_path))
                if file_hash not in duplicate_files:
                    duplicate_files[file_hash] = [file_path]
                else:
                    duplicate_files[file_hash].append(file_path)

        # TODO: Find out why this exception is being thrown
        except IsADirectoryError as e:
            pass

    print("Duplicate detect time: %f seconds" % (time.time() - duplicate_time))
    # Write to output file
    counter = 0
    with open(opts.output, 'w') as f:
        for row in duplicate_files:
            if len(duplicate_files[row]) > 1:
                counter += 1
                files = ','.join(duplicate_files[row])
                f.write("%s,%s\n" % (row, files))

    # Print statistics to screen
    stop_time = time.time()
    duration = stop_time - start_time
    print("")
    print("Number of files: %d" % len(file_list))
    print("Stop time: %s" % str(datetime.now()))
    print("Duplicate file count: %d" % counter)
    print("Total Runtime: %f" % duration)
    return True

if __name__ == "__main__":
    # Change to BASH return codes:
    # 0   -> True
    # 1   -> False
    # > 1 -> That value
    val = main()
    if val == 'False' or val == '0':
        exit(1)
    elif val == 'True' or val == '1':
        exit(0)
    else:
        exit(int(val))
