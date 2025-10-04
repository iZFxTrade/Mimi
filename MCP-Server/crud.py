#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from . import models, schemas, auth

# ===============================================
# ===              USER CRUD                  ===
# ===============================================

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role,
        is_mock=user.is_mock
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> models.User | None:
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    
    if "password" in update_data and update_data["password"]:
        hashed_password = auth.get_password_hash(update_data["password"])
        db_user.hashed_password = hashed_password
        del update_data['password'] # Don't try to set it twice

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

# ===============================================
# ===           GENERIC CRUD (for UI)         ===
# ===============================================
# Helper to get items owned by a specific user
def get_user_items(db: Session, user_id: int, model):
    return db.query(model).filter(model.owner_id == user_id).all()


# ===============================================
# ===      SPECIFIC ITEM CRUD (to be expanded) ===
# ===============================================

def create_assistant(db: Session, assistant: schemas.AssistantCreate, owner_id: int):
    db_assistant = models.Assistant(**assistant.model_dump(), owner_id=owner_id)
    db.add(db_assistant)
    db.commit()
    db.refresh(db_assistant)
    return db_assistant

def create_home(db: Session, home: schemas.HomeCreate, owner_id: int):
    db_home = models.Home(**home.model_dump(), owner_id=owner_id)
    db.add(db_home)
    db.commit()
    db.refresh(db_home)
    return db_home

def create_room(db: Session, room: schemas.RoomCreate, home_id: int):
    db_room = models.Room(**room.model_dump(), home_id=home_id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def create_device(db: Session, device: schemas.DeviceCreate, owner_id: int, room_id: int):
    db_device = models.Device(**device.model_dump(), owner_id=owner_id, room_id=room_id)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def create_aimodel(db: Session, model: schemas.AIModelCreate):
    db_model = models.AIModel(**model.model_dump())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model
