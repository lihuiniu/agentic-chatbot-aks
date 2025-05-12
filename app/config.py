import os

class Settings:
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
    COSMOS_DB_URI = os.getenv("COSMOS_DB_URI", "")
    COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY", "")
    COSMOS_DB_NAME = os.getenv("COSMOS_DB_NAME", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    DELTA_LAKE_PATH = os.getenv("DELTA_LAKE_PATH", "/mnt/data/delta")

settings = Settings()