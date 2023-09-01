import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

DATA_PATH = os.environ.get("DATA_PATH")
MAX_NEW_TOKENS = int(os.environ.get("MAX_NEW_TOKENS"))
TEMPERATURE = float(os.environ.get("TEMPERATURE"))
CONTEXT_SIZE = int(os.environ.get("CONTEXT_SIZE"))
RETURN_SOURCE_DOCUMENTS = bool(os.environ.get("RETURN_SOURCE_DOCUMENTS"))
VECTOR_COUNT = int(os.environ.get("VECTOR_COUNT"))
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP"))
EMBEDDING_MODEL_NAME = os.environ.get("EMBEDDING_MODEL_NAME")
MODEL_TYPE = os.environ.get("MODEL_TYPE")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)
HUGGING_FACE_API_URL = os.environ.get("HUGGING_FACE_API_URL", None)
HUGGING_FACE_HUB_TOKEN = os.environ.get("HUGGING_FACE_HUB_TOKEN", None)
MODEL_PATH = os.environ.get("MODEL_PATH", None)
MODEL_URL_PATH = os.environ.get("MODEL_URL_PATH", None)
