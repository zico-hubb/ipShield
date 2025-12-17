"use client";

import Link from "next/link";

export default function Navbar() {
  return (
    <nav style={{
      background: "#0A0A0B",
      padding: "18px 45px",
      borderBottom: "1px solid #1A1A1E",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      position: "sticky",
      top: 0,
      zIndex: 100,
    }}>
      <h2 style={{
        background: "linear-gradient(135deg, #9945FF, #14F195)",
        WebkitBackgroundClip: "text",
        color: "transparent",
        fontSize: "24px",
        fontWeight: "bold",
      }}>
        Ip Shield
      </h2>

      <div style={{
        display: "flex",
        gap: "25px",
        fontSize: "16px"
      }}>
        <Link href="/">Home</Link>
        <Link href="/upload">Register</Link>
        <Link href="/scan">Scan</Link>
        <Link href="/history">History</Link>
      </div>
    </nav>
  );
}
