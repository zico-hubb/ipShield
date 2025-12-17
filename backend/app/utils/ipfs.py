from typing import Tuple

# NOTE: This file is purely a mock. In a real application, you would use
# libraries like 'web3.storage' or 'pyarweave' to handle file uploads.

def upload_to_decentralized_storage(content: str, file_type: str = "text/plain") -> Tuple[str, str]:
    """
    Mocks uploading content to a decentralized storage network (like IPFS/Arweave).
    
    The actual content is NOT stored on Solana; only its hash and the CID are.

    :param content: The content string to be stored.
    :param file_type: The MIME type of the content.
    :return: A tuple of (CID/Arweave ID, Gateway URL).
    """
    # Simulate CID generation based on content hash for demonstration
    from ..utils.hasher import generate_content_hash
    content_hash = generate_content_hash(content)
    
    # Mock CID
    mock_cid = f"Qm{content_hash[:44]}" 
    # Mock Gateway URL
    mock_url = f"https://mock-ipfs-gateway.io/{mock_cid}"
    
    print(f"MOCK: Uploaded content. CID: {mock_cid}")
    
    return mock_cid, mock_url

def retrieve_from_decentralized_storage(cid: str) -> str:
    """
    Mocks retrieving content using a CID/Arweave ID.
    
    :param cid: The CID/Arweave ID of the content.
    :return: A mock content string.
    """
    # In a real app, this would perform a request to the gateway
    return f"Retrieved content for CID: {cid} (MOCK DATA)"