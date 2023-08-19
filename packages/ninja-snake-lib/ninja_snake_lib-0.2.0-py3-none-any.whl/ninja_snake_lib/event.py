import json
from datetime import datetime


class GnEvent:
    """
    Class used to represent the event types, created by GetNinjas systens.

    Methods
    -------
    to_json() -> str:
        return event in json format
    is_valid() -> bool:
        return True if event message have the correct structure.
    """

    def __init__(self, event_dict: dict) -> None:
        self._message = event_dict.get("message")
        self._schema = event_dict.get("schema")
        self._application = event_dict.get("application")
        self._true_timestamp = event_dict.get("true_timestamp", datetime.now())
        self._contexts = event_dict.get("contexts")

    def to_json(self) -> str:
        """Return GnEvent in json format."""

        event_dict = {
            "message": self._transform_dict_to_json_scaped_string(
                self._message
            ),
            "schema": self._schema,
            "application": self._application,
            "true_timestamp": str(
                int(self._true_timestamp.timestamp() * 1000)
            ),
        }

        if self._contexts is not None:
            event_dict[
                "contexts"
            ] = self._transform_dict_to_json_scaped_string(self._contexts)

        return json.dumps(event_dict)

    def _transform_dict_to_json_scaped_string(self, dict_object):
        return json.dumps(dict_object, ensure_ascii=False)

    def is_valid(self) -> bool:
        """Verify GnEvent attributes, return True if is correct format."""

        conditions = []

        conditions.append(isinstance(self._message, dict))
        conditions.append(isinstance(self._schema, str))
        conditions.append(isinstance(self._application, str))
        conditions.append(isinstance(self._true_timestamp, datetime))
        conditions.append(isinstance(self._contexts, (dict, type(None))))

        return_value = True if all(conditions) else False

        return return_value
