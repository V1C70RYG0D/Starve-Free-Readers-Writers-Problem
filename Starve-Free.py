from threading import Semaphore

mutex = Semaphore(1)
rw_mutex = Semaphore(1)
in_mutex = Semaphore(1)
counter = 0

def reader(processID):
    global counter
    while True:
        # Entry Section
        in_mutex.acquire()
        mutex.acquire()
        counter += 1
        if counter == 1:
            rw_mutex.acquire()
        mutex.release()
        in_mutex.release()

        # Critical Section

        # Exit Section
        mutex.acquire()
        counter -= 1
        if counter == 0:
            rw_mutex.release()
        mutex.release()

        # Remainder Section

def writer(processID):
   while True:
       # Entry Section
       in_mutex.acquire()
       rw_mutex.acquire()

       # Critical Section

       # Exit Section
       rw_mutex.release()
       in_mutex.release()

       # Remainder Section
      
# Start multiple reader and writer threads
for i in range(5):
   threading.Thread(target=reader).start()
   threading.Thread(target=writer).start()
