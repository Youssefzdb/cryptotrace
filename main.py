#!/usr/bin/env python3
"""
cryptotrace - Blockchain Transaction Tracing & Investigation Tool
Traces crypto transactions for forensic and compliance purposes
"""
import argparse
from modules.btc_tracer import BTCTracer
from modules.eth_tracer import ETHTracer
from modules.wallet_analyzer import WalletAnalyzer
from modules.report import CryptoReport

def main():
    parser = argparse.ArgumentParser(description="cryptotrace - Blockchain Investigator")
    parser.add_argument("--address", required=True, help="Wallet address to trace")
    parser.add_argument("--chain", choices=["btc","eth","auto"], default="auto")
    parser.add_argument("--output", default="cryptotrace_report.html")
    args = parser.parse_args()

    print(f"[*] Tracing address: {args.address}")
    results = {}

    # Auto-detect chain
    chain = args.chain
    if chain == "auto":
        chain = "eth" if args.address.startswith("0x") else "btc"

    if chain == "btc":
        tracer = BTCTracer(args.address)
        results["transactions"] = tracer.trace()
    elif chain == "eth":
        tracer = ETHTracer(args.address)
        results["transactions"] = tracer.trace()

    analyzer = WalletAnalyzer(args.address, results.get("transactions", []))
    results["analysis"] = analyzer.analyze()

    report = CryptoReport(args.address, chain, results)
    report.save(args.output)
    print(f"[+] Report: {args.output}")

if __name__ == "__main__":
    main()
