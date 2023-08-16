from datetime import datetime
from typing import Optional
from uuid import UUID

from ul_api_utils.api_resource.api_response import JsonApiResponsePayload
from data_aggregator_sdk.integration_message import IntegrationV0MessageMeta
from pydantic import BaseModel, validator


class ApiDeviceDataHistoryBody(BaseModel):
    period_from: datetime
    period_to: datetime
    mac: int
    protocol_type: Optional[str]
    packet_type: Optional[str]

    @validator('period_from', pre=True)
    def validate_period_from(cls, value: str | datetime) -> datetime:
        if isinstance(value, str):
            return datetime.combine(datetime.fromisoformat(value), datetime.min.time())
        return value

    @validator('period_to', pre=True)
    def validate_period_to(cls, value: str | datetime) -> datetime:
        if isinstance(value, str):
            return datetime.combine(datetime.fromisoformat(value), datetime.max.time())
        return value


class ApiDeviceDataHistoryResponse(JsonApiResponsePayload):
    mac: int
    bs_serial_numer: int
    date_created: datetime
    id: Optional[UUID]
    raw_dt: datetime
    raw_payload: str
    raw_message: str
    meta: IntegrationV0MessageMeta
