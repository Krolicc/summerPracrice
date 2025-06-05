from pydantic import BaseModel, Field
from typing import Annotated, Any
from bson import ObjectId
from pydantic.json_schema import JsonSchemaValue

from pydantic_core import CoreSchema, core_schema


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_file: Any, handler) -> CoreSchema:
        def validate_from_string(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId string")
            return ObjectId(value)

        def serialize_object_id_to_str(obj_id: ObjectId) -> str:
            return str(obj_id)

        return core_schema.union_schema(
            [
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(validate_from_string),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize_object_id_to_str
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema.update(
            type="string", format="ObjectId", example="60b8d295f8e5f2b8c8d8e5f2"
        )

        return json_schema


class BaseMongoModel(BaseModel):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
