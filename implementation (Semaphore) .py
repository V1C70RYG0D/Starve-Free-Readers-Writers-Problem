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
