# Rapor — Görev 1, Türkçe metin araçları

## Yapılan
- `tr_metin.py`: `buyuk`, `kucuk`, `slug`, `sayi_yaziya`. Yalnız standart kütüphane.
- `test_tr_metin.py`: 36 pytest testi (EMIR örnekleri, sınırlar, hata türleri).

## Test sonucu
`python3 -m pytest -q` → **36 geçti, 0 hata.**

## Seçimler (belirsiz yerler)
- `buyuk`/`kucuk`: önce `i/ı` ve `İ/I` elle eşlenir, kalanı Python `upper()/lower()` yapar.
  Böylece `İ.lower()`'ın ürettiği birleşik nokta (`i̇`) oluşmaz. `ß` gibi harfler Python'un
  normal davranışını izler (`ß` → `SS`).
- `slug`: `ç ğ ı ö ş ü` dışındaki ASCII olmayan harfler (ör. `é`) ayırıcı sayılıp `-` olur;
  EMIR bunları saymadığı için katlama yapılmadı.
- `sayi_yaziya`: `bin` öncesinde yalnız grup değeri tam 1 ise "bir" düşer (`1000` → `bin`,
  `1_001_000` → `bir milyon bin`, `101_000` → `yüz bir bin`). `bool` ve `int` alt sınıfı
  olmayan her şey `TypeError`; `int` alt sınıfları (bool hariç) kabul edilir.
  Tür denetimi aralık denetiminden önce yapılır.

## Emin olmadığım yer
Yok; bilinen belirsizlik yukarıdaki seçimlerle sınırlı.
