#!/usr/env/python2

"""
Implements multi-threaded job handler that solves a classic network problem:
    When processing a network job, often there will be data transferred but at such a slow
    rate that the connection is in fact "hung". In this case, the thread should be considered
    as "dead", and another thread should be started.
    The "dead" thread is marked as so. If it eventually finishes its job, it will introspect
    its state and stop.
    A new thread is created in its place, so that there is always the same amount of "alive"
    threads working.
Good programming practice is to kill network job after a certain amount of time without receiving
any data.
"""

import datetime
import threading
import thread
import Queue
import time

__author__ = "j4v"
__copyright__ = "Copyright 2016, www"
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "j4v"
__email__ = "j4v@posteo.net"


class WorkerThread(threading.Thread):
    """
    Simple worker thread that processes queue of tasks by doing job
    """
    def __init__(self, queue, job):
        """
        :param queue: queue of tasks
        :param job: job that processes tasks
        """
        threading.Thread.__init__(self)
        self.queue = queue  # queue of jobs
        self.job = job  # the job to do
        self.last_job_start_time = None  # when did the last job start
        self.alive = True  # should the thread still be alive
        self.lock = thread.allocate_lock()  # lock on the thread

    def run(self):
        """
        Run the thread
        :return:
        """
        while self.alive and not self.queue.empty():
            # start timer
            self.lock.acquire()
            self.last_job_start_time = datetime.datetime.now()
            self.lock.release()
            # get next task
            task = self.queue.get()
            # process object
            self.job(task)
            # set task as completed
            self.queue.task_done()


class TimedThreadController:

    def __init__(self, max_job_time, worker_count, tasks, job):
        """
        :param max_job_time: how long a job should be allowed to run before it is considered
                             hanging
        :param worker_count: how many active workers should be working
        :param tasks: queue of tasks
        :param job: job to process trask
        """
        self.max_job_time = max_job_time
        self.worker_count = worker_count
        self.tasks = tasks
        self.job = job

    def run(self):
        """
        Run threads that will do job until all tasks are done
        :return:
        """
        # start threads
        worker_threads_list = []
        for i in range(self.worker_count):
            worker = WorkerThread(self.tasks, self.job)
            worker.daemon = True
            worker_threads_list.append(worker)
            worker.start()

        # keep going as long as at least one worker is alive
        is_some_worker_alive = True
        while is_some_worker_alive:
            is_some_worker_alive = False
            dead_worker_list = []  # list of workers to remove after iterating
            for worker in worker_threads_list:
                # check if alive
                if worker.alive:
                    is_some_worker_alive = True
                    # get time elapsed since started
                    worker.lock.acquire()
                    worker_last_job_start_time = worker.last_job_start_time
                    worker.lock.release()
                    time_elapsed = datetime.datetime.now() - worker_last_job_start_time \
                        if worker_last_job_start_time else None
                    # check if exceeded max allowed time
                    if time_elapsed and time_elapsed.seconds > self.max_job_time:
                        # exceeded -> kill and remove from list of active threads
                        worker.alive = False
                        dead_worker_list.append(worker)
                # dead -> remove from list of active threads
                else:
                    dead_worker_list.append(worker)
            # remove dead workers from thread list
            for worker in dead_worker_list:
                worker_threads_list.remove(worker)
                # add workers if there are still tasks to be done and less workers then max
                if len(worker_threads_list) <= self.worker_count and not self.tasks.empty():
                    # start a new thread
                    new_worker = WorkerThread(self.tasks, self.job)
                    new_worker.daemon = True
                    worker_threads_list.append(new_worker)
                    new_worker.start()


# example function
def print_input(i):
    print i
    time.sleep(100)


def main():

    # create queue with jobs
    tasks = Queue.Queue()
    for i in range(1, 10):
        tasks.put(i)

    # create and start timed controller
    timed_thread_controller = TimedThreadController(max_job_time=3,
                                                    worker_count=1,
                                                    tasks=tasks,
                                                    job=print_input)
    timed_thread_controller.run()


if __name__ == "__main__":
    main()
