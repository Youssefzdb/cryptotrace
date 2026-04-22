#!/usr/bin/env python3
"""
cryptotrace - Blockchain Transaction Tracing & Analytics Tool
Traces cryptocurrency transactions for forensic investigations
"""
import argparse
from modules.btc_tracer import BTCTracer
from modules.eth_tracer import ETHTracer
from modules.address_analyzer import AddressAnalyzer
from modules.report import CryptoTraceReport

def main():
    parser = argparse.ArgumentParser(description="cryptotrace - Crypto Forensics Tool")
    parser.add_argument("--address", help="Crypto address to trace")
    parser.add_argument("--txid", help="Transaction ID to analyze")
    parser.add_argument("--coin", choices=["btc","eth","auto"], default="auto")
    parser.add_argument("--output", default="cryptotrace_report.html")
    args = parser.parse_args()

    if not args.address and not args.txid:
        print("[-] Provide --address or --txid")
        return

    print(f"[*] CryptoTrace - Blockchain Forensics")
    results = {}

    # Auto-detect coin type
    target = args.address or args.txid
    coin = args.coin
    if coin == "auto":
        if target.startswith("0x") and len(target) == 42:
            coin = "eth"
        elif target.startswith("1") or target.startswith("3") or target.startswith("bc1"):
            coin = "btc"
        else:
            coin = "btc"

    if coin == "btc":
        tracer = BTCTracer()
        if args.address:
            results["address"] = tracer.trace_address(args.address)
        if args.txid:
            results["transaction"] = tracer.trace_tx(args.txid)
    elif coin == "eth":
        tracer = ETHTracer()
        if args.address:
            results["address"] = tracer.trace_address(args.address)

    analyzer = AddressAnalyzer(target, coin)
    results["risk"] = analyzer.assess_risk()

    report = CryptoTraceReport(target, coin, results)
    report.save(args.output)
    print(f"[+] Report: {args.output}")

if __name__ == "__main__":
    main()
