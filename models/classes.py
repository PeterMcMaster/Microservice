from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ClassBase(BaseModel):
    name: str = Field(
        ...,
        description="Name of the class.",
        json_schema_extra={"example": "Mathematics 101"},
    )
    description: Optional[str] = Field(
        None,
        description="Description of the class.",
        json_schema_extra={"example": "An introductory course to Mathematics."},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Mathematics 101",
                    "description": "An introductory course to Mathematics."
                }
            ]
        }
    }

class ClassCreate(ClassBase):
    """Creation payload for a Class."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Mathematics 101",
                    "description": "An introductory course to Mathematics."
                }
            ]
        }
    }

class ClassUpdate(BaseModel):
    """Update payload for a Class."""
    name: Optional[str] = Field(
        None,
        description="Name of the class.",
        json_schema_extra={"example": "Mathematics 102"},
    )
    description: Optional[str] = Field(
        None,
        description="Description of the class.",
        json_schema_extra={"example": "A second course in Mathematics."},
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Mathematics 102",
                    "description": "A second course in Mathematics."
                }
            ]
        }
    }

class ClassRead(ClassBase):
    """Read payload for a Class."""
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
                    "name": "Mathematics 101",
                    "description": "An introductory course to Mathematics.",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z"
                }
            ]
        }
    }



        

        

