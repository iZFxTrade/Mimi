#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Optional
from pydantic import BaseModel

# Pydantic's orm_mode will tell the Pydantic model to read the data
# even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
# In Pydantic V2, this is renamed to `from_attributes`
class Config: 
    from_attributes = True

# --- Schemas cho Model AI (AIModel) ---
class AIModelBase(BaseModel):
    name: str
    provider: Optional[str] = None
    purpose: Optional[str] = None
    status: Optional[str] = "Inactive"

class AIModelCreate(AIModelBase):
    pass

class AIModel(AIModelBase):
    id: int
    class Config(Config):
        pass

# --- Schemas cho Trợ lý (Assistant) ---
class AssistantBase(BaseModel):
    name: str
    base_model: str

class AssistantCreate(AssistantBase):
    pass

class Assistant(AssistantBase):
    id: int
    owner_id: int
    class Config(Config):
        pass

# --- Schemas cho Thiết bị (Device) ---
class DeviceBase(BaseModel):
    name: str
    type: str
    status: Optional[str] = "Off"

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    owner_id: int
    room_id: Optional[int] = None
    class Config(Config):
        pass

# --- Schemas cho Phòng (Room) ---
class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    home_id: int
    devices: List[Device] = []
    class Config(Config):
        pass

# --- Schemas cho Nhà (Home) ---
class HomeBase(BaseModel):
    name: str

class HomeCreate(HomeBase):
    pass

class Home(HomeBase):
    id: int
    owner_id: int
    rooms: List[Room] = []
    class Config(Config):
        pass

# --- Schemas cho Người dùng (User) ---
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "Free"

class User(UserBase):
    id: int
    role: str
    homes: List[Home] = []
    devices: List[Device] = []
    assistants: List[Assistant] = []
    class Config(Config):
        pass


# --- Schemas cho Xác thực (Authentication) ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
