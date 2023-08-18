from dataclasses import dataclass
from typing import Callable


@dataclass
class AutoAPISettings:
    use_aio: bool = False
    host: str | Callable = 'http://127.0.0.1:8000'
    license_name: str = 'MIT'
    explorer_title: str = 'AutoAPI Docs'
    explorer_version: str = '0.0.1'
    explorer_url: str = '/docs/'
