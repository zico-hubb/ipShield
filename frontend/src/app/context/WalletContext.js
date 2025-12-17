"use client";

import { createContext, useContext, useEffect, useState } from "react";

const WalletContext = createContext();

export const WalletProvider = ({ children }) => {
  const [wallet, setWallet] = useState(null);
  const [publicKey, setPublicKey] = useState(null);

  // Load wallet from localStorage (persist)
  useEffect(() => {
    const stored = localStorage.getItem("phantom_pubkey");
    if (stored) setPublicKey(stored);
  }, []);

  const connect = async () => {
    if (!window.solana || !window.solana.isPhantom) {
      alert("Phantom wallet not found!");
      return;
    }

    const res = await window.solana.connect();
    setPublicKey(res.publicKey.toString());
    setWallet(window.solana);

    // Persist across refresh/navigation
    localStorage.setItem("phantom_pubkey", res.publicKey.toString());
  };

  const disconnect = async () => {
    if (wallet) await wallet.disconnect();
    setPublicKey(null);
    localStorage.removeItem("phantom_pubkey");
  };

  return (
    <WalletContext.Provider value={{ wallet, publicKey, connect, disconnect }}>
      {children}
    </WalletContext.Provider>
  );
};

export const useWallet = () => useContext(WalletContext);
