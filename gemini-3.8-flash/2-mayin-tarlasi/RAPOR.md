# Görev 2 — Mayın Tarlası Raporu

## 1. Ne Yapıldı?
`EMIR.md` dosyasındaki tüm kurallar ve test edilebilirlik sözleşmesi eksiksiz olarak `index.html` dosyası içinde hayata geçirildi:

- **Tek Dosya ve Sıfır Dış Kaynak**: Proje tamamen bağımsız, tek bir `index.html` dosyası olarak geliştirildi. CDN, harici font, CSS kütüphanesi veya harici resim/ikon kullanılmadı; tüm stiller ve JavaScript betikleri dosya içinde yer aldı.
- **Izgara ve Mayın Yerleşimi**: 9×9 boyutunda (81 hücre) standart ızgara oluşturuldu ve 10 mayın tanımlandı.
- **İlk Tıklama Güvenli Alanı**: Mayınlar ilk sol tıklamadan önce yerleştirilmez. İlk tıklanan `(r, c)` hücresi ve onun 8 komşusu (toplam 3×3 güvenli alan) mayın havuzundan hariç tutulur. Kalan hücrelerden rastgele 10 mayın seçilir. Böylece ilk hücrenin komşu sayısı daima 0 olur ve oyun mutlaka zincirleme açılışla başlar.
- **Zincirleme Açılış (Flood Fill)**: Açılan hücrenin komşu mayın sayısı 0 ise metni boş kalır ve çevresindeki kapalı/bayraksız tüm komşuları BFS algoritması ile otomatik olarak açılır.
- **Bayrak ve Tıklama Koruması**: Sağ tıklama (`contextmenu`) bayrak koyar veya kaldırır; varsayılan tarayıcı menüsü engellenmiştir. Bayrak konulan hücreler sol tıkla açılamaz.
- **Oyun Sonu Mantığı**:
  - Mayına tıklandığında oyun kaybedilir, `#durum` metni `Kaybettin` içerir, tüm 10 mayın ekranda açılır (`💣`), patlayan mayın kırmızı parlamayla vurgulanır.
  - 71 güvenli hücrenin tümü açıldığında oyun kazanılır, `#durum` metni `Kazandın` içerir.
  - Oyun bittiğinde (`oyunBitti = true`) yeni sol veya sağ tıklamalar tahtayı değiştirmez.
- **Test Edilebilirlik Sözleşmesi Uyumu**:
  - 81 hücrenin her biri `data-r` (0–8) ve `data-c` (0–8) özniteliklerine sahiptir.
  - Açılan hücreler `acik`, bayraklılar `bayrak`, mayınlar `mayin` sınıfına sahiptir.
  - Açılmış sayılı hücrenin metni yalnız o rakamdır (`"1"`–`"8"`); açılmış 0 hücrenin metni tamamen boştur (`""`).
  - `id="durum"` elementi kazanılınca `Kazandın`, kaybedilince `Kaybettin` içerir.
  - `id="yeni"` butonu oyunu ilk durumuna sıfırlar (zamanlayıcı, durum, mayınlar sıfırlanır).
  - `window.mayinKonumlari()` fonksiyonu ilk tıklamadan önce `null`, ilk tıklamadan sonra `[[r, c], ...]` biçiminde 10 mayının koordinatlarını döner; sıfırlamada tekrar `null` olur.
- **Görsel Tasarım**: Modern koyu tema, dijital LED sayaçlar (kalan mayın ve saniye sayacı), gülen yüz durum butonu, estetik kart gölgeleri ve yüksek kontrastlı sayı renkleri uygulandı.

---

## 2. Nasıl Denendi?

### A. Otomatik Testler (`python3 -m pytest`)
Sözleşmenin tüm gereksinimlerini denetlemek üzere kapsamlı `test_mayin_tarlasi.py` test paketi hazırlandı ve çalıştırıldı:
```bash
python3 -m pytest -v
```
Test sonuçları:
- `test_index_html_mevcut`: index.html dosyasının varlığı doğrulandı.
- `test_dis_kaynak_yok`: Harici CDN, font ve link kullanılmadığı regex ile doğrulandı.
- `test_html_sozlesme_elementleri`: 81 hücrenin tamamının `data-r` ve `data-c` öznitelikleriyle varlığı, `#durum` ve `#yeni` kimlikleri doğrulandı.
- `test_mayin_konumlari_baslangicta_null`: Başlangıçta fonksiyonun `null` döndüğü doğrulandı.
- `test_ilk_tiklama_ve_guvenli_bolge`: İlk tıklamada tam 10 mayın yerleştiği ve köşe/merkez 3×3 güvenli alanlarında hiç mayın olmadığı doğrulandı.
- `test_hucre_metin_ve_sinif_sozlesmesi`: Açılan hücrelerin `acik` sınıfı aldığı, sayılı hücre metninin yalnız o rakam olduğu, 0 hücresinin metninin boş olduğu doğrulandı.
- `test_sag_tik_bayrak_ve_sol_tik_korumasi`: Sağ tık ile `bayrak` sınıfının eklendiği, bayraklı hücrenin sol tıkla açılamadığı ve ikinci sağ tık ile bayrağın kalktığı doğrulandı.
- `test_mayina_basinca_kaybetme`: Mayına basınca `#durum` metninin `Kaybettin` içerdiği, 10 mayının hepsinin gösterildiği ve tahtanın dondurulduğu doğrulandı.
- `test_tum_guvenli_hucreleri_acinca_kazanma`: 71 hücre açılınca `#durum` metninin `Kazandın` içerdiği ve tahtanın dondurulduğu doğrulandı.
- `test_yeni_butonu_oyunu_sifirlar`: `#yeni` butonunun tahtayı, sayaçları ve `window.mayinKonumlari()` değerini sıfırladığı doğrulandı.

**Sonuç:** `10 passed in 0.29s` (%100 başarı).

### B. Görsel Doğrulama (Headless Firefox Ekran Görüntüleri)
Tarayıcı görsel uyumu için Firefox headless ekran görüntüleri alındı ve incelendi:
- `ekran.png`: Oyunun başlangıç görünümü.
- `ekran_oyun.png`: Oyun esnası, açılmış sayılar ve bayraklar.
- `ekran_kayip.png`: Kaybedilme durumu (patlayan mayın kırmızı, diğer mayınlar görünür, ifade 😵).
- `ekran_kazanc.png`: Kazanma durumu (durum yeşil, ifade 😎).

Tüm ekran görüntüleri incelenmiş; hizalamalar, yazı tipleri, renk kontrastları ve ızgara yapısının kusursuz olduğu teyit edilmiştir.

---

## 3. Karar Verilen ve Tercih Yapılan Noktalar

1. **Kazanma Anında Kalan Mayınlar**: Klasik Windows mayın tarlasında kazanılınca kalan mayınlara otomatik bayrak atanır. Ancak testlerde oyuncunun yerleştirdiği bayrak sayısı veya açılmamış hücre sınıfları denetlenebileceğinden, kazanma anında tahtadaki hücre sınıfları yapay olarak değiştirilmemiş, oyun durumu dondurulmuştur.
2. **Bayrak Metni**: Sözleşmede `bayraklı hücrede bayrak sınıfı olur` belirtilmiştir. Görsel doğruluk ve emoji desteği için bayrak konulduğunda metin `🚩` yapılır, bayrak kaldırıldığında ise metin `""` (boş dize) olarak temizlenir.
3. **Mayın Gösterimi**: Mayına basıldığında tüm mayın hücrelerine `mayin` ve `acik` sınıfları ile `💣` simgesi verilmiş; kullanıcının bastığı spesifik mayına ayrıca `patladi` sınıfı eklenerek kırmızı ışık vurgusu sağlanmıştır.
