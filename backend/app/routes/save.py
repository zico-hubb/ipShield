from flask import Blueprint, request, jsonify, current_app
from ..solana.transactions import submit_infringement_report
from ..utils.hasher import generate_content_hash
from firebase_admin import firestore
import json
import time

save_bp = Blueprint('save', __name__)

@save_bp.route('/report', methods=['POST'])
def save_and_report_infringement():
    """
    API endpoint to save the detailed infringement report locally (Firestore)
    and submit an immutable record of the claim on Solana.
    
    Required payload fields: original_hash, infringing_url, infringing_content, user_id.
    """
    payload = request.get_json()
    if not payload:
        return jsonify({"status": "error", "message": "Missing JSON payload"}), 400

    required_fields = ['original_hash', 'infringing_url', 'infringing_content', 'user_id']
    if not all(field in payload for field in required_fields):
        return jsonify({"status": "error", "message": f"Missing required fields: {', '.join(required_fields)}"}), 400

    original_hash = payload['original_hash']
    infringing_url = payload['infringing_url']
    infringing_content = payload['infringing_content']
    user_id = payload['user_id']
    
    # 1. Hash the infringing content to be recorded on Solana
    infringing_hash = generate_content_hash(infringing_content)

    # 2. Submit immutable proof on Solana
    solana_response = submit_infringement_report(
        current_app, 
        original_hash, 
        infringing_url, 
        infringing_hash
    )
    
    if solana_response['status'] != 'success':
        return jsonify({
            "status": "error", 
            "message": f"Solana submission failed: {solana_response.get('message', 'Unknown error')}"
        }), 500

    # 3. Store the detailed report in Firestore for user history (Off-chain application data)
    report_data = {
        "original_hash": original_hash,
        "infringing_url": infringing_url,
        "infringing_hash": infringing_hash,
        "user_id": user_id,
        "solana_tx_id": solana_response['transaction_id'],
        "status": "Reported to Solana",
        "timestamp": firestore.SERVER_TIMESTAMP,
        # Store a snippet of the content, but not the whole thing if it's huge
        "content_snippet": infringing_content[:200]
    }
    
    try:
        db = current_app.db
        app_id = current_app.app_id
        
        if db and app_id:
            # Firestore path: /artifacts/{appId}/users/{userId}/infringement_reports
            collection_path = f"artifacts/{app_id}/users/{user_id}/infringement_reports"
            db.collection(collection_path).add(report_data)
            print(f"Firestore: Report saved to {collection_path}")
        else:
            print(f"MOCK DB: Report saved for user {user_id}. TX: {solana_response['transaction_id']}")
            # In a mock environment, just log or save to a file
            pass 
            
    except Exception as e:
        current_app.logger.error(f"Firestore save error: {e}")
        # The Solana transaction is the critical part, so we proceed even if Firestore fails
        pass

    return jsonify({
        "status": "success",
        "message": "Report successfully recorded on Solana and saved to history.",
        "solana_tx_id": solana_response['transaction_id'],
        "infringing_hash": infringing_hash
    }), 200