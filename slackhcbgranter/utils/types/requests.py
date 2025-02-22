from dataclasses import dataclass

from multidict import CIMultiDictProxy


@dataclass
class Response:
    status: int
    headers: CIMultiDictProxy[str]
    content: str
