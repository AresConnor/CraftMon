import functools
import logging
import threading
import time
import warnings


class Task:
    def __init__(self, name, function, *args, **kwargs):
        self.name = name
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.result_lock = threading.Lock()

    def run(self):
        result = self.function(*self.args, **self.kwargs)

        self.result_lock.acquire()
        self.result = result
        self.result_lock.release()

        return self.result

    def get_result(self):
        if self.result is None:
            return self.run()
        else:
            self.result_lock.acquire()
            result = self.result
            self.result_lock.release()
            return result


class Fetcher:
    def __init__(self, interval, logger:logging.Logger):
        self.interval = interval
        self.tasks: dict[str, Task] = {}
        self.tasks_lock = threading.Lock()

        self.logger = logger
        self.run_tasks()
        self.init_timer()


    def get(self, task_name, function: functools.partial, *args, **kwargs):
        if task_name not in self.tasks:
            self.tasks_lock.acquire()
            self.tasks[task_name] = Task(task_name, function, *args, **kwargs)
            self.tasks_lock.release()
        return self.tasks[task_name].get_result()

    def init_timer(self):
        timer = threading.Timer(self.interval, self.run_tasks)
        timer.daemon = True
        timer.start()

    def run_tasks(self):
        begin = time.time()
        print(f"Fetcher: Running tasks...")
        self.tasks_lock.acquire()
        for task in self.tasks.values():
            try:
                task.run()
            except Exception as e:
                warnings.warn(f"Fetcher: Error while running task {task.name}: {e}")
        print(f"Fetcher: Finished running {len(self.tasks)} tasks in {time.time() - begin:.2f}s.")
        self.tasks_lock.release()

        self.init_timer()
