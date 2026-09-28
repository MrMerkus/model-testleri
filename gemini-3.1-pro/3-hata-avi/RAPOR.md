# Hata Avı Raporu

Görev kapsamında `kutuphane.py` dosyasında toplam **5 adet** hata tespit edilmiş ve düzeltilmiştir. Hatalar ve çözüm yöntemleri aşağıda listelenmiştir:

1. **Kitap Ekleme (Adet Güncelleme) Hatası:**
   - **Sorun:** `kitap_ekle` metodunda kütüphanede zaten var olan bir kitap (aynı ISBN ile) tekrar eklendiğinde, var olan stok miktarı ile toplanmak yerine yeni adet değeri eski değerin üzerine yazılıyordu (`self.kitaplar[isbn]["adet"] = adet`).
   - **Çözüm:** Atama işlemi `+=` operatörü ile değiştirilerek mevcut adedin üzerine eklenmesi sağlandı.

2. **Müsait Kitap Sayısı (Stok) Hatası:**
   - **Sorun:** `musait` metodunda rafta bulunan kitap sayısı hesaplanırken, daha önce ödünç alınıp iade edilmiş kayıtlar da ödünçte gibi sayılıyordu.
   - **Çözüm:** Ödünç kayıtlarını filtreleyen list comprehension'a `o["iade"] is None` koşulu eklenerek sadece henüz iade edilmemiş aktif ödünçlerin stoktan düşülmesi sağlandı.

3. **Ödünç Alma Limiti Kontrolü Hatası:**
   - **Sorun:** `odunc_ver` metodunda üyenin ödünç limiti `> MAKS_ODUNC` ile kontrol ediliyordu. Bu, üyenin limite ulaştıktan sonra limit aşımı yaparak 1 kitap daha (toplam 4 kitap) alabilmesine neden oluyordu.
   - **Çözüm:** Koşul `>= MAKS_ODUNC` olarak değiştirilerek üyenin elindeki kitap sayısı limiti bulduğu an yeni kitap alması engellendi.

4. **Son İade Tarihi Hesaplama Hatası:**
   - **Sorun:** `son_tarih` metodunda son tarih hesaplanırken ödünç gününden 1 çıkarılıyordu (`ODUNC_GUN - 1`), bu da gecikme cezasının 1 gün erken işlemeye başlamasına neden oluyordu (1 Ocak + 13 gün = 14 Ocak).
   - **Çözüm:** Koda yorumlarda belirtilen (1 Ocak -> 15 Ocak) hedefe ulaşabilmek için gün hesabından `- 1` çıkarıldı ve doğrudan `ODUNC_GUN` süresi eklendi.

5. **Popüler Kitaplar Sıralama Hatası:**
   - **Sorun:** `populer` metodunda dönen ödünç alınma sayısı sıralaması, `key=lambda x: (x[1], x[0])` kullanıldığı için azdan çoğa doğru (artan) gerçekleşiyordu. 
   - **Çözüm:** Çoktan aza (azalan) sıralama sağlamak amacıyla, tuple'daki ödünç sayısı negatif değere (`-x[1]`) çevrilerek sayıya göre azalan, eşitlik durumunda da isme göre A-Z'ye artan sıralanması sağlandı.
