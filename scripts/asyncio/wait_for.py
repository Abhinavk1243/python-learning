import asyncio
import time
from datetime import datetime
import random


x=None 

async def test_notify(condition_var):
    await condition_var.acquire()
    global x
    
    while x == None:
        print("testing notify---------------------")
        await condition_var.wait()
        
    print("done")
    condition_var.release()

def is_global_var_set():
    return x != None
async def process_item(condition_var):
    await condition_var.acquire()  ######## Acquired Lock

    global x
    
    # print(f"Task : {asyncio.Task.current_task().name} tried to process item but it was not set. It'll wait for the condition.")
    await condition_var.wait_for(is_global_var_set)

    print(f"Task : {asyncio.Task.current_task().name} processing an item : {x}")
    x = None

    condition_var.release() ######## Released Lock
    
async def set_item(condition_var,value):
    global x
    
    while x != None:
        print(f"Task : {asyncio.Task.current_task().name} tried to set item but its already set. It'll go to sleep for 2 seconds now.")
        await asyncio.sleep(2)
    
    await condition_var.acquire() ######## Acquired Lock
    x = value
    print(f"Task : {asyncio.Task.current_task().name} setting an item : {x}")
    condition_var.notify(n=1)

    condition_var.release()
        
    


async def main():
    condition_var = asyncio.Condition()

    set_tasks = []
    for i in range(5):
        task = asyncio.create_task(set_item(condition_var, random.randint(1,50)))
        task.name=f"SetItem{i+1}"
        set_tasks.append(task)

    process_tasks = []
    for i in range(5):
        task = asyncio.create_task(process_item(condition_var, ))
        task.name="ProcessItem%d"%(i+1)
        process_tasks.append(task)
    
    tasks=set_tasks + process_tasks
    ## Make main task wait for all other tasks (5 set items + 5 process items) to complete
    for task in set_tasks + process_tasks:
        await task
    
if __name__ == "__main__":
    print("Start Time : ", datetime.now(), "\n")
    start = time.time()
    asyncio.run(main())
    print("\nEnd   Time : ", datetime.now())
    print("\nTotal Time Taken : {} Seconds".format(time.time() - start))