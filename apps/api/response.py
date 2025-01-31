import json
from http import HTTPStatus
from typing import Optional, TypeVar

from django.http import HttpResponse
from django.utils.translation import gettext as _

from apps.api.serializers import Serializer

ResponseType = TypeVar("ResponseType")


class SingleResponseModel(Serializer):
    response: ResponseType


class GeneralResponse(HttpResponse):
    def __init__(self, request, data: Optional[ResponseType] = None, **kwargs):
        params = {}
        if data is not None:
            content_types = str(request.headers.get("accept", "application/json"))
            content_types = content_types.replace(" ", "").split(",")
            content_types = list(map(lambda r: r.split(";")[0], content_types))

            if any(x in ["*/*", "application/json"] for x in content_types):
                params["content_type"] = "application/json"
                params["content"] = data.model_dump_json(by_alias=True)
            else:
                params["content_type"] = "application/json"
                params["status"] = HTTPStatus.NOT_ACCEPTABLE
                params["content"] = json.dumps(
                    {
                        "message": _("Not Acceptable"),
                        "metadata": {
                            "available": [
                                "application/json",
                            ],
                            "asked": ", ".join(content_types),
                        },
                    }
                )

        kwargs.update(params)
        super().__init__(**kwargs)


class SingleResponse(GeneralResponse):
    def __init__(self, request, *, data=None, **kwargs):
        if data is None:
            kwargs.setdefault("status", HTTPStatus.NO_CONTENT)
        else:
            data = SingleResponseModel(response=data)
        super().__init__(request=request, data=data, **kwargs)


__all__ = [
    "SingleResponse",
]
