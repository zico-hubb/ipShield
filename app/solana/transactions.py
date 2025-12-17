import time
from typing import Dict, Any, List
from solders.pubkey import Pubkey  # NOTE: class name is now `Pubkey`

from .client import SolanaProgramClient, SolanaConnectionError

# Global variable to simulate the on-chain registry state for testing/mocking
MOCK_ON_CHAIN_REGISTRY: Dict[str, Dict[str, Any]] = {}

def get_solana_client(app) -> SolanaProgramClient:
    """Helper to initialize or retrieve the Solana client from the application context."""
    # This is a simple, non-thread-safe way; a real Flask app would use something like
    # Flask-SQLAlchemy or a proper Service/Singleton pattern.
    if not hasattr(app, 'solana_client'):
        app.solana_client = SolanaProgramClient(
            cluster_url=app.config['SOLANA_CLUSTER_URL'],
            program_id=app.config['SOLANA_PROGRAM_ID'],
            keypair_path=app.config['FEE_PAYER_KEYPAIR_PATH']
        )
    return app.solana_client


def register_content_on_chain(app, content_hash: str, creator_pubkey: str, ipfs_cid: str) -> Dict[str, str]:
    """
    Mocks the transaction that registers the original content hash on Solana.

    :param app: The Flask application object.
    :param content_hash: The unique hash of the content.
    :param creator_pubkey: The Solana wallet address of the creator.
    :param ipfs_cid: The ID for the content stored on decentralized storage.
    :return: Dictionary containing the transaction ID and status.
    """
    try:
        solana_client = get_solana_client(app)
    except SolanaConnectionError as e:
        return {"status": "error", "message": f"Solana connection failed: {e}"}

    # --- MOCK TRANSACTION LOGIC ---
    tx_id = f"mock-reg-tx-{int(time.time())}"
    
    # Simulate writing the data to a Program Derived Address (PDA)
    MOCK_ON_CHAIN_REGISTRY[content_hash] = {
        "hash": content_hash,
        "creator": creator_pubkey,
        "cid": ipfs_cid,
        "timestamp": int(time.time()),
        "program_id": solana_client.get_program_id(),
        "mock_account_address": str(PublicKey())
    }

    print(f"MOCK: Registered content hash {content_hash} on Solana. Tx ID: {tx_id}")
    
    return {
        "status": "success", 
        "transaction_id": tx_id, 
        "account_address": MOCK_ON_CHAIN_REGISTRY[content_hash]["mock_account_address"]
    }

def submit_infringement_report(app, original_hash: str, infringing_url: str, infringing_hash: str) -> Dict[str, str]:
    """
    Mocks the transaction that submits an infringement report on Solana.

    :param app: The Flask application object.
    :param original_hash: The registered hash of the original content.
    :param infringing_url: The URL where the copy was found.
    :param infringing_hash: The hash of the discovered content.
    :return: Dictionary containing the transaction ID and status.
    """
    try:
        get_solana_client(app)
    except SolanaConnectionError as e:
        return {"status": "error", "message": f"Solana connection failed: {e}"}

    # --- MOCK TRANSACTION LOGIC ---
    if original_hash not in MOCK_ON_CHAIN_REGISTRY:
        return {"status": "error", "message": "Original content hash not found in registry (mock)."}

    tx_id = f"mock-report-tx-{int(time.time())}"
    
    # In a real app, this would create a new Infringement PDA account
    report_data = {
        "original_hash": original_hash,
        "infringing_url": infringing_url,
        "infringing_hash": infringing_hash,
        "reporter_pubkey": "MockReporterPubkey",
        "status": "REPORTED",
        "timestamp": int(time.time())
    }
    
    # Append report to the mock registry for simulation
    MOCK_ON_CHAIN_REGISTRY[original_hash]['reports'] = MOCK_ON_CHAIN_REGISTRY[original_hash].get('reports', [])
    MOCK_ON_CHAIN_REGISTRY[original_hash]['reports'].append(report_data)

    print(f"MOCK: Submitted infringement report for {original_hash}. Tx ID: {tx_id}")

    return {"status": "success", "transaction_id": tx_id}

def fetch_on_chain_history(app, pubkey: str) -> List[Dict[str, Any]]:
    """
    Mocks fetching all content registration and infringement history 
    associated with a Solana public key.
    
    :param app: The Flask application object.
    :param pubkey: The Solana wallet address to check.
    :return: List of registration and report records.
    """
    try:
        get_solana_client(app)
    except SolanaConnectionError:
        return []

    # Filter mock registry by creator public key
    history = []
    for hash_key, data in MOCK_ON_CHAIN_REGISTRY.items():
        if data['creator'] == pubkey:
            history.append({
                "type": "Registration",
                "hash": hash_key,
                "timestamp": data['timestamp'],
                "cid": data['cid'],
                "reports": data.get('reports', [])
            })
            
    return history