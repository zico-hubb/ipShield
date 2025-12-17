                                ipShield

ipShield is a full-stack web application that helps content creators detect and report copyright infringements. It integrates off-chain search, fuzzy and semantic similarity detection, and on-chain recording via Solana. It also provides a DMCA reporting system.

                            Features
 1. Content Upload & Registration
- Creators can upload their original content.
- Each piece of content is hashed and optionally registered on the Solana blockchain for proof of ownership.
- IPFS can be used for decentralized storage.

 2. Plagiarism & Infringement Detection
- Uses Google search via SerpAPI to find potential copies.
- Fuzzy matching (`fuzzywuzzy`) and semantic similarity (TF-IDF + cosine similarity) to detect potential infringements.
- Returns a ranked list of potential infringing content.

 3. DMCA Notice
- Sends a ready-to-use DMCA takedown notice via email.
- Accepts content URL, infringing URL, and creator information.

 4. On-Chain Recording (Solana)
- Registers original content hash on Solana Devnet.
- Allows submission of infringement reports.
- Fetches registration and infringement history for any creator wallet.

5. Backend
- Python Flask REST API with modular structure.
- Routes are organized as Blueprints: `upload`, `search`, `save`, `history`, `dcma`.
- Integrates with Firebase Firestore for logging (optional).

 6. Frontend
- Built with Next.js (React-based) for responsive UI.
- Displays content, search results, and infringement history.
- Admin panel to mint and view on-chain content records.

                   Tech Stack

 Backend:
   Python, Flask, Flask-CORS, Requests  
Frontend:
   Next.js, React  
Blockchain:
  Solana (Devnet), Anchor  
Storage:
  IPFS  
Search API:
  SerpAPI (Google search)  
Text Analysis: 
  fuzzywuzzy, scikit-learn (TF-IDF + cosine similarity)  
Database:
  Firebase Firestore 



