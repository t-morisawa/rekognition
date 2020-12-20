from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class FileImage:
    key: str
    content: bytes
    result: dict


@dataclass
class FileImages:
    images: List[FileImage]


@dataclass
class TwitterImage:
    url: str
    content: bytes
    created_at: datetime
    result: dict


@dataclass
class TwitterImages:
    images: List[TwitterImage]


@dataclass
class FileResponse:
    pass


@dataclass
class TwitterResponse:
    filename: str
    result: dict
