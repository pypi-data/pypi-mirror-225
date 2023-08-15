import json
import time
import warnings
from contextlib import closing
from inspect import signature
from threading import Thread, Lock
from typing import Union

import websocket


class WebsocketAsyncClient:
    """
    Asynchronous websocket client.

    This class provides a wrapper around the websocket module to simplify receiving asynchronous messages.
    """

    def __init__(self, url: str = 'ws://localhost:5000', data_callback: Union[None, callable] = None,
                 timeout: Union[int, float] = 10.0):
        """
        Set up the websocket client.

        :param url: The full websocket url
        :param data_callback: Optional callback function when data is received. It must take a single dict argument.
        :param timeout: Websocket connection timeout
        """
        self._url = url
        self._timeout = timeout
        self._data = {}
        self._lock = Lock()
        self._ws_thread = None

        if callable(data_callback):
            if len(signature(data_callback).parameters) != 1:
                raise ValueError('Message callback must take a single dict argument')
        self._data_callback = data_callback

        websocket.setdefaulttimeout(timeout)
        self._ws = websocket.WebSocketApp(url, on_message=self._on_message, on_error=self._on_error,
                                          on_close=self._on_close)

    def __enter__(self):
        """
        Enter the websocket context by starting the asynchronous client.
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the websocket context by stopping the asynchronous client.
        """
        self.stop()

    def start(self) -> bool:
        """
        Start the asynchronous websocket client. This method blocks until the first message has been received
        on the websocket.

        :return: True if successfully connected, or false if no data has been received after the predefined
        timeout interval
        """
        if self.is_running():
            return False
        else:
            self._ws_thread = Thread(target=self._ws.run_forever)
            self._ws_thread.start()
            start_time = time.time()
            while self.is_running() and not self.has_data():
                time.sleep(0.1)
                if time.time() - start_time >= self._timeout:
                    warnings.warn(f'No data has been received from {self._url} after {self._timeout} seconds!',
                                  category=RuntimeWarning)
                    return False
            return True

    def stop(self):
        """
        Stop the asynchronous websocket client.
        """
        if self.is_running():
            self._ws.keep_running = False
            self._ws_thread.join(timeout=1.0)
            self._ws_thread = None

    def is_running(self):
        """
        Check if the asynchronous websocket client is running.
        :return: True if running, false otherwise
        """
        return self._ws_thread and self._ws.keep_running

    def has_data(self):
        """
        Check if any data has been received.
        :return: True if the data buffer is not empty
        """
        return bool(self._data)

    def poll(self) -> Union[dict, None]:
        """
        Poll the current data buffered data
        :return: The buffered data as a dict, or None if the websocket is not running
        """
        if not self.is_running():
            return None
        with self._lock:
            return self._data.copy()

    def _on_message(self, ws, message):
        data = json.loads(message)
        if callable(self._data_callback):
            try:
                self._data_callback(data)
            except Exception:
                pass
        with self._lock:
            self._data = data

    def _on_error(self, ws, error):
        warnings.warn(f'Error on websocket {self._url}: {error}', category=RuntimeWarning)
        self.stop()

    def _on_close(self, ws, close_status_code, close_msg):
        self.stop()


class WebsocketSyncClient:
    """
    Synchronous websocket client.

    This class provides a wrapper around the websocket module to read data in a blocking fashion.
    """

    def __init__(self, url: str = 'ws://localhost:5000'):
        """
        Set up the websocket client.

        :param url: The full websocket URL
        """
        self._url = url

    def read_once(self, timeout: Union[int, float] = 10.0) -> Union[None, dict]:
        """
        Read the first available message on the websocket.

        :param timeout: Timeout duration in seconds. If set to None, block indefinitely
        :return: The received data as a dict, or None if the connection times out
        """
        with closing(websocket.create_connection(self._url, timeout=timeout)) as ws:
            try:
                return json.loads(ws.recv())
            except websocket.WebSocketTimeoutException:
                return None

    def read_until(self, callback: callable, timeout: Union[None, float] = 10.0) -> bool:
        """
        Read the websocket messages until the callback function returns true or the timeout is reached.

        :param callback: A data callback function taking a single dict argument and returning true or false.
        KeyErrors are automatically suppressed. For example:
            def user_callback(data: dict) -> bool:
                return data['foo'] == 'bar'
        :param timeout: Timeout duration in seconds. If set to None, block indefinitely
        :return: True if the callback function returns true before the timeout, false otherwise
        """
        if not callable(callback):
            raise ValueError('Data callback argument must be a callable function')
        s = signature(callback)
        if len(s.parameters) != 1:
            raise ValueError('Data callback must take a single dict argument')
        if s.return_annotation is not s.empty and s.return_annotation is not bool:
            warnings.warn(
                f'The return annotation of the data callback function should be bool, not {s.return_annotation}',
                category=SyntaxWarning)

        start_time = time.time()
        kwargs = {'timeout': timeout} if timeout else {}
        with closing(websocket.create_connection(self._url, **kwargs)) as ws:
            try:
                while not callback(json.loads(ws.recv())):
                    if timeout and time.time() - start_time >= timeout:
                        return False
                return True
            except KeyError:
                pass
            except websocket.WebSocketTimeoutException:
                return False
