# Görev 2 — Mayın tarlası

Bu klasörde **tek bir `index.html` dosyası** olarak oynanabilir bir mayın tarlası yap. Dış
kaynak yok: CDN, font, resim dosyası yok; bütün CSS ve JavaScript dosyanın içinde.

## Oyun kuralları
- 9×9 ızgara, 10 mayın.
- **İlk tıklanan hücre ve onun 8 komşusu mayınsızdır.** Mayınlar ilk tıklamadan sonra
  yerleştirilir.
- Açılan hücre komşu mayın sayısını gösterir; sayı 0 ise hücre boş görünür ve komşuları
  otomatik açılır (zincirleme).
- Sağ tık bayrak koyar / kaldırır. Bayraklı hücre sol tıkla açılmaz.
- Mayına basınca oyun kaybedilir ve bütün mayınlar gösterilir. Mayın olmayan bütün hücreler
  açılınca oyun kazanılır. Oyun bitince tıklamalar tahtayı değiştirmez.

## Test edilebilirlik sözleşmesi (otomatik testler buna bakacak, harfiyen uy)
- Her hücre bir element: `data-r` (satır, 0–8) ve `data-c` (sütun, 0–8) özellikleriyle.
- Açılmış hücrede `acik` sınıfı, bayraklı hücrede `bayrak` sınıfı olur.
- Açılmış sayılı hücrenin metni yalnız o rakamdır; açılmış 0 hücrenin metni boştur.
- `id="durum"` olan bir element: kazanınca metni `Kazandın` içerir, kaybedince `Kaybettin`
  içerir.
- `id="yeni"` olan bir buton oyunu sıfırlar (mayınlar bir sonraki ilk tıklamada yeniden
  yerleşir).
- `window.mayinKonumlari()` fonksiyonu: ilk tıklamadan önce `null`, sonra `[[r, c], ...]`
  biçiminde 10 mayının konumunu döner.

## Ayrıca
- Güzel ve düzgün görünsün; ekran görüntüsü alınıp karşılaştırılacak.
- İş bitince bu klasöre kısa bir `RAPOR.md` yaz: ne yaptın, nasıl denedin, emin olmadığın
  yer var mı.
- Yalnız bu klasörde çalış. İnternete çıkma, başka klasörlere bakma.
