"use client";

import { useState } from "react";

export default function ReportPage() {
  const [originalHash, setOriginalHash] = useState("");
  const [infringingUrl, setInfringingUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

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

  const handleSubmit = async () => {
    if (!originalHash.trim() || !infringingUrl.trim()) {
      setMessage("Please fill in both fields.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const res = await fetch("http://localhost:5000/api/save/report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          original_hash: originalHash,
          infringing_url: infringingUrl,
          infringing_content: "",
          user_id: "user" 
        }),
      });

      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`Server error: ${res.status} ${txt}`);
      }

      const data = await res.json();

      setMessage(`✅ Report submitted successfully! Tx: ${data.txHash || "N/A"}`);
      setOriginalHash("");
      setInfringingUrl("");
    } catch (err) {
      console.error(err);
      setMessage("❌ Failed to submit report. Check console.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 700, margin: "0 auto", padding: 20, background: COLORS.bg, color: COLORS.text }}>
      <h2 style={{ marginBottom: 12 }}>Submit Infringement Report</h2>
      <p style={{ color: COLORS.subtext, marginBottom: 20 }}>
        Provide the original content hash and the URL of the infringing content. This will save the report on Solana.
      </p>

      <div style={{ marginBottom: 16 }}>
        <label style={{ display: "block", marginBottom: 4, color: COLORS.subtext }}>Original Content Hash</label>
        <input
          type="text"
          placeholder="Enter original hash"
          style={{
            width: "100%",
            padding: 10,
            borderRadius: 6,
            border: "1px solid #2e2e32",
            background: "#0E0E0F",
            color: COLORS.text,
            marginBottom: 12,
            fontSize: 14,
          }}
          value={originalHash}
          onChange={(e) => setOriginalHash(e.target.value)}
        />

        <label style={{ display: "block", marginBottom: 4, color: COLORS.subtext }}>Infringing URL</label>
        <input
          type="text"
          placeholder="Enter infringing URL"
          style={{
            width: "100%",
            padding: 10,
            borderRadius: 6,
            border: "1px solid #2e2e32",
            background: "#0E0E0F",
            color: COLORS.text,
            fontSize: 14,
          }}
          value={infringingUrl}
          onChange={(e) => setInfringingUrl(e.target.value)}
        />
      </div>

      <button
        onClick={handleSubmit}
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
        {loading ? "Submitting..." : "Submit Report"}
      </button>

      {message && (
        <p style={{ marginTop: 16, color: message.includes("✅") ? COLORS.accent : COLORS.danger }}>
          {message}
        </p>
      )}
    </div>
  );
}
