"""
tr_metin.py — Türkçe metin araçları
Yalnızca standart kütüphane kullanılmıştır.
"""

import re

# ---------------------------------------------------------------------------
# Büyük / küçük harf çevirimi
# ---------------------------------------------------------------------------

_BUYUK_TABLO = str.maketrans("iı", "İI")
_KUCUK_TABLO = str.maketrans("İI", "iı")


def buyuk(metin: str) -> str:
    """Metni Türkçe kurallarıyla büyük harfe çevirir (i→İ, ı→I)."""
    return metin.translate(_BUYUK_TABLO).upper()


def kucuk(metin: str) -> str:
    """Metni Türkçe kurallarıyla küçük harfe çevirir (İ→i, I→ı)."""
    return metin.translate(_KUCUK_TABLO).lower()


# ---------------------------------------------------------------------------
# Slug üretimi
# ---------------------------------------------------------------------------

_TURKCE_ASCII = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosucgiosu")


def slug(metin: str) -> str:
    """Metni URL dostu bir slug'a dönüştürür."""
    # 1. Türkçe küçük harfe çevir
    sonuc = kucuk(metin)
    # 2. Türkçe/aksan harflerini ASCII karşılıklarına çevir
    sonuc = sonuc.translate(_TURKCE_ASCII)
    # 3. a-z ve 0-9 dışındaki her karakter dizisini tek '-' yap
    sonuc = re.sub(r"[^a-z0-9]+", "-", sonuc)
    # 4. Baş ve sondaki '-' karakterlerini sil
    sonuc = sonuc.strip("-")
    return sonuc


# ---------------------------------------------------------------------------
# Sayıyı Türkçe yazıya çevirme
# ---------------------------------------------------------------------------

_BIRLER = [
    "", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"
]
_ONLAR = [
    "", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"
]

# (basamak_değeri, ad)  — büyükten küçüğe
_BASAMAKLAR = [
    (10 ** 12, "trilyon"),
    (10 ** 9,  "milyar"),
    (10 ** 6,  "milyon"),
    (10 ** 3,  "bin"),
]

_SINIR = 10 ** 15


def _uc_basamak(n: int) -> str:
    """0-999 arasındaki tam sayıyı Türkçe sözcüklerle döndürür."""
    assert 0 <= n <= 999
    parcalar = []
    yuzler = n // 100
    n %= 100
    onlar = n // 10
    birler = n % 10

    if yuzler == 1:
        parcalar.append("yüz")
    elif yuzler > 1:
        parcalar.append(_BIRLER[yuzler] + " yüz")

    if onlar:
        parcalar.append(_ONLAR[onlar])

    if birler:
        parcalar.append(_BIRLER[birler])

    return " ".join(parcalar)


def sayi_yaziya(n: int) -> str:
    """Tam sayıyı Türkçe yazıya çevirir."""
    # Tip kontrolü — bool, float vb. kabul etme
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"int bekleniyor, {type(n).__name__} verildi")

    if abs(n) >= _SINIR:
        raise ValueError(f"Desteklenen aralık dışında: {n}")

    if n == 0:
        return "sıfır"

    eksi = n < 0
    n = abs(n)

    parcalar = []

    for deger, ad in _BASAMAKLAR:
        if n >= deger:
            katsayi = n // deger
            n %= deger
            # Özel kural: tam 1 bin → "bin" (bir bin değil)
            if deger == 10 ** 3 and katsayi == 1:
                parcalar.append("bin")
            else:
                parcalar.append(_uc_basamak(katsayi) + " " + ad)

    if n > 0:
        parcalar.append(_uc_basamak(n))

    sonuc = " ".join(parcalar)
    if eksi:
        sonuc = "eksi " + sonuc
    return sonuc
