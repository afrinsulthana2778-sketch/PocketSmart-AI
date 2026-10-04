from typing import List

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


class RegisterRequest(BaseModel):

    email: str

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    full_name: str = Field(
        min_length=2,
        max_length=100,
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):

        value = value.strip().lower()

        if "@" not in value:

            raise ValueError(
                "Enter a valid email address"
            )

        return value


class LoginRequest(BaseModel):

    email: str

    password: str


class RoomInput(BaseModel):

    room_type: str = Field(
        min_length=2,
        max_length=60,
    )

    quantity: int = Field(
        default=1,
        ge=1,
        le=20,
    )

    style: str = Field(
        default="Modern",
        max_length=60,
    )


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=100000000,
    )

    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=3,
    )

    rooms: List[RoomInput] = Field(
        min_length=1,
        max_length=20,
    )

    requirements: List[str] = Field(
        default_factory=list,
        max_length=30,
    )

    location: str = Field(
        default="India",
        max_length=100,
    )


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=100000000,
    )

    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=3,
    )

    guest_count: int = Field(
        gt=0,
        le=100000,
    )

    event_type: str = Field(
        min_length=2,
        max_length=60,
    )

    venue: str = Field(
        default="Not specified",
        max_length=120,
    )

    location: str = Field(
        default="India",
        max_length=100,
    )

    preferences: List[str] = Field(
        default_factory=list,
        max_length=30,
    )


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=100000000,
    )

    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=3,
    )

    occasion: str = Field(
        min_length=2,
        max_length=80,
    )

    style: str = Field(
        default="Elegant",
        max_length=80,
    )

    outfit_description: str = Field(
        default="",
        max_length=1000,
    )