from concurrent.futures import Executor, Future


class LocalExecutor(Executor):
    def submit(self, fn, /, *args, **kwargs):
        """Submits a callable to be executed with the given arguments.

        Schedules the callable to be executed as fn(*args, **kwargs) and returns
        a Future instance representing the execution of the callable.

        Returns:
            A Future representing the given call.
        """
        out = fn(*args, **kwargs)
        future = Future()
        future.set_result(out)
        return future
