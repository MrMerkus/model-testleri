"""Türkçe metin araçları.

Standart kütüphane dışında hiçbir bağımlılık kullanılmaz.
"""

from __future__ import annotations

__all__ = ["buyuk", "kucuk", "slug", "sayi_yaziya"]


# ---------------------------------------------------------------- harf çevirisi

_KUCUK_HARF_ESLESME = str.maketrans({"İ": "i", "I": "ı", "Ş": "ş", "Ğ": "ğ"})
_BUYUK_HARF_ESLESME = str.maketrans({"i": "İ", "ı": "I", "ş": "Ş", "ğ": "Ğ"})


def kucuk(metin: str) -> str:
    """Türkçe kurallarıyla küçük harfe çevirir (``I -> ı``, ``İ -> i``)."""
    return metin.translate(_KUCUK_HARF_ESLESME).lower()


def buyuk(metin: str) -> str:
    """Türkçe kurallarıyla büyük harfe çevirir (``i -> İ``, ``ı -> I``)."""
    return metin.translate(_BUYUK_HARF_ESLESME).upper()


# ---------------------------------------------------------------- slug

_SESKIL_SES_UZUN = str.maketrans({"ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u"})


def slug(metin: str) -> str:
    """URL'de kullanılabilir kısa ad üretir."""
    duz = kucuk(metin).translate(_SESKIL_SES_UZUN)
    parcalar = []
    basladi = False
    for karakter in duz:
        if "a" <= karakter <= "z" or "0" <= karakter <= "9":
            parcalar.append(karakter)
            basladi = True
        elif basladi:
            parcalar.append("-")
            basladi = False
    return "".join(parcalar).strip("-")


# ---------------------------------------------------------------- sayı yazıya

_Rakamlar = "bir iki üç dört beş altı yedi sekiz dokuz".split()
_Onlukler = "yirmi otuz kırk elli altmış yetmiş seksen doksan".split()
_BASAMAK_ADLARI = ("", "bin", "milyon", "milyar", "trilyon")
_EN_BUYUK_DEGER = 10 ** 15  # desteklenen aralık: |n| < 10**15


def _yuzden_kucuk_uc_basamak(sayi: int) -> str:
    """0 <= sayi <= 999 için Türkçe yazım (virgülsüz, bağımsız parça)."""
    yuzler, kalan = divmod(sayi, 100)
    parcalar = []
    if yuzler:
        parcalar.append("yüz" if yuzler == 1 else f"{_Rakamlar[yuzler - 1]} yüz")
    if kalan:
        birler, onlar = divmod(kalan, 10)
        if birler:
            parcalar.append(_Rakamlar[birler - 1])
        if onlar:
            parcalar.append("on" if onlar == 1 else _Onlukler[onlar - 2])
    return " ".join(parcalar)


def sayi_yaziya(n: int) -> str:
    """Tam sayıyı Türkçe yazıya çevirir. |n| < 10**15 olmalıdır."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"tam sayı bekleniyordu, {type(n).__name__} verildi")
    if not -_EN_BUYUK_DEGER < n < _EN_BUYUK_DEGER:
        raise ValueError(f"desteklenen aralık |n| < {_EN_BUYUK_DEGER}, verilen: {n}")

    if n == 0:
        return "sıfır"

    isaret = "eksi " if n < 0 else ""
    kalan = abs(n)

    gruplar = []
    while kalan:
        grup, kalan = divmod(kalan, 1000)
        gruplar.append(grup)

    parcalar = []
    for basamak in range(len(gruplar) - 1, -1, -1):
        grup = gruplar[basamak]
        if basamak == 0:
            parcalar.append(_yuzden_kucuk_uc_basamak(grup))
        elif basamak == 1:
            # "bin" öncesinde "bir" söylenmez: 1000 -> "bin"
            parcalar.append("bin" if grup == 1 else f"{_yuzden_kucuk_uc_basamak(grup)} bin")
        else:
            parcalar.append(f"{_yuzden_kucuk_uc_basamak(grup)} {_BASAMAK_ADLARI[basamak]}")
    return isaret + " ".join(parcalar)
