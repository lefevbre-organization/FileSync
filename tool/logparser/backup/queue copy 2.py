import queue
import threading
import time
import requests

def func(q, thread_no):
    while True:
        task = q.get()
        time.sleep(2)
        update()
        q.task_done()
        print(f'Thread #{thread_no} is doing task #{task} in the queue.')

def update():
 # Create a new resource
        #time.sleep(20)
        response = requests.post('https://httpbin.org/post', data = {'key':'value'})
        #print (response)
        # Update an existing resource
        # requests.put('https://httpbin.org/put', data = {'key':'value'})
        # print (response)

        if (response.status_code == 200):
            print("The request was a success!")
        # Code here will only run if the request is successful
        elif (response.status_code) == 404:
            print("Result not found!")
            # Code here will react to failed requests

# def runMethod(q, thread_no):
#     while True:
#         task = q.get()
#         time.sleep(2)

#         q.task_done()
#         print(f'Thread #{thread_no} is doing task #{task} in the queue.')

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