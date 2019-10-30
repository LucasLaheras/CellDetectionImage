"""""
        BUSCAR ITERTOOLS
"""""
import numpy as np

class CircularQueue:

    #Constructor
    def __init__(self):
        self.queue = list()
        self.tail = 0
        self.maxSize = 15
        self.iter = -1

    #Adding elements to the queue
    def enqueue(self, data):
        delta = self.tail - (self.iter + 1)
        for i in range(delta):
            self.queue.pop()

        if self.iter == self.maxSize-1:
            self.dequeue()

        self.queue.append(data)
        self.iter += 1
        self.tail = int(np.copy(self.iter+1))

        return True

    #Removing elements from the queue
    def dequeue(self):
        if self.tail == 0:
            return "None"
        data = self.queue[0]
        self.queue.pop(0)
        self.iter -= 1
        self.tail = int(np.copy(self.iter+1))
        return data

    def last(self):
        self.iter -= 1

        if self.iter < 0:
            return self.next()

        return self.queue[self.iter]

    def next(self):
        self.iter += 1

        if self.iter == self.maxSize or self.iter >= self.tail:
            return self.last()

        return self.queue[self.iter]

    def clear_all(self):
        self.__init__()
