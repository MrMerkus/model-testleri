# Hata Avı Raporu

`kutuphane.py` dosyası incelendiğinde ve testler çalıştırıldığında toplam **5 adet mantıksal hata** tespit edilmiş ve kökünden düzeltilmiştir.

---

## Bulunan Hatalar ve Düzeltmeler

### 1. `kitap_ekle`: Mevcut Kitabın Adedinin Üzerine Yazılması
- **Hata:** Aynı ISBN ile tekrar kitap eklendiğinde `self.kitaplar[isbn]["adet"] = adet` satırı çalışıyor, mevcut adet artırılmak yerine yeni eklenen adetle eziliyordu.
- **Düzeltme:** `self.kitaplar[isbn]["adet"] += adet` olarak değiştirildi. Böylece mevcut kopyalara yeni gelen adet eklenir hale getirildi.

### 2. `musait`: İade Edilmiş Kitapların Halen Ödünçte Sayılması
- **Hata:** `musait` fonksiyonunda raftaki adet hesaplanırken `verilen = sum(1 for o in self.odunc if o["isbn"] == isbn)` kullanılıyordu. Bu ifade, daha önce iade edilmiş (`o["iade"] is not None`) kitapları da ödünç verilmiş sayıyor ve iade edilen kitaplar rafa geri dönmüyordu.
- **Düzeltme:** Yalnızca aktif (henüz iade edilmemiş) ödünçleri sayacak şekilde `o["iade"] is None` koşulu eklendi:
  `verilen = sum(1 for o in self.odunc if o["isbn"] == isbn and o["iade"] is None)`

### 3. `odunc_ver`: Maksimum Ödünç Limitinin Aşılmasına İzin Verilmesi
- **Hata:** Bir üyenin aktif ödünç sayısı kontrolünde `len(self.aktif_odunc(uye_id)) > MAKS_ODUNC` kullanılmıştı. `MAKS_ODUNC = 3` iken üye 3 kitaba sahip olduğunda `3 > 3` yanlış olduğu için 4. kitabı almasına izin veriliyordu.
- **Düzeltme:** Karşılaştırma operatörü `>=` yapıldı:
  `if len(self.aktif_odunc(uye_id)) >= MAKS_ODUNC:`

### 4. `son_tarih`: Ödünç Süresinde 1 Günlük Sapma (Off-by-one)
- **Hata:** `ODUNC_GUN = 14` olarak tanımlanmış ve kurala göre 1 Ocak'ta alınan kitabın son teslim günü 15 Ocak (`1 + 14 = 15`) olarak belirtilmiştir. Ancak `son_tarih` fonksiyonunda `alis + timedelta(days=ODUNC_GUN - 1)` yazılarak son gün 14 Ocak hesaplanıyor, bu yüzden son gününde (15 Ocak) yapılan iadeler 1 gün gecikmeli sayılıp haksız ceza kesiliyordu.
- **Düzeltme:** `ODUNC_GUN - 1` yerine `ODUNC_GUN` kullanıldı:
  `return alis + timedelta(days=ODUNC_GUN)`

### 5. `populer`: Sıralama Yönünün Ters Olması
- **Hata:** `populer` fonksiyonunda `sorted(..., key=lambda x: (x[1], x[0]))` kullanılmıştı. Python'ın varsayılan sıralaması artan (küçükten büyüğe) olduğu için kitaplar ödünç alma sayısına göre çoktan aza değil, azdan çoka sıralanıyordu.
- **Düzeltme:** Ödünç sayısına göre azalan, isim eşitliğinde ise alfabetik (A-Z) artan sıralama elde etmek için sıralama anahtarı `key=lambda x: (-x[1], x[0])` olarak güncellendi.

---

## Test Sonucu

Tüm düzeltmelerin ardından `python3 -m pytest -q` çalıştırıldı:
```
8 passed in 0.01s
```
Tüm testler başarıyla geçmiş ve sistem gereksinimleri eksiksiz karşılanmıştır.
