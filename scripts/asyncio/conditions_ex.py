import asyncio
import random

x=None 

# async def test_notify(condition_var):
#     await condition_var.acquire()
#     global x
    
#     while x == None:
#         print("testing notify---------------------")
#         await condition_var.wait()
        
#     print("done")
#     condition_var.release()
    
async def process_item(condition_var):
    await condition_var.acquire()  ######## Acquired Lock

    global x
    while x == None:
        print(f"Task : {asyncio.Task.current_task().name} tried to process item but it was not set. It'll wait for the condition.")
        await condition_var.wait()

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
        task.name=f"ProcessItem{i+1}"
        process_tasks.append(task)
    
    tasks=set_tasks + process_tasks
    # tasks.append(asyncio.create_task(test_notify()))
    ## Make main task wait for all other tasks (5 set items + 5 process items) to complete
    for task in tasks:
        await task
    
if __name__ == "__main__":
    asyncio.run(main())


