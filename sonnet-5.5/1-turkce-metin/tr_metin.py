"""Türkçe metin araçları: büyük/küçük harf, slug ve sayıyı yazıya çevirme."""

import re

_BUYUK_TABLO = str.maketrans("iı", "İI")
_KUCUK_TABLO = str.maketrans("İI", "iı")
_ASCII_TABLO = str.maketrans("çğıöşü", "cgiosu")
_AYIRICI = re.compile(r"[^a-z0-9]+")

_BIRLER = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
_ONLAR = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
_BASAMAKLAR = ["", "bin", "milyon", "milyar", "trilyon"]
_SINIR = 10**15


def buyuk(metin: str) -> str:
    """Türkçe kurallarıyla büyük harfe çevirir (i→İ, ı→I)."""
    return metin.translate(_BUYUK_TABLO).upper()


def kucuk(metin: str) -> str:
    """Türkçe kurallarıyla küçük harfe çevirir (İ→i, I→ı)."""
    return metin.translate(_KUCUK_TABLO).lower()


def slug(metin: str) -> str:
    """URL'de kullanılabilir kısa ad üretir."""
    ascii_metin = kucuk(metin).translate(_ASCII_TABLO)
    return _AYIRICI.sub("-", ascii_metin).strip("-")


def _uc_hane(n: int) -> str:
    """0 < n < 1000 için yazı; kelimeler boşlukla ayrılır."""
    yuz, kalan = divmod(n, 100)
    on, bir = divmod(kalan, 10)
    kelimeler = []
    if yuz:
        if yuz > 1:
            kelimeler.append(_BIRLER[yuz])
        kelimeler.append("yüz")
    if on:
        kelimeler.append(_ONLAR[on])
    if bir:
        kelimeler.append(_BIRLER[bir])
    return " ".join(kelimeler)


def sayi_yaziya(n: int) -> str:
    """Tam sayıyı Türkçe yazıya çevirir."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n bir int olmalı")
    if abs(n) >= _SINIR:
        raise ValueError("|n| 10**15'ten küçük olmalı")
    if n == 0:
        return "sıfır"

    onek = "eksi " if n < 0 else ""
    n = abs(n)
    parcalar = []
    for basamak in _BASAMAKLAR:
        n, grup = divmod(n, 1000)
        if grup:
            if basamak == "bin" and grup == 1:
                parcalar.append("bin")
            elif basamak:
                parcalar.append(_uc_hane(grup) + " " + basamak)
            else:
                parcalar.append(_uc_hane(grup))
        if not n:
            break
    return onek + " ".join(reversed(parcalar))
