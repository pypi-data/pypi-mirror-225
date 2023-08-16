from typing import Callable, Dict, Generator

from bson import ObjectId


class PyObjectId(ObjectId):
    """
    PyObejct of mongo ObjectId
    """

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, object_id: str) -> ObjectId:
        if not ObjectId.is_valid(object_id):
            raise ValueError("Invalid objectid")
        return ObjectId(object_id)

    @classmethod
    def __modify_schema__(cls, field_schema: Dict) -> None:
        field_schema.update(type="string")
