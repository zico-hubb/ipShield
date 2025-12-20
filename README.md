# ipShield 🛡️

**Protect and monitor your intellectual property on-chain.**

ipShield is a full-stack web application designed to help content creators detect and report copyright infringements. It integrates off-chain search, fuzzy and semantic similarity detection, and on-chain recording via Solana to provide a robust proof-of-ownership and DMCA reporting system.

---

## 📺 Project Demo

**[Watch the ipShield Demo Video](https://youtu.be/_yzxHZ_lBXw?si=sl9z0x6eySBl_IE0)**

[![ipShield Demo](https://img.youtube.com/vi/_yzxHZ_lBXw/0.jpg)](https://youtu.be/_yzxHZ_lBXw?si=sl9z0x6eySBl_IE0)

---

## ✨ Features

### 1. Content Upload & Registration
* **Upload:** Creators can upload their original content securely.
* **On-Chain Proof:** Each piece of content is hashed and optionally registered on the Solana blockchain (Devnet) to establish immutable proof of ownership.
* **Decentralized Storage:** Utilizes IPFS for decentralized content storage.

### 2. Plagiarism & Infringement Detection
* **Smart Search:** Uses **SerpAPI** (Google Search) to crawl the web for potential copies of your content.
* **Advanced Matching:** Implements **Fuzzy Matching** (`fuzzywuzzy`) and **Semantic Similarity** (TF-IDF + Cosine Similarity) to accurately detect infringements.
* **Ranked Results:** Returns a prioritized list of potential infringing URLs based on similarity scores.

### 3. DMCA Automation
* **One-Click Reporting:** Generates a ready-to-use DMCA takedown notice.
* **Automated Delivery:** Sends the notice via email, including the content URL, infringing URL, and creator details.

### 4. Solana Integration
* **Registry:** Registers original content hashes on the Solana Devnet.
* **Reporting:** Allows for the submission of infringement reports directly on-chain.
* **History:** Fetches registration and infringement history associated with any creator's wallet.

### 5. Backend Architecture
* **Modular API:** Python Flask REST API organized into Blueprints (`upload`, `search`, `save`, `history`, `dcma`).
* **Logging:** Integrated with Firebase Firestore for optional logging and data persistence.

### 6. Modern Frontend
* **Responsive UI:** Built with **Next.js** (React-based) for a seamless user experience.
* **Dashboard:** Displays content status, search results, and infringement history in an intuitive interface.
* **Admin Panel:** Tools to mint and view on-chain content records.

---

## 🛠️ Tech Stack

### 🎨 Frontend
* **Framework:** Next.js, React
* **Styling:** CSS / Tailwind (implied)

### ⚙️ Backend
* **Language:** Python
* **Framework:** Flask
* **Utilities:** Flask-CORS, Requests

### ⛓️ Blockchain
* **Network:** Solana (Devnet)
* **Framework:** Anchor
* **Storage:** IPFS

### 🔍 Search & Analysis
* **Search API:** SerpAPI (Google Search)
* **Text Analysis:** `fuzzywuzzy`, `scikit-learn` (TF-IDF + Cosine Similarity)

### 🗄️ Database
* **DB:** Firebase Firestore