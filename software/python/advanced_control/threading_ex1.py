# This code is adapted from an example at 
# http://www.science.smith.edu/dftwiki/index.php/Python_Multithreading/Multiprocessing_Examples#Example_1
# PythonThreading_Example1.py
# D. Thiebaut
# Taken and adapted from
# https://pymotw.com/2/threading/
#
# Python program illustrating how threads can
# be created and started in Python

from __future__ import print_function
import threading
import time


def worker( Id ):
    #thread worker function.  It receives an Id,
    #and prints a message indicating it's starting.
    #waits 0.5 seconds, prints another message, and dies.
    print( 'Worker %d started\n' % Id )
    time.sleep( 0.5 )
    print( 'Worker %d finished\n' % Id )
    return

def main():
    """
    Spawns 5 threads that will run the worker function.
    Waits for the threads to finish, then stops.
    """
    threads = []
    for i in range(5):
        t = threading.Thread( target=worker, args=(i,) )
        threads.append(t)
        t.start()
    print( "Main has spawn all the threads" )

    # wait for all the threads to finish
    for t in threads:
        t.join()
        
    print( "Done!" )
    
main()
