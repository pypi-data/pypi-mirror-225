from enum import Enum

from pydantic import BaseModel


class SizeTypes(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"


class Textarea(BaseModel):
    type: str = "textarea"
    action_id: str
    placeholder: str | None
    value: str | None
    height: SizeTypes
    disabled: bool = False
