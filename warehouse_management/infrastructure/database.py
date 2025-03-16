from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from warehouse_management.infrastructure.orm import Base
from warehouse_management.settings import Settings

engine = create_engine(Settings.DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)

DATABASE_URL = 'sqlite:///warehouse.db'

def init_db() -> None:
    """Initialize the database."""
    Base.metadata.create_all(engine)
