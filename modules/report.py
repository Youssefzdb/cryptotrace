#!/usr/bin/env python3
from datetime import datetime

class CryptoReport:
    def __init__(self, address, chain, results):
        self.address = address
        self.chain = chain
        self.results = results

    def save(self, filename):
        txs = self.results.get("transactions", {})
        analysis = self.results.get("analysis", {})
        tx_list = txs.get("transactions", []) if isinstance(txs, dict) else []

        tx_rows = "".join(
            f"<tr><td>{t.get('txid','')}</td><td>{t.get('value_eth', t.get('value_out',''))}</td><td>{t.get('block','')}</td></tr>"
            for t in tx_list[:20]
        )
        findings = "".join(f"<li class='{f[\"severity\"].lower()}'>{f['indicator']}</li>" for f in analysis.get("findings",[]))

        risk = analysis.get("risk_level","UNKNOWN")
        rcolor = {"LOW":"#22c55e","MEDIUM":"#f59e0b","HIGH":"#ef4444"}.get(risk,"#888")

        html = f"""<!DOCTYPE html><html><head><title>CryptoTrace Report</title>
<style>body{{font-family:Arial;background:#0f0f1a;color:#c8c8ff;padding:20px}}
h1{{color:#a78bfa}}h2{{color:#c4b5fd}}
.card{{background:#1e1b33;border-radius:8px;padding:15px;margin:10px 0}}
table{{width:100%;border-collapse:collapse}}td,th{{padding:7px;border:1px solid #2d2b4e}}
th{{background:#2d2b4e}}.low{{color:#22c55e}}.medium{{color:#f59e0b}}.high{{color:#ef4444}}
</style></head>
<body>
<h1>CryptoTrace Investigation Report</h1>
<p>Address: <code>{self.address}</code> | Chain: <b>{self.chain.upper()}</b> | {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<div class="card">
  <h2>Wallet Info</h2>
  <p>Balance: {txs.get('balance_eth', txs.get('balance','N/A'))} {self.chain.upper()} | TX Count: {txs.get('tx_count', len(tx_list))}</p>
  <p>Risk Level: <span style="color:{rcolor};font-weight:bold">{risk}</span> ({analysis.get('risk_score',0)}/100)</p>
</div>
<div class="card"><h2>Risk Indicators</h2><ul>{findings if findings else '<li>No suspicious indicators found</li>'}</ul></div>
<div class="card"><h2>Recent Transactions</h2>
<table><tr><th>TxID</th><th>Value</th><th>Block</th></tr>{tx_rows if tx_rows else '<tr><td colspan=3>No transactions</td></tr>'}</table>
</div></body></html>"""
        with open(filename, "w") as f:
            f.write(html)
        print(f"[+] Saved: {filename}")
