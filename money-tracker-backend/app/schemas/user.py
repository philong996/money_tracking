from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    """Schema for user creation."""
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str
