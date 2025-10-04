#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from . import crud, schemas, models

def init_database(db: Session):
    # Kiểm tra xem đã có dữ liệu chưa
    users = crud.get_users(db, skip=0, limit=1)
    if users:
        print("Database already contains data. Skipping initialization.")
        return

    print("Database is empty. Initializing with demo data...")

    # --- Tạo người dùng Demo ---
    user_admin_schema = schemas.UserCreate(
        username="admin",
        password="admin",
        email="admin@example.com",
        full_name="Admin User",
        role="Admin",
        is_mock=True
    )
    user_admin = crud.create_user(db=db, user=user_admin_schema)

    # --- Tạo Năng lực AI (Models, Tools, Actions) Demo ---
    # Models
    llm_model = crud.create_aimodel(db, schemas.AIModelCreate(name="llama3-8b-mock", provider="Ollama", purpose="LLM", is_mock=True))
    tts_model = crud.create_aimodel(db, schemas.AIModelCreate(name="speecht5_tts-mock", provider="HuggingFace", purpose="TTS", is_mock=True))
    stt_model = crud.create_aimodel(db, schemas.AIModelCreate(name="whisper-base-mock", provider="OpenAI", purpose="STT", is_mock=True))
    
    # Tools & Actions (sẽ được hiện thực hóa sau, hiện tại chỉ là placeholder)
    # crud.create_tool(...)
    # crud.create_action(...)

    # --- Tạo Trợ lý Demo ---
    assistant_schema = schemas.AssistantCreate(
        name="MiMi",
        description="Trợ lý ảo demo",
        llm_id=llm_model.id,
        tts_id=tts_model.id,
        stt_id=stt_model.id,
        is_mock=True
    )
    crud.create_assistant(db=db, assistant=assistant_schema, owner_id=user_admin.id)

    # --- Tạo Nhà thông minh Demo ---
    home_schema = schemas.HomeCreate(name="Ngôi nhà Mẫu", address="123 Demo Street", is_mock=True)
    home = crud.create_home(db=db, home=home_schema, owner_id=user_admin.id)

    # --- Tạo Phòng Demo ---
    room_living_room = crud.create_room(db, schemas.RoomCreate(name="Phòng khách", is_mock=True), home_id=home.id)
    room_bedroom = crud.create_room(db, schemas.RoomCreate(name="Phòng ngủ", is_mock=True), home_id=home.id)

    # --- Tạo Thiết bị Demo ---
    crud.create_device(db, schemas.DeviceCreate(name="Đèn thông minh", type="Light", status="Off", is_mock=True), owner_id=user_admin.id, room_id=room_living_room.id)
    crud.create_device(db, schemas.DeviceCreate(name="Máy lạnh", type="AC", status="On", is_mock=True), owner_id=user_admin.id, room_id=room_bedroom.id)

    # --- Tạo Chế độ Demo ---
    # Logic tạo Scene (chế độ) sẽ được thêm vào sau khi model Scene được hoàn thiện

    print("Demo data created successfully.")

