import asyncio
from asyncio.tasks import sleep
import requests
import time
import contextvars
import functools
import aiohttp
import base64
from library import read_config
import ssl

base_url="http://127.0.0.1:5000"
# def read_db():
x=2
async def cond_1(condition_var):
    await condition_var.acquire()
    global x 
    while x !=3 :
        print("task cond1 is waiting for x = 3 ")
        await condition_var.wait()
    
    print("wait is over for task : cond1 and start processing ")
    condition_var.release()
    
    
async def cond_2(condition_var):
    await condition_var.acquire()
    global x 
    while x !=3 :
        print("task cond2 is waiting for x = 3 ")
        await condition_var.wait()
    
    print("wait is over for task : cond2 and start processing ")
    condition_var.release()
    
async def set_x(condition_var):
    await condition_var.acquire() ######## Acquired Lock
    global x 
    for i in range(5):
        x=i
        
        print(f"task3 set value of x = {x}, {i}")
        if x==3:
            print(x == 3)
            # condition_var.notify()
            condition_var.notify_all()
            condition_var.release()
            await asyncio.sleep(2)
        else:
            await asyncio.sleep(2)
        
    
    # condition_var.release()  


def get_token():
    
    API_CLIENT=read_config.get_config('client-cred','client_key',file_name="oauth2_cred.cfg")
    API_SECRET=read_config.get_config('client-cred','client_secret',file_name="oauth2_cred.cfg")
        
    # Encode ID and SECRET in Base64
    base64_basicAuth = (API_CLIENT + ':'+ API_SECRET) .encode("ascii")
    base64_basicAuth = base64.b64encode(base64_basicAuth) 
        
    # Decode ID and SECRET in Base64 for getting 
    base64_basicAuth = base64_basicAuth.decode("ascii") 
    base64_basicAuth = 'Basic ' + base64_basicAuth
    headers = {
        'authorization': base64_basicAuth,
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded'
        }

    params = {
        'grant_type': 'password',
        'username' : 'admin',
        'password': 'admin12'
        }

    auth_url = f"{base_url}/oauth/token"
    api_request = requests.request("POST", auth_url, headers=headers, params = params)
    api_request = api_request.json()
    return api_request["access_token"]

async def req(url):
    # token=get_token()
    
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            data = await response.json()
            print(data)
    
    
async def fetch(session, url):
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        return await response.json()


async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results


async def print_odd():
    for i in range(1,10,2):
        print(i)
        # await asyncio.sleep(1)
        
        for j in range(1000):
            a=1
        await asyncio.sleep(1)

async def print_even():
    for i in range(2,11,2):
        print(i)
        # await asyncio.sleep(1)
        for j in range(800):
            b=1
        await asyncio.sleep(1)

async def factorial(name, number):
    fact = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        fact *= i
    print(f"Task {name}: factorial({number}) = {fact}")
    return fact

async def say_after(delay, what):
    # await asyncio.sleep(delay)
    print(what)
    await asyncio.sleep(delay)
    
async def function1(text):
    await asyncio.sleep(1)
    print(text)
    # await asyncio.sleep(1)
    print("hello")
    

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 5000)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()
    
async def main():
    # text="doing with synchronization"
    
    # # await function1(text)
    # # task=asyncio.create_task(function1(text))
    # await function1(text)
    # # await task
    # # await asyncio.sleep(0.5)
    
    # print("finished execution")
    print(f"started at {time.strftime('%X')}")

    # await say_after(1, 'hello')
    # await say_after(2, 'world')
    
    # task1=asyncio.create_task(say_after(2, 'hello'))
    # task2=asyncio.create_task(say_after(3, 'world'))
    # await asyncio.sleep(4)
    # await task2
    # await task1
    
    # starttime=time.time()
    # urls=["https://reqres.in/api/users/2","https://reqres.in/api/users/3","https://reqres.in/api/users/4","https://reqres.in/api/users/5"]
    # data=await  fetch_all(urls)
    # print(data)
    
    concurrent_task = await asyncio.gather(
        # factorial("A", 2),
        # factorial("B", 3),
        # # await to_thread(read_file),
        # factorial("C", 4),
        print_odd(),
        print_even(),
        # req()
    )
    # # print(concurrent_task)
    
    
    # condition_var = asyncio.Condition()
    # task1=asyncio.create_task(cond_1(condition_var))
    # task2=asyncio.create_task(cond_2(condition_var))
    # task3=asyncio.create_task(set_x(condition_var))
    
    # await task1
    # await task2
    # await task3
    
    
    
    
    print(f"finished at {time.strftime('%X')}")
    
if __name__ == "__main__":
    asyncio.run(main())
    # main()
    # asyncio.run(tcp_echo_client('Hello World!'))