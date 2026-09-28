# Model Testleri — 6 yapay zekâ, 3 görev, gizli testler

**Site:** https://mrmerkus.github.io/model-testleri/ (sonuç tablosu, oynanabilir mayın tarlaları)

28 Eylül 2026'da, Claude Sonnet 5.5'in çıktığı gün, altı model aynı üç görevi kendi komut
satırı ajanında baştan sona yaptı. Puanı modelin kendi raporu değil, çalışma sırasında
modelin göremediği testler verdi.

| Model | Ajan |
|---|---|
| Claude Sonnet 5.5 | Claude Code |
| Claude Opus 4.6, Claude Sonnet 4.6 | Antigravity |
| Gemini 3.8 Flash, Gemini 3.1 Pro | Antigravity |
| Space Bunny (OpenRouter stealth) | omp |

## Görevler

1. **Türkçe metin araçları** — İ/ı kuralı, URL kısa adı, sayıyı yazıya çevirme. 43 gizli test.
2. **Mayın tarlası** — tek HTML dosyası; gerçek tarayıcıda 16 otomatik kontrol.
3. **Hata avı** — 5 gizli hatalı ödünç sistemi; test dosyasına dokunmadan düzelt, 11 gizli test.

Emirler `_gorevler/`, hakemler `hakem/`, her modelin çıktısı kendi klasöründe
(`<model>/<görev>/`, ajanın konsol çıktısı `_calisma.log`).

## Yeniden üretmek

```bash
python3 -m venv .venv && .venv/bin/pip install pytest
./calistir.sh <model>            # modeli üç görevde çalıştırır
python3 hakem/puanla.py .        # _puanlar.json + Markdown tablo
python3 site-uret.py             # index.html
```

`calistir.sh` yerel kurulumu varsayar (agy, omp, claude CLI'ları; Space Bunny `bwrap`
içinde yalıtılır). Süreler duvar saatidir ve model + ajan ikilisinin hızını ölçer.
