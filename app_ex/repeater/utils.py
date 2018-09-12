from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
import requests


class RandomNumber(object):
    _instance = None
    # 这里这个单例模式其实没那么需要
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RandomNumber, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, ):
        self.apiKey = "ddcdd8bd-09a0-44e9-bb09-cb49010a80ba"
        self.url = "https://api.random.org/json-rpc/1/invoke"

    def random_number(self, max_: int, num: int = 1, min_: int = 0):
        data = {
            "jsonrpc": "2.0",
            "method": "generateIntegers",
            "params": {
                "apiKey": self.apiKey,
                "n": num,
                "min": min_,
                "max": max_,
                "replacement": True,
                "base": 10
            },
            "id": 1
        }
        r = requests.post(url=self.url, json=data)
        return r.json()["result"]["random"]["data"]


class ShinyRuoPageNumberViewSet(GenericViewSet):
    pagination_class = PageNumberPagination

    def page_response(self, queryset, serializer_class):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True)
        return self.get_paginated_response(serializer.data)
