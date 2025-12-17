import hashlib
import json

def generate_content_hash(data: str) -> str:
    """
    Generates a cryptographic hash for the content. 
    This is the immutable fingerprint stored on Solana.
    
    :param data: The raw text content or file content as a string.
    :return: SHA256 hex digest of the content.
    """
    # Normalize the data before hashing to ensure consistency
    normalized_data = data.strip().lower().encode('utf-8')
    
    # Use SHA-256 for a strong, widely accepted hash
    return hashlib.sha256(normalized_data).hexdigest()

def generate_transaction_hash(tx_data: dict) -> str:
    """
    Generates a hash for a structured transaction payload.
    Used internally for indexing or logging.
    
    :param tx_data: Dictionary of data to be hashed.
    :return: SHA256 hash of the JSON-serialized data.
    """
    # Sort keys to ensure consistent hashing across runs
    json_string = json.dumps(tx_data, sort_keys=True)
    return hashlib.sha256(json_string.encode('utf-8')).hexdigest()

# Example usage (will be called from routes)
# content_hash = generate_content_hash("My original masterpiece text.")