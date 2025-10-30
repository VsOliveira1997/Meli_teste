from pydantic import BaseModel

class ExcludeIP(BaseModel):
    ip: str