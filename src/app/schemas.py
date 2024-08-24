from datetime import datetime
from ipaddress import IPv4Address, IPv6Address

from ninja import Field, FilterSchema, ModelSchema

from app.models import NginxLog


class NginxLogFilters(FilterSchema):
    time__gte: datetime | None = None
    time__lte: datetime | None = None
    remote_ip: str | None = None
    remote_user: str | None = None
    agent: str | None = None


class NginxLogResponseItem(ModelSchema):
    time: datetime = Field(description="Time of the request")
    remote_ip: IPv6Address | IPv4Address = Field(description="IP address of the client")
    remote_user: str = Field(description="Remote user")
    request: str = Field(description="Request")
    response: int = Field(description="Response code")
    bytes: int = Field(description="Bytes sent")
    referrer: str = Field(description="Referrer")
    agent: str = Field(description="User agent")

    class Meta:
        model = NginxLog
        fields = "__all__"
