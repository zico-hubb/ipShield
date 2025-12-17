"use client";

import { useState } from "react";

export default function SearchPage() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");

  const COLORS = {
    bg: "#0A0A0B",
    card: "#1A1A1E",
    text: "#EAEAEA",
    subtext: "#BFBFBF",
    accent: "#14F195",
    purple: "#9945FF",
    danger: "#F15060",
    buttonText: "#FFFFFF",
  };

  const handleSearch = async () => {
    if (!text.trim()) {
      setError("Please enter text to search.");
      return;
    }

    setError("");
    setLoading(true);
    setResults([]);

    try {
      const res = await fetch("http://localhost:5000/api/search/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: text }), // matches Flask route
      });

      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`Server error: ${res.status} ${txt}`);
      }

      const data = await res.json();

      // Expecting a list of results: [{ url, similarity }]
      setResults(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setError("Search failed. See console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", padding: 30, background: COLORS.bg, color: COLORS.text }}>
      <div style={{ maxWidth: 800, margin: "0 auto" }}>
        <h2 style={{ fontSize: 28, marginBottom: 12 }}>Search the Web</h2>
        <p style={{ color: COLORS.subtext, marginBottom: 20 }}>
          Paste your text below to search for potential copyright infringements.
        </p>

        {error && <p style={{ color: COLORS.danger, marginBottom: 12 }}>{error}</p>}

        <textarea
          rows={6}
          placeholder="Enter text to search"
          style={{
            width: "100%",
            padding: 10,
            borderRadius: 6,
            border: "1px solid #2e2e32",
            background: "#0E0E0F",
            color: COLORS.text,
            marginBottom: 12,
            resize: "vertical",
            fontSize: 14,
          }}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button
          onClick={handleSearch}
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
          {loading ? "Searching..." : "Search"}
        </button>

        {results.length > 0 && (
          <div style={{ marginTop: 20 }}>
            <h3 style={{ marginBottom: 12 }}>Results</h3>
            <div style={{ background: COLORS.card, padding: 16, borderRadius: 8, border: "1px solid #262628" }}>
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr>
                    <th style={{ textAlign: "left", padding: 8, color: COLORS.subtext }}>URL</th>
                    <th style={{ textAlign: "left", padding: 8, color: COLORS.subtext }}>Similarity (%)</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((r, idx) => (
                    <tr key={idx}>
                      <td style={{ padding: 8, color: COLORS.text }}>
                        <a href={r.url} target="_blank" rel="noreferrer" style={{ color: COLORS.accent, textDecoration: "none" }}>
                          {r.url.length > 70 ? r.url.slice(0, 70) + "…" : r.url}
                        </a>
                      </td>
                      <td style={{ padding: 8, color: COLORS.text }}>{r.similarity}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {results.length === 0 && !loading && (
          <p style={{ color: COLORS.subtext, marginTop: 20 }}>No results yet. Run a search above.</p>
        )}
      </div>
    </div>
  );
}
