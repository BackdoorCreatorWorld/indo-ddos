#!/usr/bin/env python3
"""
Thread Manager
Thread control and management
"""

import threading
import queue
import time

class ThreadController:
    def __init__(self, max_threads=99999):
        self.max_threads = max_threads
        self.active_threads = 0
        self.thread_pool = []
        self.task_queue = queue.Queue()
        self.lock = threading.Lock()
        self.running = False
        
    def start_workers(self, target_func, num_workers, *args, **kwargs):
        """Start worker threads"""
        num_workers = min(num_workers, self.max_threads)
        
        self.running = True
        self.thread_pool = []
        
        # Create and start threads
        for i in range(num_workers):
            if not self.running:
                break
            
            thread = threading.Thread(
                target=self._worker_wrapper,
                args=(target_func, i, *args),
                kwargs=kwargs,
                daemon=True
            )
            
            with self.lock:
                self.active_threads += 1
                self.thread_pool.append(thread)
            
            thread.start()
            
            # Stagger thread creation
            if i % 100 == 0 and i > 0:
                time.sleep(0.01)
        
        return self.thread_pool
    
    def _worker_wrapper(self, target_func, worker_id, *args, **kwargs):
        """Wrapper for worker threads with error handling"""
        try:
            target_func(worker_id, *args, **kwargs)
        except Exception:
            # Silent error handling
            pass
        finally:
            with self.lock:
                self.active_threads -= 1
    
    def stop_all(self):
        """Stop all threads"""
        self.running = False
        
        # Wait for threads to finish
        timeout = 5
        start_time = time.time()
        
        while self.active_threads > 0:
            if time.time() - start_time > timeout:
                break
            time.sleep(0.1)
    
    def add_task(self, task):
        """Add task to queue"""
        self.task_queue.put(task)
    
    def process_queue(self, num_workers=10):
        """Process tasks from queue with worker threads"""
        def queue_worker():
            while self.running:
                try:
                    task = self.task_queue.get(timeout=1)
                    if task:
                        try:
                            task()
                        except:
                            pass
                    self.task_queue.task_done()
                except queue.Empty:
                    continue
        
        return self.start_workers(queue_worker, num_workers)
    
    def get_status(self):
        """Get current thread status"""
        with self.lock:
            return {
                'active': self.active_threads,
                'total': len(self.thread_pool),
                'running': self.running
            }
    
    def wait_completion(self, timeout=None):
        """Wait for all threads to complete"""
        start_time = time.time()
        
        while self.active_threads > 0:
            if timeout and (time.time() - start_time) > timeout:
                return False
            time.sleep(0.1)
        
        return True
