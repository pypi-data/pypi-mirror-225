import logging
import time
from typing import Tuple
from importlib.metadata import version

from rkclient.query import RKQuery
from rkclient.request import RequestHelper

log = logging.getLogger("rkclient")

RK_VERSION = version('RecordKeeper_Client')


class RKAdmin:
    """
    This class is not supposed to be used by normal RK user, but by RK administrator or in tests.
    """

    def __init__(self,
                 receiver_url: str,
                 graph_builder_url: str,
                 timeout_sec: int = 5,
                 insecure: bool = True,
                 user_auth: str = '',
                 puc_auth: str = ''):
        self.receiver_client = RKQuery(receiver_url, timeout_sec=timeout_sec, insecure=insecure,
                                       user_auth=user_auth, puc_auth=puc_auth)
        graph_builder_url = graph_builder_url.rstrip('/')
        log.info(f"Connecting to Graph Builder: {graph_builder_url}")
        self.graph_builder_client = RequestHelper(graph_builder_url, timeout_sec=timeout_sec, insecure=insecure,
                                                  user_auth=user_auth, puc_auth=puc_auth,
                                                  user_agent=f'recordkeeper-client-{RK_VERSION}')

    def check_connections(self) -> Tuple[str, bool]:
        msg, ok = self.graph_builder_client.get("/info")
        if not ok:
            return f"Graph Builder connection error: {msg}", False
        msg, ok = self.receiver_client.get_info()
        if not ok:
            return f"Receiver connection error: {msg}", False
        return 'OK', True

    def graph_rebuild(self) -> Tuple[str, bool]:
        """
        :return: first element: error message or 'OK'
                 second element: True for success, False for error
        """
        text, ok = self.graph_builder_client.post("/rebuild", "{}")
        if not ok:
            return f"Starting rebuilding process failed: {text}", False
        return 'OK', True

    def graph_flush(self) -> Tuple[str, bool]:
        """
        Waits till all PEMs from queue have been added to graph.
        :return: first element: error message or 'OK'
                 second element: True for success, False for error
        """
        start_time = time.time()
        text, ok = self.graph_builder_client.post("/flush", "{}")
        total_flush_time = time.time() - start_time
        if not ok:
            return f"flushing queue failed: {text}", False
        return f"flushing queue finished, in {total_flush_time:.2f}s", True

    def graph_verify(self) -> Tuple[str, bool]:
        """
        Starts sql vs graph comparison.
        :return: first element: json with "msg" field, containing error message or report (containing newlines).
                 second element: True for success, False for error
        """
        text, ok = self.graph_builder_client.post("/verify", "{}")
        if not ok:
            return f"Verifying integrity failed: {text}", False
        return text, True

    def get_graph_info(self) -> Tuple[str, bool]:
        """
        Returns json with fields as in GraphBuilderInfo class - the GB state. Use `deserialize_graph_builder_info` for easy parsing.
        :return: check class description
        """
        text, ok = self.graph_builder_client.get("/info")
        return text, ok

    def clean_dbs(self) -> Tuple[str, bool]:
        """
        Completely erases both sql and graph dbs - use only in tests. Needs admin permission from auth token.
        :return: first element: error message or 'OK'
                 second element: True for success, False for error
        """
        text, ok = self.receiver_client.receiver_request.post("/clean", "{}")
        if not ok:
            return f"Cleaning db failed: {text}", False
        return 'OK', True
