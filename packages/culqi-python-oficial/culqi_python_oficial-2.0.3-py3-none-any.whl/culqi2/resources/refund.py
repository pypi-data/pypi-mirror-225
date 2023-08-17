from culqi2.utils.errors import ErrorMessage, NotAllowedError
from culqi2.utils.urls import URL
from culqi2.resources.base import Resource

__all__ = ["Refund"]


class Refund(Resource):
    endpoint = URL.REFUND

    def delete(self, id_, data=None, **options):
        raise NotAllowedError(ErrorMessage.NOT_ALLOWED)
