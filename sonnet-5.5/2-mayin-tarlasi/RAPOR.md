# Rapor — Mayın tarlası

## Ne yaptım
Tek dosya `index.html` (satır içi CSS/JS, dış kaynak yok). 9×9, 10 mayın. Sözleşmedeki her
öğe var: `data-r`/`data-c`, `acik`/`bayrak` sınıfları, `#durum`, `#yeni`,
`window.mayinKonumlari()`. Zincirleme açma yığınla (özyinelemesiz) yapılıyor.

## Nasıl denedim
`test_mayin.py` (Playwright + pytest, `python3 -m pytest`): 7 test geçti.
- İlk tıklama ve 8 komşusu mayınsız (köşe/kenar/orta, her biri 15 tekrar), 10 benzersiz mayın.
- Açılan hücre metni doğru sayı; 0 hücre boş ve komşuları açık.
- Bayraklı hücre sol tıkla açılmaz, ilk tıklamadan önce bayrak koymak mayın yerleştirmez.
- Kayıp: `Kaybettin`, 10 mayın görünür, sonraki tıklamalar tahtayı değiştirmez.
- Kazanç: mayınsız 71 hücre açılınca `Kazandın`; `#yeni` sonrası `mayinKonumlari()` yine `null`.
- Ekran görüntüsü (`ekran.png`) alıp gözle baktım.

## Seçtiğim yorumlar (belirsiz yerler)
- Kayıpta gösterilen mayınlar `mayin` sınıfı alır, **`acik` almaz** (böylece `acik` sayısı yalnız
  gerçekten açılmış hücreleri sayar). Yanlış bayraklar `yanlis` sınıfı alır.
- Bayrak ve mayın simgeleri CSS `::before` ile çizilir; hücre metni boş kalır, yalnız sayılar metindir.
- Kazanınca kalan mayınlara otomatik `bayrak` sınıfı konur (klasik davranış).
- Açılmış hücreye sağ tık hiçbir şey yapmaz. Bayrak sayısı 10'u aşabilir, sayaç eksiye düşer.
- Çift tık/akor açma yok (istenmedi).

## Emin olmadığım yer
- Kazanınca otomatik bayrak, testin "bayraklı hücre sayısı" beklentisiyle çakışırsa sorun
  olabilir; sözleşmede yazmıyor, klasik davranışı seçtim.
- Yalnız Chromium'da denendi.
- `ekran.png` ve `test_mayin.py` klasörde kalıyor; teslim için gerekmiyor, silinebilir.
