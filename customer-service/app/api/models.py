from pydantic import BaseModel
from typing import Optional

class CustomerIn(BaseModel):
    name: str
    email: str

class CustomerOut(CustomerIn):
    id: str

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class Link(BaseModel):
    rel: str
    href: str

class CustomerListResponse(BaseModel):
    data: list[CustomerOut]
    links: list[Link]

# Define the WaitlistEntry models
class WaitlistEntryIn(BaseModel):
    pet_id: str
    breeder_id: str

class WaitlistEntryOut(WaitlistEntryIn):
    id: str
    consumer_id: str
