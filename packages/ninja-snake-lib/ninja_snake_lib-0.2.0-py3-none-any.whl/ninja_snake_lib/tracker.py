import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime

from .event import GnEvent

"""
    Development of the tracker base class in to create a model of
    behavior and ensure modularization between different technologies.

    Tracker is the main class, its a Factory for call the correct tracker type

    - TrackerBase(ABS)
        -TrackerLocalFile(TrackerBase)

    - Tracker
"""

default_logger = logging.getLogger(__name__)


class TrackerBase(ABC):
    """
    A class to represent the abstract classes of a tracker

    ...

    Attributes
    ----------
    tracker_type : str
        type of tracker

    Methods
    -------
    send_event(event: dict):
        Abstract methode for implements how to send
        file for log system tecnology
    """

    def __init__(self, tracker_type: str, app_logger: logging = None) -> None:
        self._tracker_type = tracker_type
        self.logger = app_logger if app_logger else default_logger

    @abstractmethod
    def send_event(self, event: dict):
        """Determine how to tracker send event"""
        pass


class TrackerLocalFile(TrackerBase):
    """
    Classe based in TrackeBase, for write logs in local file system.
    """

    def __init__(
        self,
        path: str = "/tmp/events.log",
        mode: str = "a",
        encoding: str = None,
        app_logger: logging = None,
    ) -> None:
        super().__init__("file", app_logger=app_logger)
        self._path = os.path.abspath(path)
        self._mode = mode
        self._encoding = encoding

    def send_event(self, event: dict) -> bool:
        gn_event = GnEvent(event)

        if gn_event.is_valid():
            try:
                gn_event_to_json = gn_event.to_json()
                self._write_file(gn_event_to_json)

            except Exception as err:
                self.logger.error(
                    "TrackerError: Error to write in file system."
                    f"Error message: {err}"
                )
                return False

            self.logger.info(
                f"Event write in file {self._path} -> {datetime.now()}"
            )
            return True

        else:
            self.logger.warning("Event invalid, verify the struct of event")
            return False

    def _write_file(self, event):
        with open(self._path, mode=self._mode, encoding=self._encoding) as f:
            f.write(event + "\n")


class Tracker:
    """
    Classe that implement factory design for call the correct tracker.

    Methods
    -------
    create_tracker(tracker_type: str, *args, **kwargs):
        Method for call the correct tracker type based
        in tracker_tipe parameter
    """

    @staticmethod
    def create_tracker(
        tracker_type: str, app_logger: logging = None, *args, **kwargs
    ) -> TrackerBase:
        logger = app_logger if app_logger else default_logger

        kwargs["app_logger"] = logger

        if tracker_type == "file":
            return TrackerLocalFile(*args, **kwargs)

        else:
            error_msg = f"Tracker type '{tracker_type}' not supported"
            logger.error(error_msg)
            raise ValueError(error_msg)
