#!/usr/bin/env python3
from datetime import datetime
import json

class CryptoTraceReport:
    def __init__(self, target, coin, results):
        self.target = target
        self.coin = coin
        self.results = results

    def save(self, filename):
        addr_data = self.results.get("address", {})
        tx_data = self.results.get("transaction", {})
        risk_data = self.results.get("risk", {})

        risk_color = {"CRITICAL": "#ef4444", "HIGH": "#f97316",
                      "MEDIUM": "#facc15", "LOW": "#22c55e"}.get(risk_data.get("risk_level","LOW"), "#888")

        addr_rows = "".join(
            f"<tr><td>{k}</td><td>{v}</td></tr>"
            for k,v in addr_data.items() if k not in ["inputs","outputs","error"]
        )

        outputs_html = ""
        for out in tx_data.get("outputs", []):
            outputs_html += f"<tr><td>{out.get('address','')}</td><td>{out.get('value_btc','')}</td></tr>"

        flags_html = "".join(f"<li>{f}</li>" for f in risk_data.get("flags", []))

        html = f"""<!DOCTYPE html><html><head><title>CryptoTrace Report</title>
<style>
body{{font-family:Arial;background:#0f0a1e;color:#e2e0f0;padding:20px}}
h1{{color:#a78bfa}} h2{{color:#c4b5fd}}
.card{{background:#1e1b2e;border-radius:8px;padding:15px;margin:10px 0;border-left:4px solid #a78bfa}}
table{{width:100%;border-collapse:collapse}} td,th{{padding:7px;border:1px solid #2d2b45}}
th{{background:#16132e}}
.risk{{font-size:1.5em;font-weight:bold;color:{risk_color}}}
</style></head><body>
<h1>🔍 CryptoTrace Report</h1>
<p>Target: <code>{self.target}</code> | Coin: {self.coin.upper()} | {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

<div class="card">
  <h2>Risk Assessment</h2>
  <p class="risk">{risk_data.get('risk_level','N/A')}</p>
  <ul>{flags_html}</ul>
</div>

<div class="card">
  <h2>Address Intelligence</h2>
  <table>{addr_rows}</table>
</div>

{f'<div class="card"><h2>Transaction Outputs</h2><table><tr><th>Address</th><th>BTC</th></tr>{outputs_html}</table></div>' if outputs_html else ''}
</body></html>"""

        with open(filename, "w") as f:
            f.write(html)
        print(f"[+] Report saved: {filename}")
