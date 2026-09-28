# Hata Avı — Rapor

Toplam **5 hata** bulundu ve düzeltildi. Tüm testler (`8/8`) yeşil.

---

## Hata 1 — `kitap_ekle`: adet birikmiyor, üzerine yazılıyor

**Satır:** 20  
**Sorun:** Aynı ISBN tekrar eklendiğinde `self.kitaplar[isbn]["adet"] = adet` ifadesi mevcut adeti silip yerine yenisini yazıyordu.  
**Etki:** `test_ayni_kitap_tekrar_eklenince_adet_artar` başarısız (2+3=5 beklenirken 3 dönüyordu).  
**Düzeltme:**
```python
# Önce
self.kitaplar[isbn]["adet"] = adet
# Sonra
self.kitaplar[isbn]["adet"] += adet
```

---

## Hata 2 — `musait`: iade edilmiş kitaplar hâlâ stoktan düşülüyordu

**Satır:** 33  
**Sorun:** `verilen` sayısı hesaplanırken iade edilmiş kayıtlar (`o["iade"] is not None`) da sayılıyordu; kitap iade edilse bile rafta görünmüyordu.  
**Etki:** `test_iade_edilen_kitap_rafa_doner` başarısız (iade sonrası musait=1 beklenirken 0 dönüyordu).  
**Düzeltme:**
```python
# Önce
verilen = sum(1 for o in self.odunc if o["isbn"] == isbn)
# Sonra
verilen = sum(1 for o in self.odunc if o["isbn"] == isbn and o["iade"] is None)
```

---

## Hata 3 — `odunc_ver`: limit kontrolü yanlış operatör

**Satır:** 44  
**Sorun:** `> MAKS_ODUNC` koşulu, aktif ödünç sayısı tam 3 iken (limit dolu) yeni ödünç vermeye izin veriyordu; ancak 4'e ulaşınca hata veriyordu.  
**Etki:** `test_odunc_limiti_uc_kitap` başarısız (3 kitap alındıktan sonra 4. ValueError fırlatmalıyken fırlatmıyordu).  
**Düzeltme:**
```python
# Önce
if len(self.aktif_odunc(uye_id)) > MAKS_ODUNC:
# Sonra
if len(self.aktif_odunc(uye_id)) >= MAKS_ODUNC:
```

---

## Hata 4 — `son_tarih`: son gün hesabında bir gün eksik

**Satır:** 49  
**Sorun:** `ODUNC_GUN - 1` = 13 gün eklendi; oysa yorum satırı da belirttiği üzere 1 Ocak'ta alınan kitabın son günü 15 Ocak (14 gün sonra) olmalıydı.  
**Etki:** `test_son_gun_iade_cezasiz` ve `test_bir_gun_gecikme_cezasi` başarısız (son tarih bir gün erken hesaplandığı için ceza yanlış çıkıyordu).  
**Düzeltme:**
```python
# Önce
return alis + timedelta(days=ODUNC_GUN - 1)
# Sonra
return alis + timedelta(days=ODUNC_GUN)
```

---

## Hata 5 — `populer`: sıralama artan, azalan olmalıydı

**Satır:** 67  
**Sorun:** `key=lambda x: (x[1], x[0])` artan sıralama yapıyor; popülerlik listesi çoktan aza istendiği için `x[1]` negatif alınmalıydı.  
**Etki:** `test_populer_coktan_aza` başarısız (en çok ödünç alınan kitap sona geliyordu).  
**Düzeltme:**
```python
# Önce
key=lambda x: (x[1], x[0]),
# Sonra
key=lambda x: (-x[1], x[0]),
```

---

## Sonuç

| # | Fonksiyon | Hata türü |
|---|-----------|-----------|
| 1 | `kitap_ekle` | `=` yerine `+=` olmalıydı |
| 2 | `musait` | İade filtresiz sayım |
| 3 | `odunc_ver` | `>` yerine `>=` olmalıydı |
| 4 | `son_tarih` | Gereksiz `-1` ile off-by-one |
| 5 | `populer` | Artan yerine azalan sıralama |

```
8 passed in 0.01s ✅
```
