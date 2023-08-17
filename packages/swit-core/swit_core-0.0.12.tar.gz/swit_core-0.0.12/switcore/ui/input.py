from pydantic import BaseModel


class Input(BaseModel):
    type: str = 'text_input'
    action_id: str
    placeholder: str | None
    trigger_on_input: bool = False
    value: str | None
