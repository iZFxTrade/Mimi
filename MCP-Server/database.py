#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./mcp_database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_all_tables():
    """
    Creates all tables in the database that are defined in models inheriting from Base.
    This is safe to run multiple times; it will not re-create existing tables.
    """
    print("Initializing database and creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("Database initialization complete.")
