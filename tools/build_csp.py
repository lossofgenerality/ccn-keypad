#!/usr/bin/env python3
"""Build index.html from src/keypad.html, adding a hash-based Content-Security-Policy.

Run this after every change to the <script> or <style> in src/keypad.html:
    python3 tools/build_csp.py
"""
import base64, hashlib, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "src" / "keypad.html", ROOT / "index.html"
API_HOST = "https://www.wolframcloud.com"

def sha(text):
    return "'sha256-" + base64.b64encode(hashlib.sha256(text.encode("utf-8")).digest()).decode() + "'"

html = SRC.read_text(encoding="utf-8")
scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
styles = re.findall(r"<style>(.*?)</style>", html, re.S)
csp = ("default-src 'none'; "
       f"script-src {' '.join(map(sha, scripts))}; "
       f"style-src {' '.join(map(sha, styles))} https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com; "
       f"connect-src {API_HOST}; "
       "img-src data:; base-uri 'none'; form-action 'none'; object-src 'none'")
meta = f'<meta http-equiv="Content-Security-Policy" content="{csp}">\n'
if "Content-Security-Policy" in html:
    raise SystemExit("src/keypad.html already has a CSP meta tag; remove it first.")
OUT.write_text(html.replace('<meta name="referrer"', meta + '<meta name="referrer"', 1), encoding="utf-8")
print(f"Wrote {OUT.name}\n{csp}")
