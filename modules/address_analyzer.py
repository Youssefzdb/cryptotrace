#!/usr/bin/env python3
"""Address Risk Analyzer - Detect suspicious patterns"""

KNOWN_BLACKLIST = {
    "1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F": "Silk Road wallet",
    "12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw": "Ransomware wallet",
}

class AddressAnalyzer:
    def __init__(self, address, coin):
        self.address = address
        self.coin = coin

    def assess_risk(self):
        risk = {"address": self.address, "coin": self.coin, "flags": [], "risk_level": "LOW"}

        # Check known blacklist
        if self.address in KNOWN_BLACKLIST:
            risk["flags"].append(f"BLACKLISTED: {KNOWN_BLACKLIST[self.address]}")
            risk["risk_level"] = "CRITICAL"
            print(f"[!] BLACKLISTED ADDRESS: {self.address}")

        # Heuristic checks
        if self.coin == "btc":
            if self.address.startswith("1"):
                risk["flags"].append("Legacy P2PKH address format")
            elif self.address.startswith("bc1"):
                risk["flags"].append("Native SegWit (bech32) address")
            elif self.address.startswith("3"):
                risk["flags"].append("P2SH address (multisig or script)")

        if not risk["flags"]:
            risk["flags"].append("No known risk indicators")

        print(f"[+] Risk assessment: {risk['risk_level']}")
        return risk
