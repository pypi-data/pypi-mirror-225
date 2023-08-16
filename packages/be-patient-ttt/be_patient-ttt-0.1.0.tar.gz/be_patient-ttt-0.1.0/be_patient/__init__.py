"""A library facilitating work with asynchronous APIs."""
import logging
from logging import NullHandler

from .api import (
    RequestsWaiter,
    to_curl,
    wait_for_value_in_request,
    wait_for_values_in_request,
)

__version__ = "0.1.0"
__all__ = [
    "to_curl",
    "wait_for_values_in_request",
    "wait_for_value_in_request",
    "RequestsWaiter",
]

logging.getLogger(__name__).addHandler(NullHandler())
