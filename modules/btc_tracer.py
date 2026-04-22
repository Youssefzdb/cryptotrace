#!/usr/bin/env python3
"""Bitcoin Transaction Tracer using public blockchain APIs"""
import requests

class BTCTracer:
    BASE_URL = "https://blockchain.info"
    MEMPOOL_URL = "https://mempool.space/api"

    def trace_address(self, address):
        print(f"[*] Tracing BTC address: {address}")
        result = {"address": address, "coin": "BTC"}
        try:
            r = requests.get(f"{self.MEMPOOL_URL}/address/{address}", timeout=10)
            if r.status_code == 200:
                data = r.json()
                stats = data.get("chain_stats", {})
                result.update({
                    "funded_txo_count": stats.get("funded_txo_count", 0),
                    "spent_txo_count": stats.get("spent_txo_count", 0),
                    "tx_count": stats.get("tx_count", 0),
                    "total_received_btc": stats.get("funded_txo_sum", 0) / 1e8,
                    "total_sent_btc": stats.get("spent_txo_sum", 0) / 1e8,
                    "balance_btc": (stats.get("funded_txo_sum", 0) - stats.get("spent_txo_sum", 0)) / 1e8
                })
                print(f"[+] BTC Address: {result['tx_count']} txs | Balance: {result['balance_btc']:.8f} BTC")
        except Exception as e:
            result["error"] = str(e)
        return result

    def trace_tx(self, txid):
        print(f"[*] Tracing BTC tx: {txid}")
        result = {"txid": txid, "coin": "BTC"}
        try:
            r = requests.get(f"{self.MEMPOOL_URL}/tx/{txid}", timeout=10)
            if r.status_code == 200:
                data = r.json()
                inputs = [{"prev_txid": inp.get("txid",""), "value_btc": inp.get("prevout",{}).get("value",0)/1e8}
                          for inp in data.get("vin", [])[:5]]
                outputs = [{"address": out.get("scriptpubkey_address","unknown"), "value_btc": out.get("value",0)/1e8}
                           for out in data.get("vout", [])[:10]]
                result.update({
                    "confirmed": data.get("status", {}).get("confirmed", False),
                    "block_height": data.get("status", {}).get("block_height"),
                    "fee_sat": data.get("fee", 0),
                    "inputs": inputs,
                    "outputs": outputs
                })
                print(f"[+] TX: {len(inputs)} inputs | {len(outputs)} outputs | fee={result['fee_sat']} sat")
        except Exception as e:
            result["error"] = str(e)
        return result
