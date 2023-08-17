from culqi2.utils.urls import URL
from culqi2.resources.base import Resource

__all__ = ["Customer"]


class Customer(Resource):
    endpoint = URL.CUSTOMER
