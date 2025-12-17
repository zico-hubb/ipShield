from web3.auto.solana import w3 # Using web3.auto.solana for client mocking
from solana.rpc.api import Client as SolanaClient
from solders.keypair import Keypair
from typing import Optional

class SolanaConnectionError(Exception):
    """Custom exception for Solana connection errors."""
    pass

class SolanaProgramClient:
    """
    Mocks the client connection and setup for interacting with the Solana Program.
    
    In a real app, this class would handle:
    1. Initializing the Solana RPC client.
    2. Loading the fee payer Keypair.
    3. Setting up the Anchor/Program Client pointing to the Program ID.
    """
    def __init__(self, cluster_url: str, program_id: str, keypair_path: str):
        self.cluster_url = cluster_url
        self.program_id = program_id
        self.fee_payer: Optional[Keypair] = None
        self.client: Optional[SolanaClient] = None

        self._initialize_connection()
        self._load_fee_payer(keypair_path)

    def _initialize_connection(self):
        """Mocks connecting to the Solana cluster."""
        try:
            self.client = SolanaClient(self.cluster_url)
            # Ping the cluster (mocked)
            # self.client.get_health() 
            print(f"MOCK: Connected to Solana cluster at {self.cluster_url}")
        except Exception as e:
            raise SolanaConnectionError(f"Failed to connect to Solana: {e}")

    def _load_fee_payer(self, keypair_path: str):
        """Mocks loading the fee payer keypair."""
        try:
            # In a real app: self.fee_payer = Keypair.from_file(keypair_path)
            # Here we mock a random keypair for simulation
            self.fee_payer = Keypair()
            print(f"MOCK: Fee payer loaded. Public Key: {self.fee_payer.public_key}")
        except Exception as e:
            raise SolanaConnectionError(f"Failed to load fee payer keypair: {e}")

    def get_program_id(self) -> str:
        """Returns the mock program ID."""
        return self.program_id

    def get_client(self) -> SolanaClient:
        """Returns the initialized Solana client (mocked)."""
        return self.client
    
    def get_fee_payer_pubkey(self) -> str:
        """Returns the fee payer's public key as a string."""
        return str(self.fee_payer.public_key)

# Example usage (called from transactions.py and routes)
# from flask import current_app
# solana_client = SolanaProgramClient(
#     cluster_url=current_app.config['SOLANA_CLUSTER_URL'],
#     program_id=current_app.config['SOLANA_PROGRAM_ID'],
#     keypair_path=current_app.config['FEE_PAYER_KEYPAIR_PATH']
# )