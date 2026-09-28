# RAPOR

## Ne Yapıldı?
Verilen `EMIR.md` dosyasındaki talimatlara uygun olarak, sadece standart kütüphane kullanılarak Türkçe metin işleme araçlarını barındıran `tr_metin.py` adlı modül kodlandı:
1. `buyuk()` ve `kucuk()` fonksiyonlarında, Python'un varsayılan davranışında sorun çıkaran `i/İ` ve `ı/I` harflerinin dönüşümü sağlandıktan sonra kalan karakterler için standart metotlar kullanıldı.
2. `slug()` fonksiyonu için metin küçültüldü, Türkçe karakterler İngilizce karşılıklarıyla değiştirildi ve harf/rakam dışı tüm karakter öbekleri `-` ile değiştirilerek baştaki/sondaki fazlalıklar temizlendi.
3. `sayi_yaziya()` fonksiyonunda `type(n) is int` kullanılarak, (Python'da bool, int'in alt sınıfı olmasına rağmen) boolean gibi istenmeyen türler için `TypeError` fırlatılması garanti altına alındı. Sayılar üçerli basamak gruplarına ayrılarak (bin, milyon, milyar, trilyon) Türkçe kurallarına uygun (ör. 1000 için "bir bin" değil "bin") şekilde metne çevrildi. -10**15 ile 10**15 aralığı dışında kalan değerler için `ValueError` koşulu konuldu.

## Test Durumu
Bütün özellikleri uç noktalarla ve özel vakalarla (örn. `0`, negatif sayılar, noktalama işaretli özel slug denemeleri) sınayan `test_tr_metin.py` test dosyası `pytest` çerçevesiyle yazılmıştır.
Yazılan testler `python3 -m pytest test_tr_metin.py` komutuyla çalıştırılmış olup **bütün testler (4/4) başarıyla geçmiş**, komut `0` çıkış kodu vermiştir.

## Belirsiz Durumlar ve Alınan Kararlar
1. **Tip Doğrulaması:** `sayi_yaziya` bölümünde "bool dahil" uyarısı mevcuttu. Bu belirsizliği / riski ortadan kaldırmak için `isinstance()` yerine doğrudan `type(n) is int` ile katı (strict) tür kontrolü yapıldı.
2. **Kalan Harflerin Çevirimi:** `buyuk` ve `kucuk` için, yalnızca "i/İ" ve "ı/I" çevrimlerinin manuel yapılması yetmiştir çünkü "ç, ş, ğ, ö, ü" gibi diğer Türkçe karakterler Python standart kütüphanesinin `.lower()` ve `.upper()` fonksiyonları tarafından halihazırda doğru olarak çevrilmektedir.
3. **Maksimum Sınır (Mutlak Değer):** `10**15` 'ten mutlak değerce küçük sayılar desteklenmesi istenmişti, bu sınır `not (-10**15 < n < 10**15)` şeklinde değerlendirilerek tam değer sınırında limit aşıldığı varsayıldı.
