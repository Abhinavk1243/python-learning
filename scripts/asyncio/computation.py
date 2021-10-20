import asyncio
from datetime import datetime
import time
import random


class SharedCounter:
    
    def __init__(self):
        self.even_available = asyncio.Event()
        self.odd_available = asyncio.Event()
        self.odd_available.set()
        
        
    async def print_odd(self):
        global limit
        global exit_prog
        global number

        while not exit_prog and number < limit:
            await self.odd_available.wait()
            print(f"Task : {asyncio.Task.current_task().name}  display : {number}")
            number = number + 1
            self.odd_available.clear()
            self.even_available.set()
            
    async def print_even(self):
        global limit
        global exit_prog
        global number

        while not exit_prog and number < limit:
            await self.even_available.wait()
            print(f"Task : {asyncio.Task.current_task().name} display : {number}")
            number = number + 1
            self.even_available.clear()
            self.odd_available.set()
            
            
class ProducerConsumer():
    
    def __init__(self,N):
        self.queue=asyncio.Queue(maxsize=N)
        self.producer_available=asyncio.Event()
        self.consumer_available=asyncio.Event()
        self.producer_available.set()
        self.max_size=N
        
    async def producer(self,no_of_item):
        
        for i in range(0,self.max_size+1):
        # for i in range(no_of_item):
            await self.producer_available.wait()
            if self.queue.full():
                print("Buffer is full , now producer wait for consumer to empty the buffer")
                self.producer_available.clear()
                self.consumer_available.set()
            # elif self.queue.full()==False and i<=no_of_item-1:
            else:
                item=random.randint(1,20)
                print(f"Producer-{i+1} produce : {item}")
                await self.queue.put(item)
                
            # else:
            #     item=random.randint(1,20)
            #     print(f"Producer-{i+1} produce : {item}")
            #     await self.queue.put(item)
            #     print("all items are produced")
            #     self.producer_available.clear()
            #     self.consumer_available.set()
                
        
    async def consumer(self,no_of_item):
        for i in range(0,self.max_size+1):
        # for i in range(no_of_item):
            await self.consumer_available.wait()
            if self.queue.empty():
                print("buffer is empty ,now consumer wait till the producer insert the items in buffer")
                # break
                self.producer_available.set()
                
                self.consumer_available.clear()
                
            # elif self.queue.empty()==False and i<=no_of_item-1:
            else:
                item = await self.queue.get()
                print(f"consumer-{i+1} consume : {item}")
            
            # else :
            #     print("all items ar e consumed ")
            #     item = await self.queue.get()
            #     print(f"consumer-{i+1} consume : {item}")
            
            
        
        
        
        
        
async def main():
    
    
    
    print(f"started at {time.strftime('%X')}")
    # sc=SharedCounter()
    # task1=asyncio.create_task(sc.print_odd())
    # task1.name = "print_odd"
    # task2=asyncio.create_task(sc.print_even())
    # task2.name = "print_even"
    
    prod_cons=ProducerConsumer(4)
    task3=asyncio.create_task(prod_cons.producer(8))
    task4=asyncio.create_task(prod_cons.consumer(8))
    # await task1
    # await task2
    await task3
    await task4
    print(f"finished at {time.strftime('%X')}")
        
if __name__ == "__main__":
    
    limit = 10
    exit_prog = False
    number = 1
    
    asyncio.run(main())

