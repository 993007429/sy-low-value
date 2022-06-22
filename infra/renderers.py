import json
from typing import Any

from django.http import HttpRequest
from ninja.renderers import JSONRenderer as NinjaJSONRenderer


class JSONRenderer(NinjaJSONRenderer):
    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> Any:
        return json.dumps(data, cls=self.encoder_class, **self.json_dumps_params, ensure_ascii=False)
