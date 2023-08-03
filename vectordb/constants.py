import os

from dotenv import load_dotenv

load_dotenv()

PINECONE_LIMIT_EXCEEDED_MSG = "The index exceeds the project quota of 1 pods by 1 pods. Upgrade your account or change the project settings to increase the quota."
PINECONE_DEFAULT_INDEX_DIMENSIONS = 1536
PINECONE_DEFAULT_POD_TYPE = "s1.x1"
PINECONE_DEFAULT_METRIC = "cosine"

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

BAD_REQUEST = 400
NOT_FOUND = 404

EMBEDDING_MODEL = "text-embedding-ada-002"

PRICING_TOKENS = 1000
