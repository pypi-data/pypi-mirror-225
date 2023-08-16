"""Defines the ResponseError class"""

from typing import Union


class ResponseError(Exception):
    """
    This class captures the response to failed a request to PSquared
    """

    def __init__(self, message: str, errorCode: int, response: Union[bytes, str]):
        self.code = errorCode
        self.message = message
        self.response = response
