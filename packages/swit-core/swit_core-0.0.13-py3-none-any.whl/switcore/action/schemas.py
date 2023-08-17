import base64
import bz2
import json
from datetime import datetime
from enum import Enum
from typing import Any
from typing import Optional, Dict, List

from pydantic import BaseModel
from pydantic import validator

from switcore.ui.button import Button
from switcore.ui.collection_entry import CollectionEntry
from switcore.ui.container import Container
from switcore.ui.divider import Divider
from switcore.ui.file import File
from switcore.ui.header import Header
from switcore.ui.html_frame import HtmlFrame
from switcore.ui.image import Image
from switcore.ui.input import Input
from switcore.ui.select import Select
from switcore.ui.signIn_page import SignInPage
from switcore.ui.tabs import Tabs
from switcore.ui.text_paragraph import TextParagraph
from switcore.ui.textarea import Textarea
from switcore.ui.datepicker import DatePicker
from switcore.ui.info_card import InfoCard


class UserInfo(BaseModel):
    user_id: str
    organization_id: str


class UserPreferences(BaseModel):
    language: str
    time_zone_offset: str
    color_theme: str


class Resource(BaseModel):
    resource_type: str
    id: str
    created_at: datetime
    edited_at: datetime
    content: str
    content_formatted: Dict[str, Any]
    attachments: Optional[List[Dict[str, Any]]]
    files: Optional[List[Dict[str, Any]]]
    creator: Dict[str, Any]


class UserActionType(str, Enum):
    right_panel_open = "right_panel_open"
    presence_sync = "presence_sync"
    user_commands_chat = "user_commands.extensions:chat"
    user_commands_chat_extension = "user_commands.chat_extension"
    user_commands_chat_commenting = "user_commands.extensions:chat_commenting"
    user_commands_context_menus_message = "user_commands.context_menus:message"
    user_commands_context_menus_message_comment = "user_commands.context_menus:message_comment"
    view_actions_drop = "view_actions.drop"
    view_actions_input = "view_actions.input"
    view_actions_submit = "view_actions.submit"
    view_actions_oauth_complete = "view_actions.oauth_complete"


class UserAction(BaseModel):
    type: UserActionType
    id: str
    slash_command: str
    resource: Resource | None
    value: str | None = None


class Context(BaseModel):
    workspace_id: str
    channel_id: str


ElementType = (CollectionEntry | Button | Divider | File | HtmlFrame | Input | Select
               | SignInPage | TextParagraph | Image | Textarea | Container | Tabs | DatePicker | InfoCard)


def contain_only_dict(elements_data: list[dict | ElementType]) -> bool:
    for element_data in elements_data:
        if isinstance(element_data, ElementType):
            return False

    return True


def get_element_type(element_data: dict):
    element_type_str = element_data.get('type')
    if element_type_str == 'collection_entry':
        return CollectionEntry
    elif element_type_str == 'button':
        return Button
    elif element_type_str == 'divider':
        return Divider
    elif element_type_str == 'file':
        return File
    elif element_type_str == 'html_frame':
        return HtmlFrame
    elif element_type_str == 'text_input':
        return Input
    elif element_type_str == 'select':
        return Select
    elif element_type_str == 'sign_in_page':
        return SignInPage
    elif element_type_str == 'text':
        return TextParagraph
    elif element_type_str == 'textarea':
        return Textarea
    elif element_type_str == 'image':
        return Image
    elif element_type_str == 'container':
        return Container
    elif element_type_str == 'tabs':
        return Tabs
    elif element_type_str == 'datepicker':
        return DatePicker
    elif element_type_str == 'info_card':
        return InfoCard
    else:
        raise ValueError(f"Unknown element type: {element_type_str}")


class Body(BaseModel):
    elements: list[ElementType]

    class Config:
        smart_union = True

    def __init__(self, **data: Any) -> None:
        elements_data = data.get('elements', [])

        if contain_only_dict(elements_data):
            _elements: list[ElementType] = []
            for element_data in elements_data:
                element_type = get_element_type(element_data)
                element = element_type(**element_data)
                _elements.append(element)
            super().__init__(elements=_elements)
        else:
            super().__init__(**data)

    def get_element_by_action_id(self, action_id: str) -> ElementType:
        """
        Get element by action_id if it exists, otherwise raise ValueError
        """
        for element in self.elements:
            if getattr(element, 'action_id', None) is None:
                continue

            if element.action_id == action_id:
                return element

        raise ValueError(f"Element with action_id: {action_id} not found")


class Footer(BaseModel):
    buttons: list[Button]


class ViewCallbackType(str, Enum):
    update = "views.update"
    initialize = "views.initialize"
    open = "views.open"
    push = "views.push"
    close = "views.close"


class AttachmentCallbackType(str, Enum):
    share_channel = "attachments.share.channel"


class AttachmentView(BaseModel):
    state: str | bytes
    header: Header
    footer: Footer | None
    body: Body


class View(AttachmentView):
    view_id: str


class ViewResponse(BaseModel):
    callback_type: ViewCallbackType
    new_view: View


class AttachmentResponse(BaseModel):
    callback_type: AttachmentCallbackType
    attachments: AttachmentView


class PlatformTypes(str, Enum):
    DESKTOP = 'Desktop'
    IOS = 'iOS'
    ANDROID = 'Android'


class SwitRequest(BaseModel):
    platform: PlatformTypes
    time: datetime
    app_id: str
    user_info: UserInfo
    user_preferences: UserPreferences
    context: Context
    user_action: UserAction
    current_view: View | AttachmentView | None

    @validator('current_view', pre=True)
    def empty_dict_to_null(cls, v):
        if v == {}:
            return None
        return v


class SwitResponse(BaseModel):
    callback_type: ViewCallbackType | AttachmentCallbackType
    new_view: View | None
    attachments: AttachmentView | None
    reference_view_id: str | None


class BaseState(BaseModel):
    autoincrement_id: int = 1

    @classmethod
    def from_bytes(cls, byte: bytes):
        d = json.loads(bz2.decompress(base64.b64decode(byte)).decode("utf-8"))
        return cls(**d)

    def to_bytes(self) -> bytes:
        return base64.b64encode(bz2.compress(json.dumps(self.dict()).encode("utf-8"), 1))
