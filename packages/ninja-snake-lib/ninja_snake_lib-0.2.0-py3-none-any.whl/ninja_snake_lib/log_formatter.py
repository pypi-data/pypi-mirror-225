import logging
import socket
from datetime import datetime
from sys import getsizeof

import json_log_formatter
from django.utils import timezone


class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def set_extra_correlation_id(self, full_log: dict, extra: dict):
        """Set extra correlation_id"""

        if extra.get("thread_correlation_id", None):
            full_log["correlation_id"] = str(
                extra.get("thread_correlation_id")
            )

        return full_log

    def get_trace_id(self, record: logging.LogRecord):
        """Get trace_id"""
        return record.otelTraceID if hasattr(record, "otelTraceID") else None

    def get_exc_info(
        self, full_log: dict, record: logging.LogRecord
    ):  # pragma: no cover
        """Get exc_info"""
        if record.exc_info or record.levelname.lower() == "exception":
            full_log["exc_info"] = self.formatException(record.exc_info)

        return full_log

    def clean_server_time(self, extra: dict):  # pragma: no cover
        """Clean server time"""
        if extra.get("server_time"):
            del extra["server_time"]

        return extra

    def json_record(
        self, message: str, extra: dict, record: logging.LogRecord
    ) -> dict:
        full_log = {
            "time": datetime.now(
                tz=timezone.get_current_timezone()
            ).isoformat(),
            "trace_id": self.get_trace_id(record=record),
            "correlation_id": record.correlation_id,
            "gn_from": None,
            "gn_version": "1.0",
            "severity": record.levelname,
            "controller": None,
            "request_time": None,
            "request_method": None,
            "request_uri": None,
            "request_length": None,
            "request_query": None,
            "response_status": None,
            "bytes_sent": None,
            "remote_ip": None,
            "user_agent": None,
            "message": message,
            "custom": None,
        }

        if extra.get("request") and not isinstance(
            extra.get("request"), socket.SocketType
        ):
            request = extra.get("request")
            web_log = {
                "correlation_id": record.correlation_id,
                "request_method": request.method,
                "request_uri": request.META.get("PATH_INFO"),
                "request_length": getsizeof(request.data),
                "remote_ip": request.META.get("REMOTE_ADDR"),
                "user_agent": request.META.get("HTTP_USER_AGENT"),
                "request_query": request.META.get("QUERY_STRING"),
                "gn_from": request.META.get("HTTP_GN_FROM"),
            }
            full_log.update(web_log)

            del extra["request"]

        full_log = self.set_extra_correlation_id(
            full_log=full_log, extra=extra
        )

        extra = self.clean_server_time(extra=extra)

        full_log = self.get_exc_info(full_log=full_log, record=record)

        return full_log
