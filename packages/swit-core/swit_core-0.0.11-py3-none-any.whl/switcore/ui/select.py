from pydantic import BaseModel

from switcore.ui.element_components import StaticAction


class Option(BaseModel):
    label: str
    action_id: str
    static_action: StaticAction | None = None


class Style(BaseModel):
    variant: str | None


class Select(BaseModel):
    type: str = 'select'
    placeholder: str | None
    multiselect: bool = False
    trigger_on_input: bool
    value: list[str] | None
    options: list[Option] = []
    style: Style | None = None
