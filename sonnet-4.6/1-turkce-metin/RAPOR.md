# RAPOR

## Ne Yaptım

### 1. `tr_metin.py` modülü

EMIR.md'de istenen dört fonksiyonu standart kütüphane kullanarak yazdım:

| Fonksiyon | Açıklama |
|---|---|
| `buyuk(metin)` | `str.maketrans` ile önce `i→İ`, `ı→I` dönüşümü yapıp ardından Python'un `.upper()` metodunu çağırır |
| `kucuk(metin)` | `str.maketrans` ile önce `İ→i`, `I→ı` dönüşümü yapıp ardından `.lower()` çağırır |
| `slug(metin)` | `kucuk()` → Türkçe/aksan harflerini ASCII'ye çevir → `[^a-z0-9]+` regex ile `-` yap → baş/son `-` sil |
| `sayi_yaziya(n)` | `bool`/`float` için `TypeError`, sınır dışı için `ValueError`; 0-999 arası yardımcı fonksiyon (`_uc_basamak`) + trilyon/milyar/milyon/bin basamakları |

#### Özel durumlar ve tasarım kararları

- **`buyuk` / `kucuk`**: Python'un `.upper()` / `.lower()` çağrıları `İ`→`I` ve `I`→`İ` dönüşümlerini yanlış yapar; `str.maketrans` ile bu harfler önceden takas edilerek sorun aşıldı.
- **`slug`**: `İ` harfi önce `kucuk()` ile `i`'ye dönüşür, ardından ASCII dönüşüm tablosu uygulanır; bu sıralama doğru sonucu verir.
- **`sayi_yaziya`**: `1000 → "bin"` (bir bin değil), `100 → "yüz"` kuralı `_uc_basamak` içinde yüzler basamağı için, bin basamağı için ise ana döngüde özel olarak ele alındı. `1_000_000 → "bir milyon"` kuralı genel yolu izler (1 milyon ifadesi için `_uc_basamak(1)` → "bir" döner, ortak bir özel durum değil).

### 2. `test_tr_metin.py` dosyası

Toplam **45 test** yazıldı; 4 sınıfa (class) ayrılarak gruplandı:

- `TestBuyuk` — 7 test
- `TestKucuk` — 6 test
- `TestSlug` — 9 test
- `TestSayiYaziya` — 23 test (sınır, hata türleri, özel kurallar dahil)

### 3. Test Sonuçları

```
45 passed in 0.05s
```

**Tüm 45 test başarıyla geçti.** Herhangi bir hata ya da uyarı oluşmadı.

---

## Emin Olmadığım Yerler

1. **`sayi_yaziya` — büyük negatif sınır**: Görevde "mutlak değerce `10**15`'ten küçük" deniyor; `-(10**15 - 1)` geçerli, `-(10**15)` `ValueError` fırlatıyor. Bunu birebil uyguladım.
2. **`slug` — `İ` harfinin ASCII karşılığı**: Görevde yalnızca `ç ğ ı ö ş ü` listelenmiş; `İ` bu listede yok. Ancak `slug`'ın ilk adımı `kucuk()` olduğundan `İ → i` dönüşümü zaten gerçekleşiyor ve sonuç doğru çıkıyor. Ayrıca büyük Türkçe harfler (`Ç Ğ Ö Ş Ü`) de `str.maketrans` tablosuna eklenerek küçük harfe indirmeden bağımsız da çalışmasını sağladım; bu davranış görevle çelişmiyor.
3. **`sayi_yaziya` — `2_001_000` durumu**: `"iki milyon bin"` olarak döner; `"iki milyon bir bin"` değil, çünkü 1000 katsayısı 1 olduğunda özel kural devreye giriyor. Görevin ruhuna uygun buldum.
