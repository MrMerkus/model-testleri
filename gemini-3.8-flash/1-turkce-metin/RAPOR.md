# Rapor — Görev 1: Türkçe Metin Araçları

## 1. Neler Yapıldı?

`EMIR.md` dosyasındaki gereksinimler doğrultusunda, harici kütüphane kullanılmadan yalnızca Python 3 standart kütüphanesi ile `tr_metin.py` modülü ve testleri içeren `test_tr_metin.py` dosyası geliştirildi.

Modülde istenen 4 fonksiyon eksiksiz biçimde uygulandı:

1. **`buyuk(metin: str) -> str`**:
   - `i ↔ İ` ve `ı ↔ I` dönüşümleri Türkçe kurallarına uygun biçimde eşlendi; diğer karakterler için Python'un yerel `upper()` kuralları korundu.
   - `str` harici tipler için `TypeError` fırlatılacak şekilde tip kontrolü eklendi.

2. **`kucuk(metin: str) -> str`**:
   - `İ ↔ i` ve `I ↔ ı` dönüşümleri sağlandı. (Python standart `str.lower()` fonksiyonunun `'İ'` karakterini `'i\u0307'` ayrık aksanlı karaktere dönüştürme problemi önlendi).
   - `str` harici tipler için `TypeError` fırlatıldı.

3. **`slug(metin: str) -> str`**:
   - Şartnamedeki 4 adım sırasıyla işletildi:
     1. Metin `kucuk()` ile Türkçe kurallarla küçültüldü.
     2. `ç ğ ı ö ş ü` harfleri `c g i o s u` harflerine dönüştürüldü.
     3. `[^a-z0-9]+` düzenli ifadesiyle `a-z` ve `0-9` dışındaki tüm karakter dizileri tek bir `-` yapıldı.
     4. Baştaki ve sondaki `-` karakterleri `strip('-')` ile temizlendi.
   - Harf/rakam kalmayan veya boş girdilerde `""` döndürüldü.

4. **`sayi_yaziya(n: int) -> str`**:
   - `0` için `"sıfır"`, negatif sayılar için `"eksi "` öneki eklendi.
   - `100` için `"yüz"`, `1000` için `"bin"` (asla `"bir yüz"` veya `"bir bin"` değil) kuralları uygulandı.
   - `1_000_000` ve üzeri basamaklarda (milyon, milyar, trilyon) `"bir milyon"`, `"bir milyar"`, `"bir trilyon"` kuralı sağlandı.
   - `|n| >= 10**15` sınırındaki sayılar için `ValueError` fırlatıldı.
   - `bool`, `float` veya `int` olmayan tüm girdiler için `TypeError` fırlatıldı.

## 2. Testler Geçti mi?

Evet. `test_tr_metin.py` dosyasına tüm gereksinimleri, köşe durumları (edge cases), sınır değerleri ve hata fırlatma koşullarını doğrulayan 26 test yazıldı.

`python3 -m pytest -v` komutu çalıştırıldı ve testlerin tamamı başarıyla geçti:
```text
============================== 26 passed in 0.06s ==============================
```

## 3. Emin Olunmayan veya Tercih Yapılan Yerler

Gereksinimler oldukça açık olmakla birlikte aşağıdaki makul tercihler yapılmıştır:
- **`bool` tip denetimi**: Python'da `bool` sınıfı `int` sınıfından türediği için `isinstance(True, int)` ifadesi `True` döner. Şartnamedeki "`bool` dahil" ifadesi gereğince `isinstance(n, bool)` kontrolü eklenerek `bool` değerlerin `TypeError` fırlatması garanti altına alındı.
- **Sınır değer (`10**15`)**: "Desteklenen aralık mutlak değerce `10**15`'ten küçük sayılardır" ifadesi uyarınca `abs(n) >= 10**15` için `ValueError` fırlatıldı; `10**15 - 1` ve `-(10**15 - 1)` sayıları başarıyla yazıya çevrilmektedir.
- **Slug karakter kümesi**: `_` (alt çizgi) gibi semboller şartnamenin 3. maddesi uyarınca (`a-z` ve `0-9` dışı) doğrudan `-` karakterine dönüştürüldü.
