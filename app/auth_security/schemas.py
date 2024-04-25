from pydantic import BaseModel, Field, validator


class UserDTO(BaseModel):
    name: str
    password: str
    telephone: int
    experience: int
    role: str

    @validator('telephone', 'experience')
    def must_be_positive(cls, value):
        if value < 0:
            raise ValueError('Must be a positive number')
        return value
