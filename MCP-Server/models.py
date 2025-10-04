#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import Base từ file database.py
# Tất cả các model sẽ kế thừa từ lớp Base này
from .database import Base

# Model cho Người dùng (User)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="Free") # Các role: Admin, VIP, Free

    # Mối quan hệ: Một User có thể sở hữu nhiều Assistant, Device, Home
    assistants = relationship("Assistant", back_populates="owner")
    devices = relationship("Device", back_populates="owner")
    homes = relationship("Home", back_populates="owner")

# Model cho Trợ lý (Assistant)
class Assistant(Base):
    __tablename__ = "assistants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    base_model = Column(String, nullable=False) # ví dụ: 'gpt-4o'
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="assistants")

# Model cho Nhà thông minh (Home)
class Home(Base):
    __tablename__ = "homes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="homes")
    
    rooms = relationship("Room", back_populates="home")

# Model cho Phòng (Room)
class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    
    home_id = Column(Integer, ForeignKey("homes.id"))
    home = relationship("Home", back_populates="rooms")

    devices = relationship("Device", back_populates="room")

# Model cho Thiết bị (Device)
class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True) # ví dụ: 'Light', 'Sensor', 'AC'
    status = Column(String, default="Off")

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="devices")

    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    room = relationship("Room", back_populates="devices")

# Model cho các mô hình AI (Model)
class AIModel(Base):
    __tablename__ = "aimodels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    provider = Column(String) # ví dụ: 'Ollama', 'Groq', 'OpenAI'
    purpose = Column(String) # ví dụ: 'Smart Home Control', 'General Chat'
    status = Column(String, default="Inactive") # Active / Inactive
