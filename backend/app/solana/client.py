from solana.rpc.api import Client as SolanaClient
from solders.keypair import Keypair
from typing import Optional

class SolanaConnectionError(Exception):
    pass

class SolanaProgramClient:
    def __init__(self, cluster_url: str, program_id: str, keypair_path: str):
        self.cluster_url = cluster_url
        self.program_id = program_id
        self.fee_payer: Optional[Keypair] = None
        self.client: Optional[SolanaClient] = None
        self._initialize_connection()
        self._load_fee_payer(keypair_path)

    def _initialize_connection(self):
        try:
            self.client = SolanaClient(self.cluster_url)
            self.client.get_health()
        except Exception as e:
            raise SolanaConnectionError(str(e))

    def _load_fee_payer(self, keypair_path: str):
        try:
            self.fee_payer = Keypair.from_file(keypair_path)
        except Exception as e:
            raise SolanaConnectionError(str(e))

    def get_program_id(self) -> str:
        return self.program_id

    def get_client(self) -> SolanaClient:
        return self.client

    def get_fee_payer_pubkey(self) -> str:
        return str(self.fee_payer.pubkey())
