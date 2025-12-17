from flask import Blueprint, request, jsonify, current_app
from ..utils.hasher import generate_content_hash
from ..utils.validator import validate_registration_payload, ValidationException
from ..utils.ipfs import upload_to_decentralized_storage
from ..solana.transactions import register_content_on_chain
import json

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/', methods=['POST'])
def register_content():
    """
    API endpoint to register new original content on the Solana blockchain.
    """
    print("DEBUG: Received request to /upload endpoint")

    payload = request.get_json()
    print(f"DEBUG: Raw payload received: {payload}")

    if not payload:
        print("DEBUG ERROR: Missing JSON payload")
        return jsonify({"status": "error", "message": "Missing JSON payload"}), 400

    try:
        # 1. Validate Input
        print("DEBUG: Validating payload...")
        validate_registration_payload(payload)
        print("DEBUG: Payload is valid.")

        content = payload['content']
        wallet_address = payload['wallet_address']
        print(f"DEBUG: Extracted content and wallet_address: {wallet_address}")

        # 2. Hash Content
        print("DEBUG: Generating content hash...")
        content_hash = generate_content_hash(content)
        print(f"DEBUG: Content hash generated: {content_hash}")

        # 3. Upload to Decentralized Storage
        print("DEBUG: Uploading content to decentralized storage...")
        ipfs_cid, ipfs_url = upload_to_decentralized_storage(content)
        print(f"DEBUG: Received from decentralized storage -> CID: {ipfs_cid}, URL: {ipfs_url}")

        # 4. Register on Solana
        print("DEBUG: Registering content on Solana blockchain...")
        solana_response = register_content_on_chain(
            current_app, 
            content_hash, 
            wallet_address, 
            ipfs_cid
        )
        print(f"DEBUG: Solana registration response: {solana_response}")

        if solana_response['status'] != 'success':
            print("DEBUG ERROR: Solana registration failed.")
            return jsonify({
                "status": "error", 
                "message": f"Solana registration failed: {solana_response.get('message', 'Unknown error')}"
            }), 500

        print("DEBUG: Registration successful, preparing final response.")

        return jsonify({
            "status": "success",
            "message": "Content registered successfully.",
            "content_hash": content_hash,
            "creator_pubkey": wallet_address,
            "cid": ipfs_cid,
            "solana_tx_id": solana_response['transaction_id']
        }), 200

    except ValidationException as e:
        print(f"DEBUG VALIDATION ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

    except Exception as e:
        print(f"DEBUG UNEXPECTED ERROR: {e}")
        current_app.logger.error(f"Upload error: {e}")
        return jsonify({"status": "error", "message": "Internal server error during registration."}), 500
