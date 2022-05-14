import os 
import threading


# print(f"processs running at process id  : {os.getpid()}")

# total_threads = threading.active_count()
# thread_name = threading.current_thread().getName()
 
# print(f'Python is currently running {total_threads} thread(s)')
# print(f'The current thread is {thread_name}')

def print_thread():
    thread_name = threading.current_thread().getName()
    print(f"thread : {thread_name} is running----")
    

thread_1 = threading.Thread(target=print_thread)
thread_1.start()

total_threads = threading.active_count()
thread_name = threading.current_thread().getName()
 
print(f'Python is currently running {total_threads} thread(s)')
print(f'The current thread is {thread_name}')

thread_1.join()