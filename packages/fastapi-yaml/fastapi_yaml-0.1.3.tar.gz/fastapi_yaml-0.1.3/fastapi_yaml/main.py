from typing import Callable

import yaml
from fastapi import Request, Response
from fastapi.routing import APIRoute


class YamlRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if self.headers.get("content-type") in [
                "application/x-yaml",
                "application/yaml",
                "text/yaml",
            ]:
                body = yaml.safe_load(body)
            self._body = body
        return self._body


class YamlRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = YamlRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler
