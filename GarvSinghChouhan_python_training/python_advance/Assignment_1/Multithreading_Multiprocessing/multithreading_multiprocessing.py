
import os
import time
import threading
import multiprocessing

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

#1 Write a program to create two threads that print numbers from 1 to 5 simultaneously.
def print_numbers(thread_name: str) -> None:
    """
    Print numbers from 1 to 5.
    """
    for number in range(1, 6):
        print(f"{thread_name}: {number}")
        time.sleep(0.5)


def threading_example() -> None:
    """
    Create two threads.
    """
    first_thread = threading.Thread(target=print_numbers,args=("Thread-1",))

    second_thread = threading.Thread(target=print_numbers,args=("Thread-2",))

    first_thread.start()
    second_thread.start()

    first_thread.join()
    second_thread.join()


#2 Create a thread that calculates the sum of numbers from 1 to 100.
def calculate_sum() -> None:
    """
    Calculate sum from 1 to 100.
    """
    total = sum(range(1, 101))

    print(f"Sum: {total}")


def thread_sum_example() -> None:
    """
    Create thread for summation.
    """
    sum_thread = threading.Thread(target=calculate_sum)

    sum_thread.start()
    sum_thread.join()


#3 Demonstrate the use of join() method in threading.
def demonstrate_join() -> None:
    """
    Demonstrate join().
    """

    def task() -> None:
        print("Thread Started")
        time.sleep(2)
        print("Thread Finished")

    worker_thread = threading.Thread(
        target=task
    )

    worker_thread.start()

    worker_thread.join()

    print("Main Thread Resumed")


#4 Create multiple threads to simulate file downloading using time.sleep().
def download_file(file_name: str) -> None:
    """
    Simulate file download.
    """
    print(f"Downloading {file_name}")

    time.sleep(2)

    print(f"Completed {file_name}")


def file_download_simulation() -> None:
    """
    Create multiple threads.
    """

    file_names = [
        "File1.pdf",
        "File2.pdf",
        "File3.pdf"
    ]

    threads = []

    for file_name in file_names:

        worker_thread = threading.Thread(
            target=download_file,
            args=(file_name,)
        )

        threads.append(worker_thread)

        worker_thread.start()

    for worker_thread in threads:
        worker_thread.join()

#5 Write a program to create two processes that print their Process IDs.
def print_process_id() -> None:
    """
    Print process ID.
    """
    print(
        f"Process ID: {os.getpid()}"
    )



def process_id_example() -> None:
    """
    Create two processes.
    """

    first_process = multiprocessing.Process(
        target=print_process_id
    )

    second_process = multiprocessing.Process(
        target=print_process_id
    )

    first_process.start()
    second_process.start()

    first_process.join()
    second_process.join()


#6 Write a multiprocessing program to calculate the square of numbers using Process class.
def calculate_square(number: int) -> None:
    """
    Calculate square.
    """
    print(
        f"Square of {number}: {number ** 2}"
    )


def multiprocessing_square_example() -> None:
    """
    Calculate squares using Process.
    """

    processes = []

    for number in [1, 2, 3, 4, 5]:

        process = multiprocessing.Process(target=calculate_square,args=(number,))

        processes.append(process)

        process.start()

    for process in processes:
        process.join()


#7 Convert a normal function into parallel execution using ThreadPoolExecutor.
def cube(number: int) -> int:
    """
    Calculate cube.
    """
    return number ** 3


def thread_pool_example() -> None:
    """
    Use ThreadPoolExecutor.
    """

    numbers = [1, 2, 3, 4, 5]

    with ThreadPoolExecutor(max_workers=3) as executor:

        results = executor.map(cube,numbers)

        print(list(results))


#8 Convert a normal function into parallel execution using ProcessPoolExecutor.
def square(number: int) -> int:
    """
    Calculate square.
    """
    return number ** 2


def process_pool_example() -> None:
    """
    Use ProcessPoolExecutor.
    """

    numbers = [1, 2, 3, 4, 5]

    with ProcessPoolExecutor(
        max_workers=3
    ) as executor:

        results = executor.map(
            square,
            numbers
        )

        print(
            list(results)
        )


def main() -> None:

    print("\nQuestion 1")
    threading_example()

    print("\nQuestion 2")
    thread_sum_example()

    print("\nQuestion 3")
    demonstrate_join()

    print("\nQuestion 4")
    file_download_simulation()

    print("\nQuestion 5")
    process_id_example()

    print("\nQuestion 6")
    multiprocessing_square_example()

    print("\nQuestion 7")
    thread_pool_example()

    print("\nQuestion 8")
    process_pool_example()


if __name__ == "__main__":
    main()