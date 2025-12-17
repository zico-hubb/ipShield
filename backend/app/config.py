import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "my_secret_key")
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"
    SERPAPI_KEY = os.environ.get("serpapi_key", "my_serpapi_key")
    SERPAPI_BASE_URL = os.environ.get("SERPAPI_BASE_URL", "https://serpapi.com/search")
    SOLANA_CLUSTER_URL = os.environ.get("SOLANA_CLUSTER_URL", "https://api.devnet.solana.com")
    SOLANA_PROGRAM_ID = os.environ.get("SOLANA_PROGRAM_ID", "EXAMPLE_PROGRAM_ID")
    FEE_PAYER_KEYPAIR_PATH = os.environ.get("FEE_PAYER_KEYPAIR_PATH", "keys/fee_payer.json")
