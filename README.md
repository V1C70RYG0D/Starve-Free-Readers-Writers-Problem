# Starve-Free-Readers-Writers-Problem

The Reader-Writer Problem is a classical problem in Computer Science in which a data structure, such as a database or storage area, is being accessed simultaneously by multiple processes concurrently. The critical section can only be accessed by one writer at any point in time, while multiple readers can simultaneously access it. To achieve this, we use semaphores to ensure there are no conflicts while accessing by writers and readers, and to properly synchronize the processes. However, this can give rise to starvation of either the readers or the writers, depending on their priorities.

The problem can be addressed using various solutions, but before diving into them, we should understand the basic implementation of a semaphore. A sample implementation can be found in the ```implementation.py``` file.

In this solution, we have described the classical solution followed by a starve-free solution. The starve-free solution is an efficient way to tackle the problem and ensures that neither the readers nor the writers starve. Finally, we have described an even faster starve-free solution that speeds up the reader process' execution in the critical section.

The Reader-Writer problem deals with synchronizing multiple processes, which are categorized into two types: Readers and Writers. Readers read data from a shared memory location, while Writers write data to the shared memory location.

## Implementation of Semaphore

The Semaphore is a synchronization construct used to protect shared resources from simultaneous access by multiple processes. It consists of an integer semaphore with a default value of 1 and a queue FIFO to store the processes that are blocked by the semaphore.

The Semaphore structure contains two functions, wait(int pID) and signal():

**wait(int pID)** - This function is used by a process that wants to access the shared resource. It checks if any resources are available by decrementing the semaphore value. If all resources are occupied, the function pushes the Process Control Block (PCB) corresponding to the process ID (pID) into the FIFO queue and blocks that process, thus, removing it from the ready queue.

**signal()** - This function is used by a process that has completed using a shared resource. It increments the semaphore value and checks if there are any processes in the FIFO queue waiting for execution. If there are any processes, it pops the first process from the queue and wakes it up by adding it to the ready queue.

Here's the Python code for the Semaphore structure:

```py
class Semaphore:
    def __init__(self, s=1):
        self.semaphore = s
        self.FIFO = Queue()

    def wait(self, pID):
        self.semaphore -= 1
        if self.semaphore < 0:
            self.FIFO.push(pID)
            pcb = self.FIFO.rear
            block(pcb)

    def signal(self):
        self.semaphore += 1
        if self.semaphore <= 0:
            pcb = self.FIFO.pop()
            wakeup(pcb)
```
**Explanation**

- The Semaphore class is defined with an initial value of 1 passed as an argument. If no value is passed, the default value is set to 1.

- The ``__init__`` function initializes two instance variables, ``semaphore`` and ``FIFO``. ``semaphore`` is used to keep track of the number of available resources, and ``FIFO`` is a queue used to store processes that are waiting to access the resource.

- The ``wait`` function is used to request access to the shared resource. It takes ``pID`` as an argument, which is the ID of the process requesting access to the resource.

- The function decrements the ``semaphore`` by 1, indicating that a resource has been requested.

- If the ``semaphore`` value is less than 0, it means that all resources are currently being used by other processes, and the requesting process must wait. In this case, the requesting process ID (``pID``) is added to the end of the ``FIFO`` queue, and a blocking function ``block(pcb)`` is called with the process control block (PCB) of the requesting process as an argument.

- The ``signal`` function is used to release a resource that is currently being used by a process. It increments the ``semaphore`` by 1, indicating that a resource has been released.

- If the ``semaphore`` value is less than or equal to 0, it means that there are processes waiting in the ``FIFO`` queue to access the resource. In this case, the first process in the ``FIFO`` queue is removed by calling the ``pop`` function, and a wakeup function ``wakeup(pcb)`` is called with the PCB of the process as an argument.

Overall, the implementation ensures that processes requesting access to a shared resource are queued in a FIFO manner and that no process is starved of accessing the resource indefinitely.


``Note that the block(pcb) and wakeup(pcb) functions used in the Semaphore's wait() and signal() functions respectively are not defined in the given code, so they should be defined elsewhere in the code or replaced with appropriate calls to the OS or threading library functions.``

## The Classical Solution

In the classical solution to the Reader-Writer's Problem, there are two Semaphores used to provide synchronization among the readers and writers. The first Semaphore, mutex, provides mutual exclusion to the readers while accessing the shared variable, counter. The second Semaphore, rw_mutex, ensures that only one writer accesses the shared memory resource at a time.

### Libraries and Variables

```py
from threading import Semaphore, Thread

mutex = Semaphore(1)      # semaphore to ensure mutual exclusion of readers
rw_mutex = Semaphore(1)   # semaphore to ensure exclusive access to shared resource by writers
counter = 0               # counter to keep track of active readers
```

### Reader Implementation

The implementation of the reader starts by acquiring the mutex lock. Once the mutex lock is acquired, the counter variable is incremented to keep track of the number of readers accessing the shared memory. If the current reader is the first reader, it acquires the rw_mutex lock to ensure that no writer process accesses the shared memory resource. Once the reader is done with the critical section, it decrements the counter variable and checks if it is the last reader. If it is the last reader, it releases the rw_mutex lock so that any waiting writer process can acquire it.

```py

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
```
**Explanation**

- The ``reader`` function takes ``processID`` as an input parameter and runs in an infinite loop, as indicated by the ``while True`` statement.

- The ``mutex`` and ``rw_mutex`` global variables are used to implement mutual exclusion between multiple reader and writer processes.

- In the entry section, the ``mutex`` lock is acquired using the ``acquire()`` method to ensure that only one process can access the counter variable at a time. The ``counter`` variable is incremented by 1 to indicate that a reader process is accessing the shared resource. If this is the first reader process (i.e., ``counter`` equals 1), the ``rw_mutex`` lock is acquired using the ``acquire()`` method to prevent any writer process from accessing the shared resource.

- In the critical section, the reader process reads from the shared resource, which is represented by the ``print()`` statement that displays a message indicating that the reader process is reading.

- In the exit section, the ``mutex`` lock is acquired again to ensure mutual exclusion while updating the ``counter`` variable. The ``counter`` variable is decremented by 1 to indicate that the reader process has finished accessing the shared resource. If this is the last reader process (i.e., ``counter`` equals 0), the ``rw_mutex`` lock is released using the ``release()`` method to allow any waiting writer process to access the shared resource.

- In the remainder section, the ``print()`` statement displays a message indicating that the reader process has finished reading. This section is not critical and does not require mutual exclusion.

- The ``while True`` loop ensures that the reader process keeps running indefinitely and can access the shared resource as needed.

### Writer Implementation

The implementation of the writer starts by acquiring the rw_mutex lock to ensure that no other reader or writer process is accessing the shared memory resource. Once the writer is done with the critical section, it releases the rw_mutex lock.

```py

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
```

**EXPLANATION**

- The ``writer`` function is a function that takes in a ``processID`` as its argument. This function is run by each writer process.

- The ``writer`` function consists of a while loop that runs indefinitely. This while loop is responsible for implementing the entry section, critical section, exit section, and remainder section of the writer process.

- In the entry section, the writer process acquires the ``rw_mutex`` semaphore. This semaphore ensures that only one writer can access the shared resource at a time.

- In the critical section, the writer process executes its writing operation on the shared resource. This is the section where the actual writing takes place.

- In the exit section, the writer process releases the ``rw_mutex`` semaphore, thereby allowing other writer processes to access the shared resource.

- In the remainder section, the writer process executes any additional code that is required after the writing operation is complete. In this case, it simply prints a message indicating that the writer process has finished writing.

- Overall, the ``writer`` function ensures that the writer processes have exclusive access to the shared resource while they are performing the writing operation.

The problem with this solution is that writers may starve. If there are several readers in the system, a writer may be blocked indefinitely because readers continuously acquire the rw_mutex lock. As a result, the writer never gets a chance to access the shared memory resource.

**TEST**
```py
# Test the solution with 2 readers and 1 writer
if __name__ == '__main__':
    r1 = Thread(target=reader, args=(1,))
    r2 = Thread(target=reader, args=(2,))
    w1 = Thread(target=writer, args=(1,))

    r1.start()
    r2.start()
    w1.start()
```



## Starve-Free Solution

The solution achieves this by introducing a third semaphore ```in_mutex```, which is used to ensure that all the processes requesting access to the resource are treated equally. When a process arrives to access the resource, it first acquires the ```in_mutex``` semaphore. This causes all subsequent arriving processes to be placed in a first-come, first-serve (FCFS) queue, regardless of whether they are readers or writers.

Once a process has acquired the ```in_mutex``` semaphore, it can then acquire the ```mutex``` semaphore. This semaphore is used to ensure mutual exclusion among the readers so that only one reader can update the ```counter``` variable at a time. If the ```counter``` variable is 1, it means the first reader has arrived and the process will then acquire the ```rw_mutex``` semaphore. This semaphore is used to ensure that no writer can enter the critical section when there are readers accessing the resource.

If a writer arrives when there are readers accessing the resource, it will wait on the ```rw_mutex``` semaphore until all the readers have exited the critical section. Once the writer is granted access to the resource, it will acquire the ```in_mutex``` semaphore to ensure that no other readers or writers can enter while it is writing to the shared resource.

The solution ensures that readers and writers are treated equally, as all arriving processes are placed in the FCFS queue of the ```in_mutex``` semaphore. This eliminates the possibility of starvation of either readers or writers.



### Libraries and Variables

```py
from threading import Semaphore

mutex = Semaphore(1)
rw_mutex = Semaphore(1)
in_mutex = Semaphore(1)
counter = 0
```

### Reader Implementation

```py
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
 ```
 ### Writer Implementation
 
 ```py
 
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
 ```
 
 **TEST**
 
 ```py
 # Start multiple reader and writer threads
for i in range(5):
    threading.Thread(target=reader).start()
    threading.Thread(target=writer).start()
```

## References

1. *Operating System Concepts*, Ninth Edition, Silberschatz, Galvin, Gagne 
2. *GFG*
3. [Stack-Overflow](https://stackoverflow.com/questions/2190090/how-to-prevent-writer-starvation-in-a-read-write-lock-in-pthreads)
4. [The Renegade Coder](https://therenegadecoder.com/code/solutions-to-the-readers-writers-problem/)
5. [University Of Maryland](https://www.cs.umd.edu/~hollings/cs412/s96/synch/synch1.html)


