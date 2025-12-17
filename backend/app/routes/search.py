from flask import Blueprint, request, jsonify
from ..crawler.google_search import execute_google_search
from ..crawler.parse_results import extract_and_clean_results
from ..matcher.text_similarity import get_combined_match_score

search_bp = Blueprint('search', __name__)

@search_bp.route('/', methods=['POST'])
def perform_search():
    """
    API endpoint to initiate the search for potential infringements.
    """
    print("DEBUG: /search endpoint hit.")

    payload = request.get_json()
    print(f"DEBUG: Received payload: {payload}")

    if not payload or 'content' not in payload:
        print("DEBUG ERROR: Missing 'content' in payload.")
        return jsonify({"status": "error", "message": "Missing 'content' in payload"}), 400

    original_content = payload['content']
    print(f"DEBUG: Extracted original content length: {len(original_content)}")

    # 1. Execute Search (Off-chain)
    print("DEBUG: Starting Google search...")
    raw_results = execute_google_search(original_content)
    print(f"DEBUG: Raw results received: {len(raw_results)} items")

    # 2. Parse Results
    print("DEBUG: Parsing and cleaning results...")
    parsed_results = extract_and_clean_results(raw_results)
    print(f"DEBUG: Parsed results count: {len(parsed_results)}")

    final_matches = []
    
    # 3. Score Matches
    print("DEBUG: Beginning scoring of each parsed result...")
    for index, result in enumerate(parsed_results):
        print(f"DEBUG: Scoring result #{index + 1}: {result}")

        # Get the match scores
        scores = get_combined_match_score(original_content, result['content_snippet'])
        print(f"DEBUG: Scores for result #{index + 1}: {scores}")

        # Combine the search data with the scores
        match_record = {
            **result,
            "scores": scores
        }
        final_matches.append(match_record)

    print(f"DEBUG: Final matches prepared: {len(final_matches)}")

    return jsonify({
        "status": "success",
        "original_content_length": len(original_content),
        "total_results_found": len(raw_results),
        "potential_infringements": final_matches
    }), 200
