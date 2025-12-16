"""
Thread Manager for managing background threads lifecycle.
Provides graceful shutdown and tracking of all background threads.
"""
import threading
import time
import Logger

logger = Logger.getLogger()


class ThreadManager:
    """Manages lifecycle of all background threads with graceful shutdown."""
    
    def __init__(self):
        self.threads = []
        self.shutdown_event = threading.Event()
        self.logger = logger
        
    def register_thread(self, thread, name: str):
        """Register a thread for management."""
        if thread is not None:
            thread.name = name
            self.threads.append(thread)
            # self.logger.info(f"Registered thread: {name}")
            
    def start_all(self):
        """Start all registered threads."""
        for thread in self.threads:
            if thread.is_alive():
                self.logger.warning(f"Thread {thread.name} is already running")
            else:
                thread.start()
                # self.logger.info(f"Started thread: {thread.name}")
    
    def stop_all(self, timeout: float = 5.0):
        """Gracefully stop all registered threads."""
        # self.logger.info("Initiating graceful shutdown of all threads...")
        self.shutdown_event.set()
        
        # Wait for threads to finish
        for thread in self.threads:
            if thread.is_alive():
                # self.logger.info(f"Waiting for thread {thread.name} to finish...")
                thread.join(timeout=timeout)
                if thread.is_alive():
                    self.logger.warning(f"Thread {thread.name} did not stop within {timeout}s")
                else:
                    # self.logger.info(f"Thread {thread.name} stopped successfully")
                    pass
    
    def is_shutdown_requested(self) -> bool:
        """Check if shutdown has been requested."""
        return self.shutdown_event.is_set()
    
    def wait_for_shutdown(self, timeout: float = None):
        """Wait for shutdown event."""
        return self.shutdown_event.wait(timeout=timeout)


# Global thread manager instance
_thread_manager = None


def get_thread_manager() -> ThreadManager:
    """Get the global thread manager instance."""
    global _thread_manager
    if _thread_manager is None:
        _thread_manager = ThreadManager()
    return _thread_manager

