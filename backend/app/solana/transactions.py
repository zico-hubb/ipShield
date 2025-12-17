from typing import Dict, Any, List
from flask import current_app
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solders.transaction import Transaction
from solders.hash import Hash
from solana.rpc.types import TxOpts
from .client import SolanaProgramClient, SolanaConnectionError

def get_solana_client(app) -> SolanaProgramClient:
    if not hasattr(app, "solana_client"):
        app.solana_client = SolanaProgramClient(
            cluster_url=app.config.get("SOLANA_CLUSTER_URL", "https://api.devnet.solana.com"),
            program_id=app.config.get("SOLANA_PROGRAM_ID", "EXAMPLE_PROGRAM_ID"),
            keypair_path=app.config.get("FEE_PAYER_KEYPAIR_PATH", "fee_payer.json")
        )
    return app.solana_client

def register_content_on_chain(app, content_hash: str, creator_pubkey: str, ipfs_cid: str) -> Dict[str, str]:
    try:
        solana = get_solana_client(app)
        client = solana.get_client()
        fee_payer = solana.fee_payer
        creator = Pubkey.from_string(creator_pubkey)
        blockhash = client.get_latest_blockhash().value.blockhash
        tx = Transaction(fee_payer=fee_payer.pubkey(), recent_blockhash=Hash.from_string(blockhash))
        tx.add(
            transfer(
                TransferParams(
                    from_pubkey=fee_payer.pubkey(),
                    to_pubkey=creator,
                    lamports=1
                )
            )
        )
        sig = client.send_transaction(tx, fee_payer, opts=TxOpts(skip_preflight=True)).value
        return {
            "status": "success",
            "transaction_id": str(sig),
            "program_id": solana.get_program_id()
        }
    except SolanaConnectionError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def submit_infringement_report(app, original_hash: str, infringing_url: str, infringing_hash: str) -> Dict[str, str]:
    try:
        solana = get_solana_client(app)
        client = solana.get_client()
        fee_payer = solana.fee_payer
        blockhash = client.get_latest_blockhash().value.blockhash
        tx = Transaction(fee_payer=fee_payer.pubkey(), recent_blockhash=Hash.from_string(blockhash))
        sig = client.send_transaction(tx, fee_payer, opts=TxOpts(skip_preflight=True)).value
        return {
            "status": "success",
            "transaction_id": str(sig)
        }
    except SolanaConnectionError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def fetch_on_chain_history(app, pubkey: str) -> List[Dict[str, Any]]:
    try:
        solana = get_solana_client(app)
        client = solana.get_client()
        owner = Pubkey.from_string(pubkey)
        sigs = client.get_signatures_for_address(owner).value
        history = []
        for s in sigs:
            history.append({
                "signature": str(s.signature),
                "slot": s.slot
            })
        return history
    except Exception:
        return []
