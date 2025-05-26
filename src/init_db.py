from models import Base
from utils.db_connection import get_db_client


def init_db():
    db_client = get_db_client()
    engine = db_client.engine
    print("Creating all tables if they do not exist...")
    Base.metadata.create_all(engine)
    print("Database initialization complete.")


if __name__ == "__main__":
    init_db()
