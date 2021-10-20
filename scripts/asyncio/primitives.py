import asyncio
from asyncio.queues import Queue
from datetime import datetime
import time 
import random

x=3

# 1. from line 8 to line 32 is the example of using lock
async def non_primitives(y):
    global x 
    
    print(f"initial value of x = {x}")
    x_init=x
    
    for i in range(y-1):
        await asyncio.sleep(2)
        x=x*x_init
        
    print(f"final value of x = {x}")
    
async def Raise(lock, y):
    global x

    acquired = await lock.acquire()
    print(f"Value of X Initially : {x}")
    X_init = x
    for i in range(y-1):
        await asyncio.sleep(2)
        x *= X_init

    print(f"Value of X After Raise : {x}")

    lock.release()
        
async def producer(item,queue,condition_var):
    if queue.full():
        print(" -------------------------------------")
        print(f"| Buffer is full ,{asyncio.Task.current_task().name} will wait |")
        print(" -------------------------------------")
       
        await asyncio.sleep(2)
    
    await condition_var.acquire()
    print(f"{asyncio.Task.current_task().name} insert {item} in buffer")
    await queue.put(item)
    condition_var.notify(n=1)

    condition_var.release()
    

async def consumer(queue,condition_var):
    
    await condition_var.acquire()
    if queue.empty():
        print(" --------------------------------------")
        print(f"| Buffer is empty ,{asyncio.Task.current_task().name} will wait |")
        print(" --------------------------------------")
        await condition_var.wait()

    item=await queue.get()
    print(f"{asyncio.Task.current_task().name} consume the {item}")
    condition_var.release()
        
    
        
    
async def main():
    ### non primitive tasks
    
    # task1 = asyncio.create_task(non_primitives(3) )
    # task2 = asyncio.create_task(non_primitives(3) )
    # task3 = asyncio.create_task(non_primitives(3) )
    
    ### Primitives tasks
    
    # using Lock()
    # lock = asyncio.Lock()
    # task1 = asyncio.create_task(Raise(lock,3))
    # task2 = asyncio.create_task(Raise(lock,3))
    # task3 = asyncio.create_task(Raise(lock,3))
    
    # ## using Semaphores
    # lock=asyncio.Semaphore(value=1)
    # task1 = asyncio.create_task(Raise(lock,3))
    # task2 = asyncio.create_task(Raise(lock,3))
    # task3 = asyncio.create_task(Raise(lock,3))
    
    condition_var = asyncio.Condition()
    queue = asyncio.Queue(maxsize=4)
    set_tasks = []
    for i in range(5):
        task = asyncio.create_task(producer(random.randint(1,50),queue,condition_var))
        task.name=f"producer{i+1}"
        set_tasks.append(task)

    process_tasks = []
    for i in range(5):
        task = asyncio.create_task(consumer(queue,condition_var))
        task.name=f"consumer{i+1}"
        process_tasks.append(task)
        
    for task in set_tasks+process_tasks:
        await task
        
    # await task1
    # await task2
    # await task3

if __name__ == "__main__":
    print("===============START===================")
    print("Start Time : ", datetime.now())
    print("=======================================")
    start = time.time()

    asyncio.run(main())
    print("=======================================")
    print("End   Time : ", datetime.now())
    print("Total Time Taken : {} Seconds".format(time.time() - start))
    print("===============FINISH===================")