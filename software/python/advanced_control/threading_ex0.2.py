# threading_ex0.2.py
# A program for learning about threads.  Explicitly defines two functions
# and calls them into threading.

from __future__ import print_function
import threading
import time

def workerA( Id ):
    myNumber = 0

    while(1):
        myNumber = myNumber + 1
        print("Worker__", Id, "counting:__", myNumber)
        time.sleep( 0.2 )

def workerB( Id ):
    myNumberB = 0
    # thread worker function.  It receives an Id,
    while(1):
        myNumberB = myNumberB + 1
        print("Worker", Id, "counting: ", myNumberB)
        time.sleep( 2 )

def main():
    # Spawns 5 threads that will run the worker function.
    # Waits for the threads to finish, then stops.
    threads = []

    t = threading.Thread( target=workerA, args=(1,) )
    threads.append(t)
    t.start()

    t2 = threading.Thread( target=workerB, args=(2,))
    threads.append(t2)
    t2.start()

    print( "Main has spawn all the threads." )

    t.join()
    t2.join()

    print( "Done!" )

main()
