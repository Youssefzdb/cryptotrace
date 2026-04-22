#!/usr/bin/env python3
"""Ethereum Transaction Tracer using public APIs"""
import requests

class ETHTracer:
    BASE_URL = "https://api.etherscan.io/api"

    def trace_address(self, address):
        print(f"[*] Tracing ETH address: {address}")
        result = {"address": address, "coin": "ETH"}
        try:
            # Balance check via public API (no API key needed for basic)
            r = requests.get(
                f"https://eth.llamarpc.com",
                json={"jsonrpc": "2.0", "method": "eth_getBalance",
                      "params": [address, "latest"], "id": 1},
                timeout=10
            )
            if r.status_code == 200:
                data = r.json()
                balance_hex = data.get("result", "0x0")
                balance_eth = int(balance_hex, 16) / 1e18
                result["balance_eth"] = round(balance_eth, 6)
                print(f"[+] ETH Balance: {balance_eth:.6f} ETH")

            # Transaction count
            r2 = requests.get(
                "https://eth.llamarpc.com",
                json={"jsonrpc": "2.0", "method": "eth_getTransactionCount",
                      "params": [address, "latest"], "id": 1},
                timeout=10
            )
            if r2.status_code == 200:
                count_hex = r2.json().get("result", "0x0")
                result["tx_count"] = int(count_hex, 16)
                print(f"[+] ETH TX Count: {result['tx_count']}")

        except Exception as e:
            result["error"] = str(e)
        return result
