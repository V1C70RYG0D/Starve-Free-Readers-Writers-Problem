from threading import Semaphore, Thread

mutex = Semaphore(1)      # semaphore to ensure mutual exclusion of readers
rw_mutex = Semaphore(1)   # semaphore to ensure exclusive access to shared resource by writers
counter = 0               # counter to keep track of active readers

def reader(processID):
    global counter
    
    while True:
        # Entry section
        mutex.acquire()
        counter += 1
        if counter == 1:
            rw_mutex.acquire()
        mutex.release()

        # Critical section
        print(f"Reader {processID} is reading...")

        # Exit section
        mutex.acquire()
        counter -= 1
        if counter == 0:
            rw_mutex.release()
        mutex.release()

        # Remainder section
        print(f"Reader {processID} finished reading.")
        
def writer(processID):
    while True:
        # Entry section
        rw_mutex.acquire()

        # Critical section
        print(f"Writer {processID} is writing...")

        # Exit section
        rw_mutex.release()

        # Remainder section
        print(f"Writer {processID} finished writing.")
        
        
# Test the solution with 2 readers and 1 writer
if __name__ == '__main__':
    r1 = Thread(target=reader, args=(1,))
    r2 = Thread(target=reader, args=(2,))
    w1 = Thread(target=writer, args=(1,))

    r1.start()
    r2.start()
    w1.start()
