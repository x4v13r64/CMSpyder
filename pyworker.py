#!/usr/bin/python3

import datetime
import threading
import _thread  # todo: figure out how to use only threading instead
import queue

import time


def print_input(input):
    time.sleep(20)
    print(input)


class WorkerThread(threading.Thread):
    def __init__(self, queue, job):
        threading.Thread.__init__(self)
        self.queue = queue  # queue of jobs
        self.job = job  # the job to do
        self.last_job_start = None  # when did the last job start
        self.alive = True  # should the thread still be alive
        self.lock = _thread.allocate_lock()  # lock on the thread

    def run(self):
        while True:
            if self.alive and not self.queue.empty():
                task = self.queue.get()  # get next task
                # start timer
                self.lock.acquire()
                self.last_job_start = datetime.datetime.now()
                self.lock.release()
                # process object
                self.job(task)
                # set task as completed
                self.queue.task_done()
            else:  # dead or queue empty
                break  # exit thread


def main():
    job_time_max = 1  # maximum time that any worker can pass on a job
    worker_count = 5  # max number of workers
    task_queue = queue.Queue()
    worker_threads_list = []

    # todo: fill queue
    for i in range(1, 100):
        task_queue.put(i)

    # start threads
    for i in range(worker_count if task_queue.qsize() > worker_count else task_queue.qsize()):
        worker = WorkerThread(task_queue, print_input)
        worker.daemon = True
        worker_threads_list.append(worker)
        worker.start()

    is_some_worker_alive = True
    # keep going as long as at least one worker is alive
    while is_some_worker_alive:
        is_some_worker_alive = False
        dead_worker_list = []  # necessary so that we only remove after iterating (not while)
        for worker in worker_threads_list:
            # todo: error, checking if it is Alive, not alive
            if worker.isAlive():
                is_some_worker_alive = True
                worker.lock.acquire()
                last_job_start_time = worker.last_job_start
                worker.lock.release()
                difference = datetime.datetime.now() - last_job_start_time if last_job_start_time else None
                # check if exceeded max allowed time
                if last_job_start_time and difference.seconds > job_time_max:
                    worker.alive = False
                    # todo: could create new thread after the other one is dead
            else:
                print(2)
                dead_worker_list.append(worker)
        # now we can safely remove them
        for worker in dead_worker_list:
            print("killing %s" % worker)
            worker_threads_list.remove(worker)

if __name__ == "__main__":
    main()