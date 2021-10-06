import asyncio
from datetime import datetime
import time 

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
    lock=asyncio.Semaphore(value=1)
    task1 = asyncio.create_task(Raise(lock,3))
    task2 = asyncio.create_task(Raise(lock,3))
    task3 = asyncio.create_task(Raise(lock,3))

    await task1
    await task2
    await task3

if __name__ == "__main__":
    print("Start Time : ", datetime.now(), "\n")
    start = time.time()

    asyncio.run(main())

    print("\nEnd   Time : ", datetime.now())
    print("\nTotal Time Taken : {} Seconds".format(time.time() - start))