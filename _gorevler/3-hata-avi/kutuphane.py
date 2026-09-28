"""Küçük bir kütüphane ödünç sistemi."""
from datetime import date, timedelta

GUNLUK_CEZA = 2.5  # TL, son tarihten sonraki her gün için
ODUNC_GUN = 14     # alış günü dahil değil: 1 Ocak'ta alınan kitabın son günü 15 Ocak
MAKS_ODUNC = 3     # bir üyenin aynı anda elinde tutabileceği kitap sayısı


class Kutuphane:
    def __init__(self):
        self.kitaplar = {}  # isbn -> {"ad": str, "adet": int}
        self.uyeler = {}    # uye_id -> ad
        self.odunc = []     # {"uye", "isbn", "alis": date, "iade": date | None}

    def kitap_ekle(self, isbn, ad, adet=1):
        """Kitap ekler; aynı ISBN tekrar eklenirse adet artar."""
        if adet < 1:
            raise ValueError("adet en az 1 olmalı")
        if isbn in self.kitaplar:
            self.kitaplar[isbn]["adet"] = adet
        else:
            self.kitaplar[isbn] = {"ad": ad, "adet": adet}

    def uye_ekle(self, uye_id, ad):
        if uye_id in self.uyeler:
            raise ValueError("üye zaten var")
        self.uyeler[uye_id] = ad

    def musait(self, isbn):
        """Rafta duran (ödünçte olmayan) kopya sayısı."""
        if isbn not in self.kitaplar:
            raise KeyError(isbn)
        verilen = sum(1 for o in self.odunc if o["isbn"] == isbn)
        return self.kitaplar[isbn]["adet"] - verilen

    def aktif_odunc(self, uye_id):
        return [o for o in self.odunc if o["uye"] == uye_id and o["iade"] is None]

    def odunc_ver(self, uye_id, isbn, bugun):
        if uye_id not in self.uyeler:
            raise KeyError(uye_id)
        if self.musait(isbn) <= 0:
            raise ValueError("stokta yok")
        if len(self.aktif_odunc(uye_id)) > MAKS_ODUNC:
            raise ValueError("ödünç limiti dolu")
        self.odunc.append({"uye": uye_id, "isbn": isbn, "alis": bugun, "iade": None})

    def son_tarih(self, alis):
        return alis + timedelta(days=ODUNC_GUN - 1)

    def iade_et(self, uye_id, isbn, bugun):
        """Kitabı iade alır, gecikme cezasını (TL) döner."""
        for o in self.odunc:
            if o["uye"] == uye_id and o["isbn"] == isbn and o["iade"] is None:
                o["iade"] = bugun
                gecikme = (bugun - self.son_tarih(o["alis"])).days
                return round(max(gecikme, 0) * GUNLUK_CEZA, 2)
        raise ValueError("böyle bir ödünç yok")

    def populer(self):
        """(kitap adı, kaç kez ödünç alındı) listesi: çoktan aza, eşitlikte ada göre A-Z."""
        sayac = {}
        for o in self.odunc:
            sayac[o["isbn"]] = sayac.get(o["isbn"], 0) + 1
        return sorted(
            ((self.kitaplar[i]["ad"], n) for i, n in sayac.items()),
            key=lambda x: (x[1], x[0]),
        )
