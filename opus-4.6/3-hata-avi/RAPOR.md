# Hata Avı Raporu

**Toplam bulunan hata:** 5
**Etkilenen test:** 6 (düzeltme sonrası 8/8 yeşil)

---

## Hata 1 — `kitap_ekle`: adet üzerine yazılıyor

- **Satır:** 20
- **Sorun:** Aynı ISBN ile `kitap_ekle` çağrıldığında `self.kitaplar[isbn]["adet"] = adet` mevcut adedi sıfırlayıp yeni değeri yazıyordu; oysa mevcut adede eklemesi gerekir.
- **Düzeltme:** `= adet` → `+= adet`
- **Etkilenen test:** `test_ayni_kitap_tekrar_eklenince_adet_artar`

## Hata 2 — `musait`: iade edilen kitaplar da ödünçte sayılıyor

- **Satır:** 33
- **Sorun:** `musait()` tüm ödünç kayıtlarını (iade edilmiş olanlar dahil) sayıyordu. Raft sayısı hep düşük çıkıyordu.
- **Düzeltme:** Filtreye `and o["iade"] is None` eklendi; yalnızca aktif ödünçler sayılıyor.
- **Etkilenen test:** `test_iade_edilen_kitap_rafa_doner`

## Hata 3 — `odunc_ver`: limit kontrolü off-by-one

- **Satır:** 44
- **Sorun:** `len(...) > MAKS_ODUNC` yerine `>= MAKS_ODUNC` olmalıydı. MAKS_ODUNC=3 iken 3 kitabı olan üyeye 4. kitap veriliyordu.
- **Düzeltme:** `>` → `>=`
- **Etkilenen test:** `test_odunc_limiti_uc_kitap`

## Hata 4 — `son_tarih`: son gün bir gün erken hesaplanıyor

- **Satır:** 49
- **Sorun:** `timedelta(days=ODUNC_GUN - 1)` kullanılıyordu. Alış günü dahil olmadığına göre 1 Ocak + 14 gün = 15 Ocak olmalı. `-1` fazladan çıkarma yüzünden son gün 14 Ocak oluyordu.
- **Düzeltme:** `ODUNC_GUN - 1` → `ODUNC_GUN`
- **Etkilenen testler:** `test_son_gun_iade_cezasiz`, `test_bir_gun_gecikme_cezasi`

## Hata 5 — `populer`: sıralama artan (azdan çoğa) yapılıyor

- **Satır:** 67
- **Sorun:** `key=lambda x: (x[1], x[0])` artan sıra veriyordu; docstring'e göre çoktan aza olmalı.
- **Düzeltme:** `x[1]` → `-x[1]` (azalan sayı, artan ad)
- **Etkilenen test:** `test_populer_coktan_aza`
