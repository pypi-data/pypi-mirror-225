from culqi2.utils.urls import URL
from culqi2.resources.base import Resource


__all__ = ["Order"]


class Order(Resource):
    endpoint = URL.ORDER

    def confirm(self, id_, data=None, **options):
        url = self._get_url(id_, "confirm")
        return self._post(url, data, **options)
    def confirmtipo(self, data=None, **options):
        url = self._get_url("confirm")
        return self._post(url, data, **options)