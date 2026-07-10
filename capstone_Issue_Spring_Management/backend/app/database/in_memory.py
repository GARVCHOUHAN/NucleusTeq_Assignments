"""
Small in-memory Mongo-like collections for backend tests.
"""

from copy import deepcopy
from dataclasses import dataclass
import re
from typing import Any

from bson import ObjectId


@dataclass
class InsertOneResult:
    inserted_id: ObjectId

@dataclass
class UpdateResult:
    matched_count: int
    modified_count: int

@dataclass
class DeleteResult:
    deleted_count: int


def _get_nested(document: dict, dotted_key: str) -> Any:
    value: Any = document

    for part in dotted_key.split("."):
        if isinstance(value, list):
            return [
                item.get(part)
                for item in value if isinstance(item, dict) and part in item]

        if not isinstance(value, dict) or part not in value:
            return None

        value = value[part]

    return value


def _matches(document: dict, query: dict) -> bool:
    for key, expected_value in query.items():
        if key == "$or":
            if not any(_matches(document, item) for item in expected_value):
                return False
            continue

        actual_value = _get_nested(document, key)

        if isinstance(expected_value, dict):
            if "$in" in expected_value:
                if actual_value not in expected_value["$in"]:
                    return False
                continue

            if "$regex" in expected_value:
                flags = re.IGNORECASE if "i" in expected_value.get("$options", "") else 0
                if actual_value is None or re.search(expected_value["$regex"], str(actual_value), flags) is None:
                    return False
                continue

        if isinstance(actual_value, list):
            if expected_value not in actual_value:
                return False
        elif actual_value != expected_value:
            return False

    return True


class InMemoryCollection:
    def __init__(self):
        self._documents: list[dict] = []

    def insert_one(self, document: dict):
        stored_document = deepcopy(document)
        stored_document.setdefault("_id", ObjectId())
        self._documents.append(stored_document)
        return InsertOneResult(stored_document["_id"])

    def find_one(self, query: dict):
        for document in self._documents:
            if _matches(document, query):
                return deepcopy(document)

        return None

    def find(self, query: dict):
        return [
            deepcopy(document)
            for document in self._documents
            if _matches(document, query)
        ]

    def update_one(self, query: dict, update: dict):
        for document in self._documents:
            if not _matches(document, query):
                continue

            if "$set" in update:
                document.update(deepcopy(update["$set"]))

            if "$push" in update:
                for key, value in update["$push"].items():
                    document.setdefault(key, []).append(deepcopy(value))

            if "$pull" in update:
                for key, value in update["$pull"].items():
                    if isinstance(value, dict):
                        document[key] = [
                            item
                            for item in document.get(key, [])
                            if not _matches(item, value)
                        ]
                    else:
                        document[key] = [
                            item
                            for item in document.get(key, [])
                            if item != value
                        ]

            return UpdateResult(1, 1)

        return UpdateResult(0, 0)

    def delete_many(self, query: dict):
        original_count = len(self._documents)
        self._documents = [
            document
            for document in self._documents
            if not _matches(document, query)
        ]
        return DeleteResult(original_count - len(self._documents))

    def count_documents(self, query: dict):
        return len(self.find(query))


class InMemoryDatabase:
    def __init__(self):
        self._collections: dict[str, InMemoryCollection] = {}

    def __getitem__(self, name: str):
        if name not in self._collections:
            self._collections[name] = InMemoryCollection()

        return self._collections[name]


class InMemoryClient:
    def __init__(self):
        self.admin = self

    def command(self, command_name: str):
        return {"ok": 1, "command": command_name}

    def close(self):
        return None
