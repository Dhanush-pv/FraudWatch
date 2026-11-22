"""Canonical event contract for the transaction source domain."""
from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TransactionStatus(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    DECLINED = "DECLINED"
    REVERSED = "REVERSED"

class Channel(str, Enum):
    POS = "POS"
    ECOMMERCE = "ECOMMERCE"
    ATM = "ATM"
    MOBILE = "MOBILE"

class TransactionEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(min_length=8, max_length=64)
    transaction_id: str = Field(min_length=8, max_length=64)
    event_version: int = Field(ge=1)
    event_type: str = Field(min_length=3, max_length=40)
    event_timestamp: datetime
    transaction_timestamp: datetime
    customer_id: str = Field(min_length=3, max_length=64)
    card_id: str = Field(min_length=3, max_length=64)
    merchant_id: str = Field(min_length=3, max_length=64)
    merchant_category: str = Field(min_length=2, max_length=40)
    merchant_country: str = Field(min_length=2, max_length=2)
    device_id: str = Field(min_length=3, max_length=64)
    ip_address: str
    channel: Channel
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3)
    status: TransactionStatus
    is_fraud: bool | None = None
    source_system: str = Field(min_length=2, max_length=40)

    @field_validator("currency", "merchant_country")
    @classmethod
    def uppercase_codes(cls, value: str) -> str:
        return value.upper()

    @field_validator("ip_address")
    @classmethod
    def valid_ip(cls, value: str) -> str:
        import ipaddress
        ipaddress.ip_address(value)
        return value
