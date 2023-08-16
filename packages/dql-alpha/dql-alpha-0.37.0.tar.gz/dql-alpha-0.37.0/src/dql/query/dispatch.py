from itertools import chain
from multiprocessing import cpu_count
from typing import Any, Dict, Iterator, Optional

from multiprocess import Process, Queue  # pylint: disable=no-name-in-module

from dql.catalog import Catalog

from .udf import UDFFactory

WORKER_BUFFER_SIZE = 1000
STOP_SIGNAL = "STOP"
OK_STATUS = "OK"
FINISHED_STATUS = "FINISHED"
FAILED_STATUS = "FAILED"


class UDFDispatcher:
    def __init__(self, udf, catalog_init_params, db_adapter_clone_params):
        if not isinstance(udf, UDFFactory):
            self.udf = udf
        else:
            self.udf = None
            self.udf_factory = udf
        self.catalog_init_params = catalog_init_params
        (
            self.db_adapter_class,
            self.db_adapter_args,
            self.db_adapter_kwargs,
        ) = db_adapter_clone_params
        self.catalog = None
        self.initialized = False
        self.task_queue = None
        self.done_queue = None

    def _init_worker(self):
        # TODO: Add UDF class init here with any custom params (if needed)
        if not self.catalog:
            db_adapter = self.db_adapter_class(
                *self.db_adapter_args, **self.db_adapter_kwargs
            )
            self.catalog = Catalog(db_adapter, **self.catalog_init_params)
        if not self.udf:
            self.udf = self.udf_factory()
        self.initialized = True

    def _run_worker(self):
        try:
            self._init_worker()
            for row in iter(self.task_queue.get, STOP_SIGNAL):
                udf_output = self._call_udf(row)
                self.done_queue.put({"status": OK_STATUS, "result": udf_output})
            # Finalize UDF, clearing the batch collection and returning
            # any held results
            if udf_output := self._finalize_udf():
                self.done_queue.put({"status": OK_STATUS, "result": udf_output})
            self.done_queue.put({"status": FINISHED_STATUS})
        except Exception as e:
            self.done_queue.put({"status": FAILED_STATUS, "exception": e})
            raise e

    def _call_udf(self, row):
        if not self.initialized:
            raise RuntimeError("Internal Error: Attempted to call uninitialized UDF!")
        return self.udf(self.catalog, row)

    def _finalize_udf(self):
        if not self.initialized:
            raise RuntimeError("Internal Error: Attempted to call uninitialized UDF!")
        if hasattr(self.udf, "finalize"):
            return self.udf.finalize()
        return None

    def run_udf_parallel(
        self, input_rows, n_workers: Optional[int] = None
    ) -> Iterator[Dict[str, Any]]:
        if not n_workers:
            n_workers = cpu_count()
        if n_workers < 1:
            raise RuntimeError(
                "Must use at least one worker for parallel UDF execution!"
            )

        self.task_queue = Queue()
        self.done_queue = Queue()
        # pylint: disable=not-callable
        pool = [
            Process(name=f"Worker-UDF-{i}", target=self._run_worker)
            for i in range(n_workers)
        ]
        for p in pool:
            p.start()

        # Will be set to True if all tasks complete normally
        normal_completion = False
        try:
            # Will be set to True when the input is exhausted
            input_finished = False
            # Stop all workers after the input rows have finished processing
            input_data = chain(input_rows, [STOP_SIGNAL] * n_workers)

            # Add initial buffer of tasks
            for _ in range(WORKER_BUFFER_SIZE):
                try:
                    self.task_queue.put(next(input_data))
                except StopIteration:
                    input_finished = True
                    break

            # Process all tasks
            while n_workers > 0:
                result = self.done_queue.get()
                status = result["status"]
                if status == FINISHED_STATUS:
                    # Worker finished
                    n_workers -= 1
                elif status == OK_STATUS:
                    if not input_finished:
                        try:
                            self.task_queue.put(next(input_data))
                        except StopIteration:
                            input_finished = True
                    yield result["result"]
                else:  # Failed / error
                    n_workers -= 1
                    exc = result.get("exception")
                    if exc:
                        raise exc
                    raise RuntimeError("Internal error: Parallel UDF execution failed")

            # Finished with all tasks normally
            normal_completion = True
        finally:
            if not normal_completion:
                # Stop all workers if there is an unexpected exception
                for _ in pool:
                    self.task_queue.put(STOP_SIGNAL)
                self.task_queue.close()

                # This allows workers (and this process) to exit without
                # consuming any remaining data in the queues.
                # (If they exit due to an exception.)
                self.task_queue.cancel_join_thread()
                self.done_queue.cancel_join_thread()

                # Flush all items from the done queue.
                # This is needed if any workers are still running.
                while n_workers > 0:
                    result = self.done_queue.get()
                    status = result["status"]
                    if status != OK_STATUS:
                        n_workers -= 1

            # Wait for workers to stop
            for p in pool:
                p.join()
