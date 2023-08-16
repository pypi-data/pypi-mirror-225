"""Defines the RequestError class"""

from typing import Union


class RequestError(Exception):
    """
    This class captures how a request to PSquared could not be made
    """

    def __init__(self, message: Union[bytes, str]):
        self.message = message
