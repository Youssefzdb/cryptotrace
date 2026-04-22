#!/usr/bin/env python3
"""Bitcoin Transaction Tracer - Using public blockchain APIs"""
import requests

class BTCTracer:
    def __init__(self, address):
        self.address = address
        self.api_base = "https://blockstream.info/api"

    def get_address_info(self):
        try:
            r = requests.get(f"{self.api_base}/address/{self.address}", timeout=10)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[-] API error: {e}")
        return {}

    def get_transactions(self, limit=10):
        try:
            r = requests.get(f"{self.api_base}/address/{self.address}/txs", timeout=10)
            if r.status_code == 200:
                txs = r.json()[:limit]
                result = []
                for tx in txs:
                    result.append({
                        "txid": tx.get("txid","")[:16] + "...",
                        "value_in":  sum(inp.get("prevout", {}).get("value", 0) for inp in tx.get("vin", [])),
                        "value_out": sum(out.get("value", 0) for out in tx.get("vout", [])),
                        "confirmed": tx.get("status", {}).get("confirmed", False),
                        "block": tx.get("status", {}).get("block_height", "mempool")
                    })
                    print(f"[+] TX: {tx.get('txid','')[:16]}... block={result[-1]['block']}")
                return result
        except Exception as e:
            print(f"[-] TX fetch error: {e}")
        return []

    def trace(self):
        print(f"[*] Tracing BTC address: {self.address}")
        info = self.get_address_info()
        txs = self.get_transactions()
        return {
            "chain": "BTC",
            "address": self.address,
            "tx_count": info.get("chain_stats", {}).get("tx_count", 0),
            "total_received": info.get("chain_stats", {}).get("funded_txo_sum", 0),
            "balance": info.get("chain_stats", {}).get("funded_txo_sum", 0) - info.get("chain_stats", {}).get("spent_txo_sum", 0),
            "transactions": txs
        }
