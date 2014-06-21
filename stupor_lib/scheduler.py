"""
Library for job scheduling and execution
"""
import multiprocessing

class Worker(multiprocessing.Process):
    def __init__(self, worker_queue):
        multiprocessing.Process.__init__(self)
        self.worker_queue = worker_queue

    def run(self):
        if not self.client_queue.empty():
            job = self.worker_queue.get()
            return job.run()
        else:
            return None

class Scheduler():
    def __init__(self):
        pass