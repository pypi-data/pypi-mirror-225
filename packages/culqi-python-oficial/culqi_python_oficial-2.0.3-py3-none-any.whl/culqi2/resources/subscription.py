from culqi2.utils.urls import URL
from culqi2.resources.base import Resource

__all__ = ["Subscription"]


class Subscription(Resource):
    endpoint = URL.SUBSCRIPTION
