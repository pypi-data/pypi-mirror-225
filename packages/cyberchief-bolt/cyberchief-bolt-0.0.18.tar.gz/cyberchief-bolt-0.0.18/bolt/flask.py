import json
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import logging

from flask import request

endpoint = "api/v1/log-request/single"


class BoltFlask:
    def perform_request(self, data):
        try:
            urlopen(url=self.saved_request, data=json.dumps(data).encode("utf-8"))
        except Exception as e:
            self.logger.warning(e)

    def __init__(self, app, bolt_host: str, bolt_api_key: str, **kwargs):
        """
        :param app: Instance of Flask app
        :param bolt_host: Publicly accessible address of Bolt Collector
        :param bolt_api_key: Bolt API Key
        :param kwargs: optional parameter containing worker count for communicating with bolt
        """
        self.app = app
        self.pool = ThreadPoolExecutor(max_workers=kwargs.get("workers", 4))
        self.disabled = kwargs.get("disabled", False)
        self.logger = logging.getLogger("bolt")
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s]  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S %z",
        )
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        assert (
            bolt_host is not None
        ), "Bolt for FLASK __init__ is missing bolt_host parameter"
        assert (
            bolt_api_key is not None
        ), "Bolt for FLASK __init__ is missing bolt_api_key parameter"
        assert urlparse(bolt_host).scheme in [
            "http",
            "https",
        ], f"Bolt for FLASK has invalid host scheme. Host must be in format http[s]://example.com"

        self.host = bolt_host
        self.host += endpoint if self.host[-1] == "/" else f"/{endpoint}"
        self.key = bolt_api_key
        self.saved_request = Request(
            url=self.host,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": self.key,
            },
            method="POST",
        )

        if not self.disabled:

            @app.after_request
            def function(response, *args, **kwargs):
                try:
                    dst_host = (
                        request.environ.get("HTTP_HOST")
                        or request.environ.get("HTTP_X_FORWARDED_FOR")
                        or request.environ.get("REMOTE_ADDR")
                    )
                    data = {
                        "request": {
                            "url": {
                                "host": dst_host,
                                "path": request.path,
                                "parameters": list(
                                    map(
                                        lambda x: {"name": x[0], "value": x[1]},
                                        request.args.items(),
                                    )
                                ),
                            },
                            "headers": list(
                                map(
                                    lambda x: {"name": x[0], "value": x[1]},
                                    (request.headers).items(),
                                )
                            ),
                            "body": request.data.decode("utf-8"),
                            "method": request.method,
                        },
                        "response": {
                            "url": f"{request.environ.get('SERVER_NAME')}:{request.environ.get('SERVER_PORT')}",
                            "status": response.status_code,
                            "headers": list(
                                map(
                                    lambda x: {"name": x[0], "value": x[1]},
                                    (response.headers).items(),
                                )
                            ),
                            "body": response.data.decode("utf-8"),
                        },
                        "meta": {
                            "environment": "production",
                            "incoming": True,
                            "source": request.environ.get("HTTP_X_FORWARDED_FOR")
                            or request.environ.get("REMOTE_ADDR"),
                            "sourcePort": request.environ.get("REMOTE_PORT"),
                            "destination": request.environ.get("SERVER_NAME"),
                            "destinationPort": request.environ.get("SERVER_PORT"),
                            "boltSource": "python/flask",
                        },
                    }
                    self.pool.submit(self.perform_request, data=data)
                except Exception as e:
                    self.logger.debug(e)
                return response
