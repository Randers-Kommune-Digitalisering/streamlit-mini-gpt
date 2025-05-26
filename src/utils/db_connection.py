from utils.config import POSTGRES_USER, POSTGRES_PASS, POSTGRES_HOST, POSTGRES_DB
from utils.database import DatabaseClient
from models import Base  # Import Base for table creation
import logging


def get_db_client():
    client = DatabaseClient(
        db_type='postgresql',
        database=POSTGRES_DB,
        username=POSTGRES_USER,
        password=POSTGRES_PASS,
        host=POSTGRES_HOST,
        port='5432'
    )
    try:
        # Try to create tables if they do not exist
        Base.metadata.create_all(client.engine)
    except Exception as e:
        logging.getLogger(__name__).error(f"Error initializing database tables: {e}")
    return client
