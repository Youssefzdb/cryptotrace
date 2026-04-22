#!/usr/bin/env python3
"""Wallet Analyzer - Risk scoring and pattern detection"""

# Known mixing/tumbler services (public info)
KNOWN_MIXERS = ["ChipMixer", "Wasabi", "CoinJoin", "Tornado.Cash"]
# Known exchange hot wallet patterns
HIGH_VOLUME_THRESHOLD = 10_000_000_000  # satoshis (100 BTC equivalent)

class WalletAnalyzer:
    def __init__(self, address, tx_data):
        self.address = address
        self.tx_data = tx_data if isinstance(tx_data, list) else tx_data.get("transactions", [])

    def analyze(self):
        findings = []
        risk_score = 0

        # Check transaction volume
        if len(self.tx_data) > 100:
            findings.append({"indicator": "High transaction volume", "severity": "MEDIUM"})
            risk_score += 20

        # Check for round number transactions (common in laundering)
        for tx in self.tx_data:
            val = tx.get("value_eth", tx.get("value_out", 0))
            if val > 0 and val == int(val):
                findings.append({"indicator": f"Round number TX: {val}", "severity": "LOW"})
                risk_score += 5
                break

        # Risk level
        level = "LOW" if risk_score < 20 else "MEDIUM" if risk_score < 50 else "HIGH"
        print(f"[+] Risk Score: {risk_score}/100 ({level})")

        return {
            "risk_score": risk_score,
            "risk_level": level,
            "findings": findings,
            "tx_count": len(self.tx_data)
        }
