"use client";

import { useState } from "react";
import Link from "next/link";
import "./globals.css";
import { WalletProvider } from "./context/WalletContext";
import WalletConnect from "./components/WalletConnect";

export default function RootLayout({ children }) {
  const [open, setOpen] = useState(false);

  return (
    <html lang="en">
      <body style={styles.body}>
        <WalletProvider>
          <WalletConnect />

          <button style={styles.menuButton} onClick={() => setOpen(true)}>
            ☰
          </button>

          {open && <div style={styles.overlay} onClick={() => setOpen(false)} />}

          <div
            style={{
              ...styles.sidebar,
              left: open ? "0px" : "-260px",
            }}
          >
            <h2 style={styles.logo}>ipShield</h2>

            <nav style={styles.nav}>
              <Link href="/" style={styles.link} onClick={() => setOpen(false)}>
                Home
              </Link>
              <Link href="/upload" style={styles.link} onClick={() => setOpen(false)}>
                Upload
              </Link>
              <Link href="/search" style={styles.link} onClick={() => setOpen(false)}>
                Search
              </Link>
              <Link href="/report" style={styles.link} onClick={() => setOpen(false)}>
                Report
              </Link>
              <Link href="/history" style={styles.link} onClick={() => setOpen(false)}>
                History
              </Link>
            </nav>
          </div>

          <main style={styles.mainContent}>{children}</main>
        </WalletProvider>
      </body>
    </html>
  );
}

const styles = {
  body: {
    margin: 0,
    padding: 0,
    backgroundColor: "#0A0A0B",
    color: "#EAEAEA",
    fontFamily: "sans-serif",
  },

  menuButton: {
    position: "fixed",
    top: 20,
    left: 20,
    background: "linear-gradient(135deg, #9945FF, #14F195)",
    border: "none",
    padding: "10px 14px",
    borderRadius: 8,
    color: "white",
    fontSize: 20,
    cursor: "pointer",
    zIndex: 2000,
  },

  overlay: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100vw",
    height: "100vh",
    backgroundColor: "rgba(0,0,0,0.5)",
    zIndex: 1500,
  },

  sidebar: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "260px",
    height: "100vh",
    backgroundColor: "#111114",
    padding: "30px 20px",
    boxShadow: "2px 0px 10px rgba(0,0,0,0.5)",
    zIndex: 1600,
    transition: "left 0.2s ease-in-out",
  },

  logo: {
    fontSize: "26px",
    fontWeight: "bold",
    background: "linear-gradient(135deg, #9945FF, #14F195)",
    WebkitBackgroundClip: "text",
    color: "transparent",
    marginBottom: "40px",
  },

  nav: {
    display: "flex",
    flexDirection: "column",
    gap: "18px",
  },

  link: {
    color: "#EAEAEA",
    textDecoration: "none",
    fontSize: "18px",
    padding: "10px 5px",
    borderRadius: "8px",
    backgroundColor: "#1A1A1E",
  },

  mainContent: {
    marginLeft: 0,
    padding: "30px",
    minHeight: "100vh",
  },
};
