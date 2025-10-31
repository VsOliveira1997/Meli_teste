from pydantic import BaseModel
from ipaddress import IPv4Address, IPv6Address
from typing import Union

class ExcludeIP(BaseModel):
    ip: Union[IPv4Address, IPv6Address]


