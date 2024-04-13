from pydantic import BaseModel
from typing import Type, Dict


def generate_json_schema(model: Type[BaseModel]) -> Dict:
    schema = model.model_json_schema()
    simplified_properties = {}
    for prop, details in schema.get("properties", {}).items():
        simplified_properties[prop] = {"type": details["type"]}
    simplified_schema = {
        "title": schema.get("title", model.__name__),
        "properties": simplified_properties,
    }
    return simplified_schema
