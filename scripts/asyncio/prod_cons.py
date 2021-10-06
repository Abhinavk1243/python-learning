import asyncio
from datetime import datetime
import time 



# import threading, time
# from multiprocessing import Queue
# def producer(q, n):
#     for item in range(n):
#         q.put(item)
#         print(f"[Produced] {item}")
#         time.sleep(1)
#     print("[Producer] Done")
#     q.put(None)
# def consumer(q):
#     while True:
#         item = q.get()
#         if item is None:
#             break
#         print(f"[Consumer] {item}")
#         time.sleep(1)
#     print("[Consumer] Done")
# q = Queue()
# t1 = threading.Thread(target=lambda: producer(q, 10))
# t2 = threading.Thread(target=lambda: consumer(q))
# t1.start()
# t2.start()

import asyncio
from asyncio import Queue, sleep
async def producer(queue, n):
    
    for item in range(1,n):
    
        print(f"[Produced] {item}")
        await queue.put(item)
        await sleep(1)
    print("[Producer] Done")
    await queue.put(None)
    
async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"[Consumer] {item}")
        await sleep(1)
    print("[Consumer] Done")
    
async def main():
    n = 10
    queue = asyncio.Queue()
    producers=asyncio.create_task(producer(queue,n))
    consumers=asyncio.create_task(consumer(queue))
    await producers
    await consumers
    

asyncio.run(main())
    
    
# loop = asyncio.get_event_loop()
# loop.create_task(producer(q, n))
# loop.create_task(consu)