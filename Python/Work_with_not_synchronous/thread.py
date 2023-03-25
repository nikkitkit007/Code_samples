# ----------------------info----------------------
# getName() - получить имя потока
# getPriority() - получить приоритет потока
# isAlive() - определить, выполняется ли поток
# join() - ожидать завершение потока
# sleep() - приостановить поток на заданное время
# start() - запустить поток
# ----------------------info----------------------

import time
from threading import Thread
from time import sleep

def simple_timer(time):                         # really simple timer
    print("Set timer on %d seconds"%(time))
    sleep(time)
    return False


def thread_life(thread_name):
    print(str(thread_name) + " " + str(time.monotonic()))
    sleep(1)
    global_thread_list.append(str(thread_name))
    return False

if __name__ == "__main__":
    print("- - - - - - - Work with threads! - - - - - - -")
    threads = []
    thread_count = 10
    global_thread_list = []

    for i in range(thread_count):
        th = Thread(target = thread_life, args = (i,))
        threads.append(th)
        th.start()
        sleep(0.5)

    [thread.join() for thread in threads]
    print("Threads: " + str(global_thread_list))                # so we get info from thread

    print("Program continue works...")
    
    timer_time = 0
    dicision = input("If you want to set timer, write 'y': ")
    if dicision == 'y':
        timer_time = int(input("Please, write time for timer in seconds: "))

    if timer_time != 0:
        th = Thread(target = simple_timer, args = (timer_time,))
        th.start()
        
        print("Time now is: " + str(time.monotonic()))
        th.join()
        print("Time now is: " + str(time.monotonic()))
        print("Continue working...")