# RAPOR — Görev 1: Türkçe Metin Araçları

## Yapılanlar

### `tr_metin.py`
Dört fonksiyon EMIR.md'deki spesifikasyona uygun olarak yazıldı:

| Fonksiyon | Açıklama |
|-----------|----------|
| `buyuk(metin)` | Türkçe kurallarla büyük harfe çevirir (`i→İ`, `ı→I`). `str.translate` ile özel Türkçe harfler eşlenir, ardından `.upper()` uygulanır. |
| `kucuk(metin)` | Türkçe kurallarla küçük harfe çevirir (`İ→i`, `I→ı`). `str.translate` + `.lower()`. |
| `slug(metin)` | URL dostu kısa ad üretir: Türkçe küçült → Türkçe özel karakterleri ASCII'ye dönüştür → `[^a-z0-9]+` → tek `-` → baş/son `-` sil. |
| `sayi_yaziya(n)` | Tam sayıyı Türkçe yazıya çevirir. `bin` özel durumu (başına "bir" eklenmez), 10^15 sınırı, `bool`/`float` reddi dahil. |

Yalnız standart kütüphane kullanıldı (`re` modülü).

### `test_tr_metin.py`
44 test yazıldı (pytest):
- **buyuk**: 6 test (temel, boş, i/ı ayrımı, rakam/noktalama)
- **kucuk**: 5 test (temel, boş, I/İ ayrımı)
- **slug**: 6 test (EMIR.md örneği, boş sonuç, rakamlar, ardışık özel karakter, Türkçe harfler, büyük I/İ)
- **sayi_yaziya**: 27 test (0, birler, onlar, yüzler, bin, milyon, milyar, trilyon, negatif, sınır değerler, TypeError × 3, ValueError × 2)

## Test Sonucu

```
44 passed in 0.05s
```

Tüm testler geçti. ✅

## Belirsiz Noktalar & Kararlar

1. **`buyuk`/`kucuk` yaklaşımı**: Önce `str.translate` ile Türkçe özel harfleri dönüştürüp sonra Python'un `.upper()` / `.lower()` fonksiyonunu çağırma yöntemi kullanıldı. Bu, spesifikasyondaki "diğer harfler Python'un normal davranışıyla çevrilir" kuralını karşılar.

2. **`slug` ve `ğ` harfi**: `ğ` → `g` dönüşümü tabloya eklendi (URL slug'larında standart uygulama).

3. **`sayi_yaziya` — "bin" özel durumu**: Yalnızca `1 × bin` olduğunda "bin" denir (EMIR.md'deki kural). `1 × milyon` → "bir milyon" şeklinde kalır.

4. **Sınır**: `|n| < 10^15` şeklinde yorumlandı (EMIR.md: "10^15'ten küçük"). `10^15` tam değeri dahil değil, `ValueError` fırlatır.
