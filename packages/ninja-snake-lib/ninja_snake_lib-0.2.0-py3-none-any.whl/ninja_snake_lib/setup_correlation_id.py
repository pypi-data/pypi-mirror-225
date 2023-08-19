import logging
import uuid
from contextvars import ContextVar

correlation_id: ContextVar[uuid.UUID] = ContextVar(
    "correlation_id", default=uuid.uuid4()
)


def gn_context_correlation_id_from_request(func):
    def wraps(*args, **kwargs):
        REQUEST_INDEX = 1
        correlation_id.set(
            args[REQUEST_INDEX].headers.get("Correlation-Id", uuid.uuid4())
        )
        return func(*args, **kwargs)

    return wraps


class ContextFilter(logging.Filter):
    """ "Provides correlation id parameter for the logger"""

    def filter(self, record):
        record.correlation_id = correlation_id.get()
        return True
