import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# Base class for models
Base = declarative_base()

# In-memory SQLite engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
