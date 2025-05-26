import os
from dotenv import load_dotenv


# loads .env file, will not overide already set enviroment variables (will do nothing when testing, building and deploying)
load_dotenv()


DEBUG = os.getenv('DEBUG', 'False') in ['True', 'true']
PORT = os.getenv('PORT', '8080')
POD_NAME = os.getenv('POD_NAME', 'pod_name_not_set')

POSTGRES_USER = os.getenv('POSTGRES_USER', '').strip()
POSTGRES_PASS = os.getenv('POSTGRES_PASS', '').strip()
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '').strip()
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '').strip()
POSTGRES_DB = os.getenv('POSTGRES_DB', '').strip()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-05-01-preview")
AZURE_API_VERSION_FILES = os.getenv("AZURE_API_VERSION_FILES", "2024-10-21")
AZURE_API_VERSION_VECTORS = os.getenv("AZURE_API_VERSION_VECTORS", "2025-03-01-preview")

ASSISTANT_ID = os.getenv("ASSISTANT_ID")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "assistenten")
PREDEFINED_QUESTIONS = [q for q in os.getenv("PREDEFINED_QUESTIONS", "Hvad kan du hjælpe mig med?").split(";") if q.strip()]
