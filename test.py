import threading
import time


# Пример функции 1
def function1():
    for i in range(5):
        print("Функция 1 выполняется")
        time.sleep(1)


# Пример функции 2
def function2():
    for i in range(5):
        print("Функция 2 выполняется")
        time.sleep(1)


# Создаем потоки
thread1 = threading.Thread(target=function1)
thread2 = threading.Thread(target=function2)

# Запускаем потоки
thread1.start()
thread2.start()

# Ждем завершения потоков
thread1.join()
thread2.join()

print("Обе функции завершены.")
