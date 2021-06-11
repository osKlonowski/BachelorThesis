import time
import threading
import random

rocket = 0


def func1():
    global rocket
    print('start func1')
    while rocket < 100:
        print("Im in func1")
        rocket += 1
        value = "Im global var "+str(rocket)+" from fun1"
        print(value)

    print('end func1')


def func2():
    global rocket
    print('start func2')
    while rocket < 100:
        print("Im in func2")
        rocket += 1
        value = "Im global var " + str(rocket) + " from fun2"
        print(value)
    print('end func2')


if __name__ == '__main__':
    p1 = threading.Thread(target=func1)
    p2 = threading.Thread(target=func2)
    p1.start()
    p2.start()
