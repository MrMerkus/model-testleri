#!/usr/bin/env python3
"""Yayın öncesi: ajan günlüklerindeki mutlak yerel yolları göreli yola çevirir."""
import re, sys
from pathlib import Path
from urllib.parse import quote

KOK = Path(__file__).resolve().parent
onekler = [str(KOK) + "/", quote(str(KOK)) + "/", str(Path.home() / "ofis/model-testleri") + "/"]
kalan = 0
for f in KOK.glob("*/*/_calisma.log"):
    t = f.read_text(errors="replace")
    for o in onekler:
        t = t.replace("file://" + o, "").replace(o, "")
    t = t.replace(str(Path.home()), "~")
    f.write_text(t)
    kalan += len(re.findall(r"/home/|baran", t, re.I))
print("temizlendi; kalan iz:", kalan)
sys.exit(1 if kalan else 0)
