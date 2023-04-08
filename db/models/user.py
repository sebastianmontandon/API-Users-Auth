from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    username: str
    fullname: str
    availability: Optional[bool]
    password: str
    email: str
    domain: str