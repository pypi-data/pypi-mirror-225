import logging

from dql.nodes_thread_pool import NodesThreadPool

logger = logging.getLogger("dql")


class NodesFetcher(NodesThreadPool):
    def __init__(self, client, data_storage, file_path, max_threads, cache):
        super().__init__(max_threads)
        self.client = client
        self.data_storage = data_storage
        self.file_path = file_path
        self.cache = cache

    def done_task(self, done):
        updated_nodes = []
        for d in done:
            lst = d.result()
            for node, checksum in lst:
                self.data_storage.update_checksum(node, checksum)
                node.checksum = checksum
                updated_nodes.append(node)
        return updated_nodes

    def do_task(self, chunk):
        res = []
        for node in chunk:
            if self.cache.exists(node.checksum):
                self.increase_counter(node.size)
                continue

            pair = self.fetch(node.path, node)
            res.append(pair)
        return res

    def fetch(self, path, node):
        from dvc_objects.fs.callbacks import Callback

        class _CB(Callback):
            def relative_update(  # pylint: disable=no-self-argument
                _, inc: int = 1  # noqa: disable=no-self-argument
            ):
                self.increase_counter(inc)

        hash_value = self.client.download(
            path, node.vtype, node.location, callback=_CB()
        )
        return node, hash_value
