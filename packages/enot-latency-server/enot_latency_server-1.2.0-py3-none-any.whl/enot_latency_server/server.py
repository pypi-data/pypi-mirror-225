"""Extendable latency measurement server."""
import asyncio
import pickle
from abc import ABC
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Dict

from aiohttp import web

_DEFAULT_HOST: str = '0.0.0.0'
_DEFAULT_PORT: int = 5450
_DEFAULT_ENDPOINT: str = 'measure_latency'

__all__ = ['LatencyServer']


class LatencyServer(ABC):
    """
    Server for remote latency measurement.

    Extend this class by inheriting from it and implement the ``measure_latency`` method.
    This method should take model and return its latency in **milliseconds**.

    """

    __CLIENT_MAX_SIZE: int = 1000 * 1024 * 1024

    def __init__(
        self,
        host: str = _DEFAULT_HOST,
        port: int = _DEFAULT_PORT,
        endpoint: str = _DEFAULT_ENDPOINT,
        max_workers: int = 1,
    ):
        """
        Server ctor.

        Parameters
        ----------
        host : str
            Host name or IP address. Default value is '0.0.0.0'.
        port : int
            Port. Default value is 5450.
        endpoint : str
            Endpoint. Default value is 'measure_latency'.
        max_workers : int
            Maximum number of workers in ThreadPoolExecutor. Default value is 1.

        """
        super().__init__()

        self._host: str = host
        self._port: int = port
        self._endpoint: str = endpoint

        self._loop = asyncio.get_event_loop()
        self._app = web.Application(client_max_size=self.__CLIENT_MAX_SIZE)
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def run(self) -> None:
        """Start latency measurement server."""

        async def _measure_latency_handler(request: web.Request) -> web.Response:
            data: Dict = pickle.loads(await request.read())
            latency: Dict[str, float] = await self._loop.run_in_executor(
                self._executor, partial(self.measure_latency, **data)
            )
            return web.json_response(data=latency, status=200)

        route = web.post(path=f'/{self._endpoint}', handler=_measure_latency_handler)
        self._app.add_routes([route])
        web.run_app(app=self._app, host=self._host, port=self._port, loop=self._loop)

    @staticmethod
    @abstractmethod
    def measure_latency(model: bytes, **kwargs) -> Dict[str, float]:
        """
        Latency measuring implementation for concrete device/framework/task/etc.

        Must return time in **MILLISECONDS** in the form: {'latency': latency}.
        You can also put in anything else like memory consumption: {'latency': latency, 'memory': memory}.
        When something bad happens you should raise ``aiohttp.web.<Exception>`` for correct reponse for client,
        see https://docs.aiohttp.org/en/latest/web_exceptions.html for more details.

        Parameters
        ----------
        model : bytes
            Packaged model: pickled python object, ONNX, etc.
        kwargs : Dict
            Additional keyword arguments.

        Returns
        -------
        Dict[str, float]
            Latency in milliseconds and anything else (optional).

        """
