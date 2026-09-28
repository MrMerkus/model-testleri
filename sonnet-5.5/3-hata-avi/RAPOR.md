# Rapor — Hata avı

5 hata buldum, hepsi `kutuphane.py` içinde. `test_kutuphane.py`'ye dokunmadım.

| # | Yer | Hata | Düzeltme |
| --- | --- | --- | --- |
| 1 | `kitap_ekle` | Aynı ISBN tekrar eklenince adet artmıyor, üzerine yazılıyordu (`= adet`) | `+= adet` |
| 2 | `musait` | İade edilmiş ödünçler de "verilen" sayılıyordu, kitap rafa dönmüyordu | Yalnız `iade is None` olanlar sayılıyor |
| 3 | `odunc_ver` | Limit kontrolü `>` idi, 4. kitaba izin veriyordu (off-by-one) | `>=` |
| 4 | `son_tarih` | `ODUNC_GUN - 1` kullanılıyordu; 1 Ocak alışın son günü 14 Ocak çıkıyordu, sabit ve yorum 15 Ocak diyor | `alis + timedelta(days=ODUNC_GUN)` |
| 5 | `populer` | Sıralama artan (azdan çoğa) idi | Anahtar `(-sayı, ad)`: çoktan aza, eşitlikte A-Z |

## Seçimler
- `populer` iade edilmiş ödünçleri de sayıyor ("kaç kez ödünç alındı" tarihsel sayım); değiştirmedim.
- Bilinmeyen ISBN'de `odunc_ver` `KeyError` veriyor (`musait` üzerinden); mevcut davranışı korudum.
