#!/usr/bin/env python3
"""Ethereum Transaction Tracer - Using Etherscan public API"""
import requests

ETHERSCAN_API = "https://api.etherscan.io/api"

class ETHTracer:
    def __init__(self, address, api_key=""):
        self.address = address
        self.api_key = api_key or "YourApiKeyToken"  # Free tier works for basic queries

    def get_balance(self):
        try:
            params = {"module": "account", "action": "balance",
                      "address": self.address, "tag": "latest", "apikey": self.api_key}
            r = requests.get(ETHERSCAN_API, params=params, timeout=10)
            if r.status_code == 200:
                data = r.json()
                wei = int(data.get("result", 0))
                eth = wei / 10**18
                print(f"[+] Balance: {eth:.4f} ETH")
                return eth
        except Exception as e:
            print(f"[-] Balance error: {e}")
        return 0

    def get_transactions(self, limit=10):
        try:
            params = {"module": "account", "action": "txlist",
                      "address": self.address, "startblock": 0,
                      "endblock": 99999999, "page": 1, "offset": limit,
                      "sort": "desc", "apikey": self.api_key}
            r = requests.get(ETHERSCAN_API, params=params, timeout=10)
            if r.status_code == 200:
                txs = r.json().get("result", [])
                result = []
                for tx in txs[:limit]:
                    val_eth = int(tx.get("value", 0)) / 10**18
                    result.append({
                        "txid": tx.get("hash","")[:16] + "...",
                        "from": tx.get("from",""),
                        "to": tx.get("to",""),
                        "value_eth": round(val_eth, 6),
                        "block": tx.get("blockNumber","")
                    })
                    print(f"[+] TX: {val_eth:.4f} ETH block={tx.get('blockNumber')}")
                return result
        except Exception as e:
            print(f"[-] TX error: {e}")
        return []

    def trace(self):
        print(f"[*] Tracing ETH address: {self.address}")
        balance = self.get_balance()
        txs = self.get_transactions()
        return {
            "chain": "ETH",
            "address": self.address,
            "balance_eth": balance,
            "transactions": txs
        }
