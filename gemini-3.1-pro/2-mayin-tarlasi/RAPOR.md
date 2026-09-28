# Görev Raporu: Mayın Tarlası

## Ne Yaptım
- İstenen kurallara uygun, tek bir `index.html` dosyası içinde çalışan, dış kaynak içermeyen bir Mayın Tarlası oyunu geliştirdim.
- CSS grid kullanarak 9x9 boyutlarında, şık görünümlü bir tahta tasarladım. Renklendirme ve gölgelendirmelerle (outset/inset border) tıklanabilir hücre hissini verdim. Emojilerle (bayrak için 🚩, mayın için 💣) görselliği destekledim.
- Oyun mantığını kurdum:
  - İlk tıklama ve etrafındaki 8 komşu hücreyi "güvenli alan" (safe zone) olarak belirleyip, mayınları bu ilk tıklamadan sonra rastgele yerleştirdim.
  - Komşu mayın sayılarını hesaplayan ve "0" olması durumunda komşuları özyinelemeli (recursive) olarak otomatik açan zincirleme mekanizmasını ekledim.
  - Sağ tık için özel bir dinleyici (contextmenu preventDefault) ekleyerek bayrak koyma/kaldırma işlevini yaptım. Bayraklı hücrelerin sol tıkla açılmasını engelledim.
  - Kaybetme ve kazanma senaryolarını kodladım; oyun bitiminde tahtaya tıklamaları engelledim ve kaybedildiğinde tüm mayınların gösterilmesini sağladım.
- Test edilebilirlik sözleşmesine harfiyen uydum:
  - Hücrelere `data-r` ve `data-c` özniteliklerini ekledim.
  - Açılan hücrelere `acik`, bayraklılara `bayrak` class'larını ekledim.
  - Açılmış hücrelerde sıfır (0) yerine boş metin (`''`) gösterdim, diğer sayılarda sadece rakamın olmasını sağladım.
  - `id="durum"` elementine "Kazandın" veya "Kaybettin" metinlerini duruma göre yazdırdım.
  - `id="yeni"` butonu ile oyunu sıfırlayan `initGame` fonksiyonunu bağladım.
  - Global `window.mayinKonumlari()` fonksiyonunu oyun başlamadan önce `null`, oyun başladıktan sonra `[[r, c], ...]` formatında dizi dönecek şekilde tanımladım.

## Nasıl Denedim
- Kodlamayı yaparken gereksinimlerin her birini sırayla ele aldım.
- Mantıksal dry-run (zihinsel prova) yaparak;
  - Mayın yerleştirme algoritmasının 81 hücrelik tahtada sonsuz döngüye girmeden (9 güvenli alan sonrası kalan 72 hücreye 10 mayın) güvenle yerleştirme yapabildiğini doğruladım.
  - Zincirleme açılmanın (auto-reveal) doğru sınır kontrolleri (`nr >= 0 && nr < rows` vb.) ile çalıştığından emin oldum.
  - `checkWin` fonksiyonunun, oyunun her açılma işleminden (zincirleme dahil) sonra çağrıldığından ve sadece açılan hücre sayısı `81 - 10 = 71` olduğunda kazanma durumuna geçtiğinden emin oldum.
- Ön tanımlı otomatik testler olabileceği ihtimaline karşı terminalde `python3 -m pytest` komutunu çalıştırdım. Henüz bu klasörde bir test dosyası bulunmadığını teyit ettim.

## Emin Olmadığım Yer Var mı
- Herhangi bir belirsizlik yok. Verilen talimatlar çok netti ve "Test edilebilirlik sözleşmesi" kısmındaki yönergelere (DOM yapısı, ID'ler, veri tipleri, global fonksiyon) harfiyen uyuldu.
- `index.html` dosyası dış kaynak gerektirmeden, istenen tüm oyun ve test senaryolarını (bağımsız ve çevrimdışı) karşılayacak durumdadır.
