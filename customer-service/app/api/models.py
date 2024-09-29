from pydantic import BaseModel
from typing import List, Optional

class CustomerIn(BaseModel):
    name: str


class CustomerOut(CustomerIn):
    id: int


# class MovieUpdate(MovieIn):
#     name: Optional[str] = None
#     plot: Optional[str] = None
#     genres: Optional[List[str]] = None
#     casts_id: Optional[List[int]] = None