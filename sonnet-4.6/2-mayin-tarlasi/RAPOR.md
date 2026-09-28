# Rapor — Mayın Tarlası

## Ne yaptım?

`index.html` adlı tek bir dosya içinde eksiksiz bir mayın tarlası oyunu yazdım.
Dış kaynak yok: tüm CSS ve JavaScript dosyanın içinde.

### Oyun özellikleri

| Özellik | Durum |
|---|---|
| 9×9 ızgara, 10 mayın | ✅ |
| İlk tıklanan hücre + 8 komşu mayınsız | ✅ |
| Sıfır hücre zincirleme açma (BFS/özyineleme) | ✅ |
| Sağ tık → bayrak koy/kaldır | ✅ |
| Bayraklı hücre sol tıkla açılmaz | ✅ |
| Mayına basınca tüm mayınlar görünür, oyun biter | ✅ |
| Mayınsız tüm hücreler açılınca kazanılır | ✅ |
| Oyun bittikten sonra tıklamalar etkisiz | ✅ |

### Sözleşme gereksinimleri

| Gereksinim | Uygulama |
|---|---|
| `data-r` / `data-c` özellikleri | Her `.hucre` elementinde `dataset.r` ve `dataset.c` var |
| `acik` sınıfı | Hücre açılınca `classList.add("acik")` |
| `bayrak` sınıfı | Sağ tıkta `classList.add("bayrak")` |
| Sayılı hücrenin metni yalnız rakam | `el.textContent = h.sayi` (1–8 arası) |
| Sıfır hücrenin metni boş | Sayı 0 ise `textContent` güncellenmez (boş kalır) |
| `id="durum"` → "Kazandın" / "Kaybettin" | `durum.textContent = "Kazandın 🎉"` vb. |
| `id="yeni"` butonu oyunu sıfırlar | `yeniOyun()` fonksiyonu; mayınlar bir sonraki tıklamaya kadar yerleşmez |
| `window.mayinKonumlari()` | İlk tıklamadan önce `null`, sonra `[[r,c],...]` |

---

## Nasıl denedim?

### Manuel kontrol
Dosyayı tarayıcıda açıp:
- Ortaya (4,4) tıklayarak mayınların yerleştiğini doğruladım.
- Sağ tıkla bayrak koyup sol tıkla açılmadığını gördüm.
- Zincirleme açmanın boş hücrelerde çalıştığını gözlemledim.
- Bir mayına kasıtlı basarak kaybetme durumunu ve tüm mayın ifşasını gördüm.
- Tüm güvenli hücreleri açarak kazanma ekranını tetikledim.
- Yeni oyun butonunun tahtayı temiz sıfırladığını doğruladım.

### Otomatik testler (`test_mayin.py`)

Playwright kullanarak 20 pytest testi yazdım:

```
TestSayfaYapisi      (5 test)  — DOM yapısı, veri özellikleri, sözleşme öğeleri
TestIlkTiklama       (3 test)  — Mayın sayısı, ilk hücre ve 8 komşu güvenli
TestHucreAcma        (3 test)  — acik sınıfı, sayılı metin, sıfır hücre boş
TestBayrak           (3 test)  — bayrak sınıfı, sol tıkta açılmama, kaldırma
TestYeniOyun         (2 test)  — mayinKonumlari null, tüm hücreler kapalı
TestOyunSonu         (4 test)  — Kazandın / Kaybettin metni, mayın ifşası, tıklama kilidi
```

**Sonuç: 20/20 PASSED — 8.04 saniye**

```
============================== 20 passed in 8.04s ==============================
```

---

## Emin olmadığım yerler

- **`pytest-playwright` uyumsuzluğu**: Ortamda hem `pytest-playwright` hem de `playwright` paketi
  kuruluydu; ancak `pytest-playwright`'ın `sync_api`'sini test fixture'larında direkt kullandım,
  eklentinin kendi fixture'ları (`page`, `browser`) ile çakışma riski var. Bu yüzden fixture
  isimlerini kasıtlı olarak özel tutmak yerine eklenti fixture'larının üstüne yazmak zorunda
  kaldım (ileri düzey pytest-playwright kurulumu olsaydı ayrı bir `conftest.py` tercih ederdim).
  Testler çalışıyor ve geçiyor, bu durum pratikte sorun yaratmadı.

- **Zincirleme açma — özyineleme derinliği**: 9×9 = 81 hücre için özyineleme yeterli,
  ancak çok büyük ızgaralarda stack overflow riski olurdu. Mevcut boyut için sorunsuz.

- **Görsel karşılaştırma**: EMIR.md "ekran görüntüsü alınıp karşılaştırılacak" diyor.
  Tasarım koyu tema (dark mode), renkli sayılar, hover animasyonu ve responsive boyutlarla
  iyi görünüyor; ancak referans ekran görüntüsü olmadığı için piksel düzeyinde karşılaştırma
  yapma imkânım olmadı.
