"use client";

import { useEffect, useState } from "react";
import { useWallet } from "../context/WalletContext";

export default function WalletConnect() {
  const [connected, setConnected] = useState(false);
  const [publicKey, setPublicKey] = useState("");

  // Check if Phantom is installed
  useEffect(() => {
    if (typeof window !== "undefined" && window.solana?.isPhantom) {
      window.solana.on("connect", () => {
        setConnected(true);
        setPublicKey(window.solana.publicKey.toString());
      });

      window.solana.on("disconnect", () => {
        setConnected(false);
        setPublicKey("");
      });
    }
  }, []);

  // Connect function
  const connectWallet = async () => {
    try {
      if (!window.solana) {
        alert("Phantom Wallet not found. Install the extension first.");
        return;
      }

      const resp = await window.solana.connect();
      setConnected(true);
      setPublicKey(resp.publicKey.toString());
    } catch (err) {
      console.error("Connection Error:", err);
    }
  };

  // Disconnect function
  const disconnectWallet = async () => {
    try {
      await window.solana.disconnect();
    } catch (err) {
      console.error("Disconnect Error:", err);
    }
  };

  return (
    <div style={{ position: "absolute", top: 20, right: 20 }}>
      {!connected ? (
        <button
          onClick={connectWallet}
          style={{
            padding: "10px 20px",
            background: "linear-gradient(90deg, #9945FF, #14F195)",
            border: "none",
            borderRadius: 8,
            color: "white",
            cursor: "pointer",
          }}
        >
          Connect Phantom
        </button>
      ) : (
        <button
          onClick={disconnectWallet}
          style={{
            padding: "10px 20px",
            background: "#222",
            border: "1px solid #444",
            borderRadius: 8,
            color: "#14F195",
            cursor: "pointer",
          }}
        >
          {publicKey.slice(0, 4)}...{publicKey.slice(-4)}
        </button>
      )}
    </div>
  );
}
