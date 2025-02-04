from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./vet_clinic.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)