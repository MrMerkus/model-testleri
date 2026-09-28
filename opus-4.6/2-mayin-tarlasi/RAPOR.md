# RAPOR — Mayın Tarlası

## Ne yaptım

Tek bir `index.html` dosyasında (dış kaynak yok: CDN, font, resim yok) tam çalışan bir
mayın tarlası oyunu oluşturdum.

### Uygulanan kurallar
- **9×9 ızgara, 10 mayın.**
- **İlk tık güvenliği:** İlk tıklanan hücre ve 8 komşusu asla mayın içermez; mayınlar
  ilk tıklamadan sonra Fisher–Yates karıştırmasıyla yerleştirilir.
- **Sayı gösterimi:** Açılan hücre komşu mayın sayısını gösterir. 0 ise metin boş bırakılır.
- **Zincirleme açma:** 0 sayılı hücre açılınca komşuları özyinelemeli olarak açılır.
- **Sağ tık bayrak:** Sağ tık ile bayrak konur/kaldırılır. Bayraklı hücre sol tıkla açılamaz.
- **Kaybetme:** Mayına basınca `id="durum"` elementine `Kaybettin` yazılır, tüm mayınlar
  gösterilir. Artık tıklamalar tahtayı değiştirmez.
- **Kazanma:** Mayınsız tüm hücreler açılınca `Kazandın` yazılır. Artık tıklamalar
  tahtayı değiştirmez.
- **Yeni Oyun:** `id="yeni"` butonu her şeyi sıfırlar; mayınlar yeni ilk tıklamada yeniden
  yerleşir.

### Test edilebilirlik sözleşmesi (harfiyen uyuldu)
| Kural | Uygulama |
|-------|----------|
| `data-r` / `data-c` (0–8) | Her hücrede mevcut |
| Açılmış → `acik` sınıfı | ✅ |
| Bayraklı → `bayrak` sınıfı | ✅ |
| Sayılı hücre metni = rakam | ✅ |
| 0 hücre metni = boş | ✅ |
| `id="durum"` — `Kazandın` / `Kaybettin` | ✅ |
| `id="yeni"` buton | ✅ |
| `window.mayinKonumlari()` → `null` veya `[[r,c], ...]` | ✅ |

## Nasıl denedim

`pytest` + `playwright` ile 18 otomatik test yazdım (`test_mayin.py`). Testler:

| Sınıf | Ne test ediyor | Sonuç |
|-------|---------------|-------|
| `TestIzgara` | 81 hücre var mı, `data-r`/`data-c` doğru mu | ✅ 2/2 |
| `TestIlkTiklama` | Başta `null`, sonra 10 mayın, güvenli bölge | ✅ 3/3 |
| `TestAcma` | `acik` sınıfı, boş metin, zincirleme açma | ✅ 3/3 |
| `TestBayrak` | Bayrak koy/kaldır, bayraklı hücre açılmaz | ✅ 3/3 |
| `TestKaybet` | Mayına basınca `Kaybettin`, sonra tıklama işlemez | ✅ 2/2 |
| `TestKazan` | Tüm güvenli hücreler açılınca `Kazandın` | ✅ 1/1 |
| `TestYeniOyun` | Sıfırlama, mayın konumları tekrar `null` | ✅ 2/2 |
| `TestMayinKonumlariAPI` | Fonksiyon var, dönüş formatı doğru | ✅ 2/2 |

**Toplam: 18/18 geçti** (5 saniyede).

## Tasarım kararları
- **Renk paleti:** Koyu lacivert–mor arkaplan, hücrelerin açık gri açılması. Sayı renkeri
  klasik mayın tarlası renk kodlamasına yakın.
- **Emoji:** Mayınlar 💣, bayraklar 🚩 olarak gösteriliyor.
- **Süre sayacı ve bayrak sayacı** eklendi (görsel zenginlik için).
- **Hover efekti:** Kapalı hücrelerde hafif büyüme ve renk değişimi.

## Emin olmadığım yer
- Yok. Sözleşmedeki tüm maddeler harfi harfine uygulandı ve 18 testle doğrulandı.
