from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class AccountBase(BaseModel):
    username: str = Field(
        ...,
        description="Username for the account.",
        json_schema_extra={"example": "user123"},
    )
    number_id: int = Field(
        ...,
        description="ID associated with the account.",
        json_schema_extra={"example": 42}, 
    )
    amount: float = Field(
        ...,
        description="Monetary amount in the account.",
        json_schema_extra={"example": 1000.50},
    )

    model_config = {
        "json_schema_extra": { 
            "examples": [
                {
                    "username": "user123",
                    "number_id": 42,
                    "amount": 1000.50
                }
            ]
        }
    }

class AccountCreate(AccountBase):
    """Creation payload for an Account."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "user123",
                    "number_id": 42,
                    "amount": 1000.50
                }
            ]
        }
    }

class AccountUpdate(BaseModel):
    """Update payload for an Account."""
    username: Optional[str] = Field(
        None,
        description="Username for the account.",
        json_schema_extra={"example": "newuser123"},
    )
    number_id: Optional[int] = Field(
        None,
        description="ID associated with the account.",
        json_schema_extra={"example": 43}, 
    )
    amount: Optional[float] = Field(
        None,
        description="Monetary amount in the account.",
        json_schema_extra={"example": 1500.75},
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "newuser123",
                    "number_id": 43,
                    "amount": 1500.75
                }
            ]
        }
    }

class AccountRead(AccountBase):
    """Read payload for an Account, including metadata."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Account ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "user123",
                    "number_id": 42,
                    "amount": 1000.50,
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-02T15:30:00Z"
                }
            ]
        }
    }
