# Görev 2 — Mayın Tarlası · Rapor

## Ne yaptım

Bu klasörde tek dosyalık, oynanabilir bir mayın tarlası var: **`index.html`**.
Dış kaynak yok — CSS ve JS dosyanın içinde, `system-ui` yazı tipi ailesi dışında hiçbir şey
istenmiyor. Tahta 9×9, 10 mayın.

Oyun davranışı:

- İlk tıklamada mayınlar yerleşir; tıklanan hücre **ve 8 komşusu** mayınsız kalır
  (kenar/köşe tıklamalarında güvenli bölge 4 veya 6 hücreye iner, 9×9'da her zaman yeter).
- Açılan hücre komşu mayın sayısını gösterir; sayı 0 ise hücre boş görünür ve komşular
  kuyrukla (iteratif, `shift()` ile) zincirleme açılır.
- Sağ tık bayrak koyar/kaldırır; bayraklı hücre sol tıkla açılmaz, açık hücre bayraklanamaz.
- Mayına basınca kaybedilir, bütün mayınlar gösterilir, bastığın mayın kırmızı çerçeveyle
  ayrılır, yanlış konmuş bayraklar soluklaşır. Bütün mayınsız hücreler açılınca kazanılır;
  bayraklanmamış mayınlar yeşil "temiz" olarak işaretlenir.
- Oyun bittikten sonra tıklamalar tahtayı değiştirmez (`bitti` bayrağı tüm giriş noktalarında
  kontrol edilir).
- `Yeni oyun` (`#yeni`) her şeyi sıfırlar; mayınlar bir sonraki ilk tıklamada yeniden yerleşir.
- Ek olarak: kalan mayın sayacı, süre sayacı (ilk tıklamada başlar, oyun bitince durur),
  canlı durum satırı, klavye/odak desteği (her hücre gerçek `<button>`, `aria-label` durumu
  anlatır), 320 px'e kadar daralan düzen.

## Test edilebilirlik sözleşmesi — nasıl doğruladım

`test_mayin.py` yazdım; Playwright + Chromium ile **gerçek tarayıcıda** sürüyor
(`python3 -m pytest`, 20 test, hepsi geçiyor). Kapsananlar:

- 81 hücre, `data-r`/`data-c` 0–8 tam olarak birer kez.
- `window.mayinKonumlari()` ilk tıklamadan önce `null`; sonra tam 10, tekil, sınırlar içinde konum.
- `acik` / `bayrak` sınıfları; açıklı hücrenin metni yalnız rakam, 0 hücrenin metni boş;
  rakam, tahtadaki gerçek komşu mayın sayısıyla birebir tutarlı (9 farklı ilk tıklama konumu için).
- Zincirleme açılış: 0 hücreye tıklayınca mayın olmayan tüm komşular açılıyor, mayın komşular
  açılmıyor.
- Sağ tık bayrak koyuyor/kaldırıyor, bayraklı hücre sol tıkla açılmıyor.
- Kaybetme: `#durum` "Kaybettin" içeriyor, 10 mayının 10'u da `mayin` sınıfıyla görünür.
- Kazanma: `#durum` "Kazandın" içeriyor, tam 71 hücre `acik`.
- Oyun bittikten sonra 81 hücreye de sol hem sağ tık → tahta ve `#durum` metni birebir aynı.
- 20 rastgele tam oyun baştan sona oynanıyor; ilk tıklama güvenliği ve kazanma tutarlılığı denetleniyor.

Ayrıca elle de oynadım (tarayıcıda): kazanma → `#durum` = "Kazandın! 1 saniyede temizledin.",
kaybetme → "Kaybettin. 0 saniye dayandın." + 10 mayın görünür, sayfa konsolunda hiç hata yok.
Başlangıç / oynanış / kazanma / kaybetme / 320 px dar ekran için ekran görüntüsü aldım ve
tek tek inceledim; bu sırada bir ızgara hizası hatası buldum (sabit 34 px sütunlar 382 px'lik
kapsayıcıda sağda boş bir şerit bırakıyordu) ve düzelttim: tahta artık `1fr` sütunlarla
kapsayıcıyı dolduruyor, hücreler `aspect-ratio: 1` ile kare kalıyor.

## Emin olmadığım / karar verdiğim yerler

- **`acik` sınıfının anlamı.** Oyun sonunda gösterilen mayınlara `acik` vermedim; sözleşmede
  "açılmış sayılı hücre" diye geçtiği için `acik`'i yalnızca oyuncu tıklamasıyla açılan
  hücrelere ayırdım, mayınlar `mayin` (+ gerekiyorsa `bayrak`/`temiz`/`vuruldu`) sınıfını alıyor.
  Böylece kazanmada `.acik` sayısı tam 71 oluyor. Eğer bir kontrol betiği tersini beklerse
  (kaybettikten sonra bütün mayınlarda `acik` arıyorsa) bu tek satırlık bir değişiklik.
- **Yanlış bayrak kazanmayı engeller.** "Mayın olmayan bütün hücreler açılınca kazanılır"
  kuralını birebir uyguladım: bir temiz hücre yanlış bayraklanırsa onu açamazsın, kazanma o
  bayrağı kaldırana kadar gerçekleşmez. Klasik mayın tarlası da aynı şekilde davranır, ama
  EMIR.md'de bunu söylemedim diye not düşüyorum.
- **Bayrak glifi.** Metin olarak `⚑` (U+2691) kullandım — dış dosya/ikon olmadığı için.
  Tarayıcı bunu renkli emoji olarak çizerse CSS rengini yutmaz; görsel olarak yine de
  bayrağın kırmızı olması gerektiği için `⚑` yerine `⚐` ya da `✚` gibi düz bir karakter
  daha tutarlı olurdu. Şu anki hali kabul edilebilir.
- **Bayrak modu yok.** Dokunmatik ekranda sağ tık yok; telefonda bayrak koymak için uzun basma
  gibi bir jest eklemedim çünkü istenmemişti. Dar ekranda (320 px) tahta oynanabilir ama
  bayrağsız oynanır.
- **Test bağımlılığı.** Testler `playwright` + `chromium` gerektiriyor. Kurulu değilse
  `pip install playwright && playwright install chromium` gerekir; oyunun kendisi hiçbir
  pakete ihtiyaç duymuyor, tek dosya olduğu için çift tıklamakla oynanıyor.
