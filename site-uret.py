#!/usr/bin/env python3
"""_puanlar.json + _sureler.tsv → index.html (GitHub Pages ana sayfası)."""
import html
import json
from pathlib import Path

KOK = Path(__file__).resolve().parent
P = json.loads((KOK / "_puanlar.json").read_text())

AD = {"sonnet-5.5": ("Claude Sonnet 5.5", "Anthropic", "Claude Code CLI"),
      "opus-4.6": ("Claude Opus 4.6", "Anthropic", "Antigravity CLI"),
      "sonnet-4.6": ("Claude Sonnet 4.6", "Anthropic", "Antigravity CLI"),
      "gemini-3.8-flash": ("Gemini 3.8 Flash", "Google", "Antigravity CLI"),
      "gemini-3.1-pro": ("Gemini 3.1 Pro", "Google", "Antigravity CLI"),
      "space-bunny": ("Space Bunny", "gizli (OpenRouter stealth)", "omp CLI")}
GOREV = ["1-turkce-metin", "2-mayin-tarlasi", "3-hata-avi"]


def oran(x):
    return (0, 0) if not x else tuple(x)


def satir(m, s):
    g1, g2 = oran(s["1"]["gizli"]), s["2"].get("puan") or "0/16"
    g2 = tuple(int(x) for x in g2.split("/"))
    g3 = oran(s["3"]["gizli"])
    sure = [v[0] if v else None for v in (s["sure"].get(g) for g in GOREV)]
    toplam = sum(x for x in sure if x) if all(sure) else None
    puan = g1[0] + g2[0] + g3[0]
    return {"m": m, "g1": g1, "g2": g2, "g3": g3, "puan": puan, "sure": sure, "toplam": toplam,
            "kendi": oran(s["1"]["kendi_testi"])[1], "dokunmadi": s["3"]["test_dosyasi_ayni"]}


S = [satir(m, s) for m, s in P.items()]
SURUYOR = [AD[r["m"]][0] for r in S if r["toplam"] is None]   # üç görevi bitmemiş modeller
S = [r for r in S if r["toplam"] is not None]
S.sort(key=lambda r: (-r["puan"], r["toplam"] or 10**9))
MAKS = 43 + 16 + 11
EN_UZUN = max((r["toplam"] or 0) for r in S) or 1


def dk(sn):
    return "—" if sn is None else (f"{sn} sn" if sn < 60 else f"{sn // 60} dk {sn % 60:02d} sn")


def hucre(x, maks):
    tam = x[0] == maks
    return f'<td class="{"tam" if tam else "eksik"}">{x[0]}/{maks}</td>'


satirlar = []
for r in S:
    ad, sirket, arac = AD[r["m"]]
    bar = int(100 * (r["toplam"] or 0) / EN_UZUN)
    satirlar.append(f"""<tr>
<th scope="row"><span class="ad">{ad}</span><span class="alt">{sirket} · {arac}</span></th>
{hucre(r['g1'], 43)}{hucre(r['g2'], 16)}{hucre(r['g3'], 11)}
<td class="puan">{r['puan']}/{MAKS}</td>
<td class="sure"><div class="bar"><i style="width:{bar}%"></i></div>{dk(r['toplam'])}</td>
<td>{r['kendi']}</td><td>{'✓' if r['dokunmadi'] else '✗ değiştirdi'}</td></tr>""")

kartlar = []
for r in S:
    ad = AD[r["m"]][0]
    img = f"_ekranlar/{r['m']}-kazandi.png"
    gorsel = f'<img src="{img}" alt="{html.escape(ad)} mayın tarlası, kazanılmış oyun" loading="lazy">' \
        if (KOK / img).exists() else '<div class="yok">ekran görüntüsü yok</div>'
    kartlar.append(f"""<article class="kart">{gorsel}
<div class="kart-alt"><b>{ad}</b><span>{r['g2'][0]}/16 · {dk(r['sure'][1])}</span></div>
<div class="linkler"><a href="{r['m']}/2-mayin-tarlasi/index.html">Oyna ▸</a>
<a href="https://github.com/MrMerkus/model-testleri/tree/main/{r['m']}">Kod</a></div></article>""")

sayfa = f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Model Testleri — {len(S)} yapay zekâ, 3 görev</title>
<meta name="description" content="Claude Sonnet 5.5, Opus 4.6, Sonnet 4.6, Gemini 3.8 Flash, ve Gemini 3.1 Pro aynı üç kodlama görevinde; gizli testlerle puanlandı.">
<style>
:root{{--bg:#0f1117;--kart:#171a23;--cizgi:#262b38;--yazi:#e6e8ee;--soluk:#8b92a5;--vurgu:#d97757;--iyi:#4fb477;--kotu:#e5484d}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--yazi);font:16px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}}
main{{max-width:1080px;margin:auto;padding:48px 20px 80px}}
h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.1;margin:0 0 12px;letter-spacing:-.02em}}
h1 em{{font-style:normal;color:var(--vurgu)}}h2{{margin:56px 0 16px;font-size:1.5rem}}
.giris{{color:var(--soluk);font-size:1.15rem;max-width:720px}}
.ozet{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-top:32px}}
.ozet div{{background:var(--kart);border:1px solid var(--cizgi);border-radius:12px;padding:16px}}
.ozet b{{display:block;font-size:1.6rem}}.ozet span{{color:var(--soluk);font-size:.9rem}}
.tablo{{overflow-x:auto;border:1px solid var(--cizgi);border-radius:12px}}
table{{border-collapse:collapse;width:100%;min-width:760px;font-variant-numeric:tabular-nums}}
th,td{{padding:12px 14px;text-align:left;border-bottom:1px solid var(--cizgi)}}
thead th{{font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:var(--soluk);background:var(--kart)}}
tbody tr:last-child>*{{border-bottom:0}}.ad{{display:block;font-weight:600}}.alt{{font-size:.8rem;color:var(--soluk);font-weight:400}}
td.tam{{color:var(--iyi)}}td.eksik{{color:var(--kotu)}}td.puan{{font-weight:700}}
.sure{{min-width:160px}}.bar{{height:6px;background:var(--cizgi);border-radius:3px;margin-bottom:4px}}.bar i{{display:block;height:100%;background:var(--vurgu);border-radius:3px}}
.kartlar{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.kart{{background:var(--kart);border:1px solid var(--cizgi);border-radius:12px;overflow:hidden}}
.kart img{{width:100%;aspect-ratio:1;object-fit:cover;object-position:top;display:block;background:#000}}
.yok{{aspect-ratio:1;display:grid;place-items:center;color:var(--soluk)}}
.kart-alt{{display:flex;justify-content:space-between;padding:12px 14px 4px}}.kart-alt span{{color:var(--soluk);font-size:.9rem}}
.linkler{{display:flex;gap:16px;padding:0 14px 14px}}a{{color:var(--vurgu)}}
.gorevler{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}}
.gorevler article{{background:var(--kart);border:1px solid var(--cizgi);border-radius:12px;padding:18px}}
.gorevler h3{{margin:0 0 8px}}.gorevler p{{margin:0;color:var(--soluk)}}
.not{{border-left:3px solid var(--vurgu);padding:4px 16px;color:var(--soluk)}}
footer{{margin-top:64px;color:var(--soluk);font-size:.9rem}}
</style></head><body><main>
<h1>{len(S)} yapay zekâ, 3 görev, <em>gizli testler</em></h1>
<p class="giris">Aynı emirler, aynı klasör yapısı, insan müdahalesi yok. Her model görevini kendi
komut satırı ajanında baştan sona yaptı; puanı modelin kendi raporu değil, modelin görmediği
testler verdi. 28 Eylül 2026 — Claude Sonnet 5.5'in çıktığı gün.</p>
<div class="ozet">
<div><b>{sum(1 for r in S if r['puan'] == MAKS)}/{len(S)}</b><span>model tam puan aldı</span></div>
<div><b>{AD[S[0]['m']][0]}</b><span>en hızlı tam puan · {dk(S[0]['toplam'])}</span></div>
<div><b>{MAKS}</b><span>gizli kontrol / model</span></div>
<div><b>{sum(1 for r in S if not r['dokunmadi'])}</b><span>test dosyasını değiştiren model</span></div>
</div>

<h2>Sonuçlar</h2>
<div class="tablo"><table>
<thead><tr><th>Model</th><th>G1 Türkçe metin</th><th>G2 Mayın tarlası</th><th>G3 Hata avı</th><th>Toplam</th><th>Süre (3 görev)</th><th>Kendi testi</th><th>G3 test dosyası</th></tr></thead>
<tbody>{''.join(satirlar)}</tbody></table></div>
{f'<p class="not">Henüz sürüyor: {", ".join(SURUYOR)}. Bitince tabloya eklenecek.</p>' if SURUYOR else ''}
<p class="not">Doğrulukta ayrışma olmadı: tam puan alan her model görev 3'teki beş hatayı da aynı
10 satırlık düzeltmeyle buldu. Bu tur için fark hızda ve modelin kendine yazdığı test
sayısında. Daha zor ikinci tur planlanıyor.</p>

<h2>Mayın tarlaları — kendin oyna</h2>
<div class="kartlar">{''.join(kartlar)}</div>

<h2>Görevler</h2>
<div class="gorevler">
<article><h3>1 · Türkçe metin araçları</h3><p>İ/ı kuralıyla büyük-küçük harf, URL kısa adı ve
sayıyı yazıya çevirme ("bin" ama "bir milyon"). 43 gizli test.</p>
<a href="_gorevler/1-turkce-metin/EMIR.md">Emir</a> · <a href="hakem/1/test_gizli.py">Gizli testler</a></article>
<article><h3>2 · Mayın tarlası</h3><p>Tek HTML dosyası. İlk tık güvenli, zincirleme açılma,
bayrak, kazan/kaybet. Gerçek tarayıcıda 16 otomatik kontrol.</p>
<a href="_gorevler/2-mayin-tarlasi/EMIR.md">Emir</a> · <a href="hakem/2/mayin_hakem.js">Tarayıcı hakemi</a></article>
<article><h3>3 · Hata avı</h3><p>Beş gizli hatalı bir ödünç sistemi. Test dosyasına dokunmadan
düzelt; görünmeyen 11 testle kökten mi düzeltildiği sınandı.</p>
<a href="_gorevler/3-hata-avi/EMIR.md">Emir</a> · <a href="hakem/3/test_gizli.py">Gizli testler</a></article>
</div>

<h2>Yöntem</h2>
<p>Her model yalnız kendi klasöründe, görev başına 25 dakika sınırla çalıştı (<a href="calistir.sh">calistir.sh</a>).
Gizli testler çalışma sırasında depo dışında tutuldu. Puanlama <a href="hakem/puanla.py">hakem/puanla.py</a>
ile yapıldı; ham sonuç <a href="_puanlar.json">_puanlar.json</a>. Süreler duvar saati; modellerin
çalıştığı araçlar (Claude Code, Antigravity, omp) farklı olduğundan hız, model + araç ikilisinin hızıdır.</p>

<footer>Model Testleri · <a href="https://github.com/MrMerkus/model-testleri">GitHub</a></footer>
</main></body></html>
"""
(KOK / "index.html").write_text(sayfa)
print("index.html yazıldı:", len(S), "model")
