import queue
import threading
import time
from tracemalloc import start
from turtle import update
import requests


def func(q, thread_no):
        while True:
            task = q.get()
            time.sleep(2)
            update()
            q.task_done()
            print(f'Thread #{thread_no} is doing task #{task} in the queue.')

def update():
    print ("queue_update")

    # def runMethod(q, thread_no):
    #     while True:
    #         task = q.get()
    #         time.sleep(2)

    #         q.task_done()
    #         print(f'Thread #{thread_no} is doing task #{task} in the queue.')
    
class Queue:    
    def __init__(self):
        print('queue_ini')

    def main(self):
        q = queue.Queue()

        for i in range(4):
            worker = threading.Thread(target=func, args=(q, i,), daemon=True)
            worker.start()

        # worker = threading.Thread(target=func, args=(q, 1,), daemon=True)
        # worker.start()
        # q.put(1)

        for j in range(10):
            q.put(j)
            
        q.join()

    if __name__ == "__main__":
        #main()
        print('queuemanager_main')