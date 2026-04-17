from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "taller.db"


def get_database_url() -> str:
    return f"sqlite:///{DB_PATH}"


engine = None
SessionLocal = None
Base = declarative_base()


def init_db(database_url: str = None):
    global engine, SessionLocal

    url = database_url or get_database_url()

    if "sqlite" in url:
        engine = create_engine(
            url, connect_args={"check_same_thread": False}, poolclass=StaticPool
        )
    else:
        engine = create_engine(url)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    create_tables()
    return engine


def create_tables():
    from infrastructure.models.models import (
        ClienteModel,
        EquipoModel,
        OrdenModel,
        TecnicoModel,
        RepuestoModel,
        ItemOrdenModel,
        FacturaModel,
    )

    Base.metadata.create_all(bind=engine)


def get_session():
    if SessionLocal is None:
        init_db()
    return SessionLocal()
