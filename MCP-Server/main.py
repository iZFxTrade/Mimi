#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware # Import CORS
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import auth, crud, models, schemas, database, database_init
from datetime import timedelta

# --- Initialization ---
models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="MCP-Server", version="0.1.0")

# ===============================================
# ===           MIDDLEWARE SETUP              ===
# ===============================================

# Add CORS middleware to allow requests from the frontend
# This is the crucial fix for the 404 errors you were seeing.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for simplicity in development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"], # Allows all major methods
    allow_headers=["*"],  # Allows all headers
)


def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

@app.on_event("startup")
def on_startup():
    with database.SessionLocal() as db:
        database_init.init_database(db)

# ===============================================
# ===          AUTHENTICATION & USERS         ===
# ===============================================

@app.post("/api/auth/token", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=schemas.User, tags=["Users"])
def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

# ===============================================
# ===      ADMIN: USER CRUD OPERATIONS        ===
# ===============================================

@app.post("/api/users/", response_model=schemas.User, tags=["Admin: Users"], dependencies=[Depends(auth.require_admin)])
def create_user_as_admin(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/api/users/", response_model=list[schemas.User], tags=["Admin: Users"], dependencies=[Depends(auth.require_admin)])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/api/users/{user_id}", response_model=schemas.User, tags=["Admin: Users"], dependencies=[Depends(auth.require_admin)])
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/api/users/{user_id}", response_model=schemas.User, tags=["Admin: Users"], dependencies=[Depends(auth.require_admin)])
def update_user_as_admin(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Admin: Users"], dependencies=[Depends(auth.require_admin)])
def delete_user_as_admin(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return # No content on success


# ===============================================
# ===       GENERAL DATA GETTERS (READ)       ===
# ===============================================
@app.get("/api/assistants/", response_model=list[schemas.Assistant], tags=["Data"])
def read_assistants(user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return db.query(models.Assistant).all() if user.role == 'Admin' else crud.get_user_items(db, user.id, models.Assistant)

@app.get("/api/homes/", response_model=list[schemas.Home], tags=["Data"])
def read_homes(user: models.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return db.query(models.Home).all() if user.role == 'Admin' else crud.get_user_items(db, user.id, models.Home)

@app.get("/api/rooms/", response_model=list[schemas.Room], tags=["Data"])
def read_rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).all()

@app.get("/api/devices/", response_model=list[schemas.Device], tags=["Data"])
def read_devices(db: Session = Depends(get_db)):
    return db.query(models.Device).all()

@app.get("/api/scenes/", response_model=list[schemas.Scene], tags=["Data"])
def read_scenes(db: Session = Depends(get_db)):
    return db.query(models.Scene).all()

@app.get("/api/models/", response_model=list[schemas.AIModel], tags=["Data"])
def read_aimodels(db: Session = Depends(get_db)): return db.query(models.AIModel).all()

@app.get("/api/tools/", response_model=list[schemas.Tool], tags=["Data"])
def read_tools(db: Session = Depends(get_db)): return db.query(models.Tool).all()

@app.get("/api/actions/", response_model=list[schemas.Action], tags=["Data"])
def read_actions(db: Session = Depends(get_db)): return db.query(models.Action).all()