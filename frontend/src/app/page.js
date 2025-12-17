"use client";

import Link from "next/link";
import WalletConnect from "./components/WalletConnect";

export default function Home() {
  const COLORS = {
    accent: "#14F195",
    purple: "#9945FF",
    text: "#EAEAEA",
    subtext: "#BFBFBF",
    buttonText: "#FFFFFF",
    bg: "#0A0A0B",
    card: "#1A1A1E",
  };

  const buttonStyle = {
    padding: "12px 25px",
    fontSize: 16,
    fontWeight: "bold",
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
    color: COLORS.buttonText,
    background: `linear-gradient(90deg, ${COLORS.purple}, ${COLORS.accent})`,
    transition: "transform 0.1s",
  };

  return (
    <div
      style={{
        padding: 60,
        textAlign: "center",
        background: COLORS.bg,
        minHeight: "100vh",
        color: COLORS.text,
      }}
    >

      {/* ---------------- TOP RIGHT WALLET BUTTON ---------------- */}
      <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: 20 }}>
        <WalletConnect />
      </div>
      {/* --------------------------------------------------------- */}

      <h1
        style={{
          fontSize: 48,
          fontWeight: "bold",
          background: `linear-gradient(135deg, ${COLORS.purple}, ${COLORS.accent})`,
          WebkitBackgroundClip: "text",
          color: "transparent",
          marginBottom: 20,
        }}
      >
        IP Shield
      </h1>

      <p
        style={{
          fontSize: 18,
          color: COLORS.subtext,
          maxWidth: 600,
          margin: "0 auto",
        }}
      >
        Register your work, detect copyright misuse,
        and prove ownership on-chain.
      </p>

      <div
        style={{
          marginTop: 50,
          display: "flex",
          justifyContent: "center",
          gap: 25,
          flexWrap: "wrap",
        }}
      >
        <Link href="/upload">
          <button style={buttonStyle}>Register Content</button>
        </Link>

        <Link href="/search">
          <button style={buttonStyle}>Scan the Internet</button>
        </Link>

        <Link href="/history">
          <button style={buttonStyle}>View Your History</button>
        </Link>
      </div>
    </div>
  );
}
