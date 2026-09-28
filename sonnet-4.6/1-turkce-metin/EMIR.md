# Görev 1 — Türkçe metin araçları

Bu klasörde `tr_metin.py` adlı bir Python 3 modülü yaz. Yalnız standart kütüphane kullan.
Aşağıdaki dört fonksiyon **tam bu adlarla** olmalı:

## `buyuk(metin: str) -> str` ve `kucuk(metin: str) -> str`
Türkçe kurallarıyla büyük/küçük harfe çevirir: `i ↔ İ`, `ı ↔ I`. Diğer harfler Python'un
normal davranışıyla çevrilir. Örnek: `buyuk("istanbul ılık") == "İSTANBUL ILIK"`,
`kucuk("IĞDIR İZMİR") == "ığdır izmir"`.

## `slug(metin: str) -> str`
URL'de kullanılabilir kısa ad üretir:
1. Metni Türkçe kurallarla küçült.
2. `ç ğ ı ö ş ü` harflerini `c g i o s u` yap.
3. `a-z` ve `0-9` dışındaki her karakter dizisini tek bir `-` yap.
4. Baştaki ve sondaki `-` karakterlerini sil.
Örnek: `slug("  Çok Güzel Şarkı: İyi ki Doğdun!  ") == "cok-guzel-sarki-iyi-ki-dogdun"`.
Sonuçta harf ya da rakam kalmıyorsa boş dize döner.

## `sayi_yaziya(n: int) -> str`
Tam sayıyı Türkçe yazıya çevirir. Kurallar:
- `0` → `"sıfır"`. Negatif sayılar `"eksi "` ile başlar.
- Kelimeler tek boşlukla ayrılır, hepsi küçük harf.
- `100` → `"yüz"` (bir yüz değil), `1000` → `"bin"` (bir bin değil), ama `1_000_000` →
  `"bir milyon"`.
- Basamak adları: bin, milyon, milyar, trilyon. Desteklenen aralık mutlak değerce
  `10**15`'ten küçük sayılardır; dışındaysa `ValueError` fırlat.
- `int` olmayan girdi (`bool` dahil, `float` dahil) için `TypeError` fırlat.
Örnek: `sayi_yaziya(1_250_003) == "bir milyon iki yüz elli bin üç"`,
`sayi_yaziya(-1001) == "eksi bin bir"`.

## Ayrıca
- Kendi testlerini `test_tr_metin.py` dosyasına pytest ile yaz ve çalıştır.
- İş bitince bu klasöre kısa bir `RAPOR.md` yaz: ne yaptın, testler geçti mi, emin olmadığın
  yer var mı.
- Yalnız bu klasörde çalış. İnternete çıkma, başka klasörlere bakma.
