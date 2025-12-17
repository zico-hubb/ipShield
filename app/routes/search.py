from flask import Blueprint, request, jsonify
from ..crawler.google_search import execute_google_search
from ..crawler.parse_results import extract_and_clean_results
from ..matcher.text_similarity import get_combined_match_score


search_bp = Blueprint('search', __name__)

@search_bp.route('/', methods=['POST'])
def perform_search():
    """
    API endpoint to initiate the search for potential infringements.
    
    Steps:
    1. Get content (or content hash + retrieval link) from payload.
    2. Run Google Search on a snippet of the content.
    3. Parse and clean search results.
    4. Score each result against the original content.
    """
    payload = request.get_json()
    if not payload or 'content' not in payload:
        return jsonify({"status": "error", "message": "Missing 'content' in payload"}), 400

    original_content = payload['content']
    
    # 1. Execute Search (Off-chain)
    raw_results = execute_google_search(original_content)
    
    # 2. Parse Results
    parsed_results = extract_and_clean_results(raw_results)
    
    final_matches = []
    # 3. Score Matches
    for result in parsed_results:
        # Get the match scores
        scores = get_combined_match_score(original_content, result['content_snippet'])
        
        # Combine the search data with the scores
        match_record = {
            **result,
            "scores": scores
        }
        final_matches.append(match_record)
        
    return jsonify({
        "status": "success",
        "original_content_length": len(original_content),
        "total_results_found": len(raw_results),
        "potential_infringements": final_matches
    }), 200