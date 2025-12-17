"use client";

import { useState } from "react";

export default function UploadPage() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false); // FIXED "the" bug
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // Solana theme colors
  const COLORS = {
    bg: "#0A0A0B",
    card: "#1A1A1E",
    text: "#EAEAEA",
    subtext: "#BFBFBF",
    accent: "#14F195",
    purple: "#9945FF",
    buttonText: "#FFFFFF",
    danger: "#F15060",
  };

  const handleUpload = async () => {
    if (!text && !file) {
      setError("Please enter text or select a file.");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      // ✅ HARDCODED WALLET ADDRESS (required by backend)
      const walletAddress =
        "ANamGVSXoSgxW2UM5bBEWLHJRztnTCHBbTv1favFTTWC";

      let finalContent = text;

      // convert file → text
      if (file) {
        const fileText = await file.text();
        finalContent = fileText;
      }

      // ✅ MUST MATCH backend expected JSON EXACTLY
      const payload = {
        title: text.split("\n")[0] || "Untitled",
        content: finalContent, // string
        wallet_address: walletAddress, // string
      };

      const res = await fetch("http://localhost:5000/api/upload/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // backend requires JSON
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`Server error: ${res.status} ${txt}`);
      }

      const data = await res.json();

      setResult({
        hash: data.content_hash,
        cid: data.cid,
        owner: data.creator_pubkey,
      });

      setText("");
      setFile(null);
    } catch (err) {
      console.error(err);
      setError("Upload failed. See console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: 700,
        margin: "0 auto",
        padding: 20,
        background: COLORS.bg,
        color: COLORS.text,
      }}
    >
      <h2 style={{ marginBottom: 12 }}>Upload Original Work</h2>

      {error && (
        <p style={{ color: COLORS.danger, marginBottom: 12 }}>{error}</p>
      )}

      <div style={{ marginBottom: 20 }}>
        <label
          style={{
            display: "block",
            marginBottom: 4,
            color: COLORS.subtext,
          }}
        >
          Enter Text:
        </label>
        <textarea
          rows={6}
          style={{
            width: "100%",
            padding: 10,
            borderRadius: 6,
            border: "1px solid #2e2e32",
            background: "#0E0E0F",
            color: COLORS.text,
            marginTop: 5,
            resize: "vertical",
          }}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      </div>

      <div style={{ marginBottom: 20 }}>
        <label
          style={{
            display: "block",
            marginBottom: 4,
            color: COLORS.subtext,
          }}
        >
          Or Upload a File:
        </label>
        <input
          type="file"
          style={{ display: "block", marginTop: 5 }}
          onChange={(e) => setFile(e.target.files[0])}
        />
      </div>

      <button
        onClick={handleUpload}
        disabled={loading}
        style={{
          padding: "10px 20px",
          background: `linear-gradient(90deg, ${COLORS.purple}, ${COLORS.accent})`,
          color: COLORS.buttonText,
          border: "none",
          borderRadius: 6,
          cursor: "pointer",
        }}
      >
        {loading ? "Uploading..." : "Upload"}
      </button>

      {result && (
        <div
          style={{
            marginTop: 30,
            background: COLORS.card,
            padding: 16,
            borderRadius: 8,
            border: "1px solid #262628",
          }}
        >
          <h3 style={{ marginBottom: 8 }}>Upload Successful</h3>
          <p>
            <strong>Hash:</strong> {result.hash}
          </p>
          <p>
            <strong>CID:</strong> {result.cid}
          </p>
          <p>
            <strong>Owner (Solana pubkey):</strong> {result.owner}
          </p>
        </div>
      )}
    </div>
  );
}
