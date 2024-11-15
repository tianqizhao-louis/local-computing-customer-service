from pydantic import BaseModel
from typing import List, Optional


class Link(BaseModel):
    rel: str
    href: str


class CustomerIn(BaseModel):
    name: str
    email: str


class CustomerOut(CustomerIn):
    id: str
    links: Optional[List[Link]] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class CustomerListResponse(BaseModel):
    data: List[CustomerOut]
    links: Optional[List[Link]] = None
