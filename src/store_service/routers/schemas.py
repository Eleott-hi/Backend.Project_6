from typing import Optional, Annotated
from uuid import UUID
from datetime import datetime, date
import enum
from pydantic import BaseModel, EmailStr, StringConstraints, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


class AddressRequest(BaseModel):
    country: str
    city: str
    street: str


class AddressResponse(AddressRequest):
    id: UUID


class SupplierRequest(BaseModel):
    name: str
    phone_number: PhoneNumber
    address_id: Optional[UUID] = None


class SupplierResponse(SupplierRequest):
    id: UUID


class ProductRequest(BaseModel):
    name: str
    category: str
    price: float
    available_stock: int
    supplier_id: Optional[UUID] = None
    image_id: Optional[UUID] = None


class ProductResponse(ProductRequest):
    id: UUID
    last_update_date: datetime


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class ClientRequest(BaseModel):
    client_name: str
    client_surname: str
    birthday: date
    gender: Gender
    address_id: Optional[UUID] = None


class ClientResponse(ClientRequest):
    id: UUID
    registration_date: datetime


class RegistrationRequest(BaseModel):
    name: Annotated[
        str, StringConstraints(strip_whitespace=True,
                               min_length=1, max_length=256)
    ]
    surname: Annotated[
        str, StringConstraints(strip_whitespace=True,
                               min_length=1, max_length=256)
    ]
    email: EmailStr
    phone_number: PhoneNumber
    password: Annotated[
        str, StringConstraints(strip_whitespace=True,
                               min_length=7, max_length=256)
    ]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@example.com",
                "phone_number": "+79241325785",
                "password": "mysecretpassword"
            }
        }


class LoginRequest(BaseModel):
    email: EmailStr
    password: Annotated[
        str, StringConstraints(strip_whitespace=True,
                               min_length=7, max_length=256)
    ]

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "mysecretpassword"
            }
        }


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com"
            }
        }


class ChangePasswordRequest(BaseModel):
    email: EmailStr
    old_password: Annotated[
        str, StringConstraints(strip_whitespace=True,
                               min_length=7, max_length=256)
    ]
    new_password: Annotated[
        str, StringConstraints(strip_whitespace=True,
                               min_length=7, max_length=256)
    ]

    @model_validator(mode='after')
    def check_passwords_not_match(self) -> 'ChangePasswordRequest':
        if self.old_password == self.new_password:
            raise ValueError('Passwords match')
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "old_password": "mysecretpassword",
                "new_password": "mynewsecretpassword"
            }
        }
