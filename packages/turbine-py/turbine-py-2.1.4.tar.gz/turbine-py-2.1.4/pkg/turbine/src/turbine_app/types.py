import logging
import json
from collections import UserList

logging.basicConfig()


class Record:
    def __init__(self, key: str, value: ..., timestamp: float):
        self.key = key
        try:
            self.value = json.loads(str(value, encoding="utf-8"))
        except Exception:
            self.value = value

        self.timestamp = timestamp

    def __repr__(self):
        from pprint import pformat

        return pformat(vars(self), indent=4, width=1)

    def __getitem__(self, key):
        return self.value

    @property
    def is_json_schema(self):
        return all(x in self.value for x in ("payload", "schema"))

    @property
    def is_cdc_format(self):
        return self.is_json_schema and bool(self.value.get("payload").get("source"))

    def unwrap(self) -> None:
        if self.is_cdc_format:
            payload = self.value["payload"]

            try:
                schema_fields = self.value["schema"]["fields"]
                after_field = next(sf for sf in schema_fields if sf["field"] == "after")

                del after_field["field"]
                after_field["name"] = self.value["schema"]["name"]
                self.value["schema"] = after_field
            except StopIteration or KeyError as e:
                logging.error(f"CDC envelope is malformed: {e}")

            self.value["payload"] = payload["after"]


class RecordList(UserList):
    def unwrap(self):
        [rec.unwrap() for rec in self.data]

    def add_record(self, record):
        self.data.append(
            Record(key=record.key, value=record.value, timestamp=record.timestamp)
        )


class Records:
    records: RecordList = None
    stream = ""
    name = ""

    def __init__(self, records: RecordList, stream: str, name: str):
        self.records = records
        self.stream = stream
        self.name = name

    def __repr__(self):
        from pprint import pformat

        return pformat(vars(self), indent=4, width=1)

    def unwrap(self):
        [rec.unwrap() for rec in self.records.data]
