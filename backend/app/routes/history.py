from flask import Blueprint, request, jsonify, current_app
from firebase_admin import firestore
from ..solana.transactions import fetch_on_chain_history
from typing import List, Dict, Any

history_bp = Blueprint('history', __name__)

@history_bp.route('/', methods=['GET'])
def get_user_history():
    """
    API endpoint to fetch a user's content registration and infringement history.
    
    It fetches data from two sources:
    1. Firestore: Detailed off-chain report data (infringing URLs, snippets).
    2. Solana (Mock): Core on-chain registration and claim proof.
    """
    user_id = request.args.get('user_id')
    solana_pubkey = request.args.get('solana_pubkey')
    
    if not user_id or not solana_pubkey:
        return jsonify({"status": "error", "message": "Missing 'user_id' or 'solana_pubkey' query parameters"}), 400

    # 1. Fetch Off-Chain History from Firestore
    firestore_reports: List[Dict[str, Any]] = []
    try:
        db = current_app.db
        app_id = current_app.app_id
        
        if db and app_id:
            # Firestore path: /artifacts/{appId}/users/{userId}/infringement_reports
            collection_path = f"artifacts/{app_id}/users/{user_id}/infringement_reports"
            reports_ref = db.collection(collection_path).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(50).stream()
            for doc in reports_ref:
                report_data = doc.to_dict()
                report_data['id'] = doc.id
                # Convert firestore.SERVER_TIMESTAMP to a usable format if possible
                if report_data.get('timestamp') and hasattr(report_data['timestamp'], 'isoformat'):
                    report_data['timestamp'] = report_data['timestamp'].isoformat()
                firestore_reports.append(report_data)
        else:
            print("MOCK DB: Cannot fetch history, using mock Solana data only.")
            
    except Exception as e:
        current_app.logger.error(f"Firestore fetch error: {e}")
        
    # 2. Fetch On-Chain Registration History from Solana (Mock)
    solana_history = fetch_on_chain_history(current_app, solana_pubkey)

    # 3. Combine and return
    return jsonify({
        "status": "success",
        "user_id": user_id,
        "solana_pubkey": solana_pubkey,
        "on_chain_registrations": solana_history,
        "off_chain_reports": firestore_reports
    }), 200