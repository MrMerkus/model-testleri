"""Türkçe metin işleme ve sayı dönüştürme araçları.

Bu modül, Türkçe dil kurallarına uygun harf büyütme/küçültme,
URL uyumlu kısa ad (slug) üretme ve tam sayıları Türkçe yazıya
çevirme işlevlerini içerir.
"""

from __future__ import annotations

import re

__all__ = ["buyuk", "kucuk", "slug", "sayi_yaziya"]

_BUYUK_MAP = {
    ord("i"): "İ",
    ord("ı"): "I",
}

_KUCUK_MAP = {
    ord("İ"): "i",
    ord("I"): "ı",
}

_SLUG_MAP = str.maketrans({
    "ç": "c",
    "ğ": "g",
    "ı": "i",
    "ö": "o",
    "ş": "s",
    "ü": "u",
})

_BIRLER = {
    1: "bir",
    2: "iki",
    3: "üç",
    4: "dört",
    5: "beş",
    6: "altı",
    7: "yedi",
    8: "sekiz",
    9: "dokuz",
}

_ONLAR = {
    1: "on",
    2: "yirmi",
    3: "otuz",
    4: "kırk",
    5: "elli",
    6: "altmış",
    7: "yetmiş",
    8: "seksen",
    9: "doksan",
}

_BASAMAKLAR = ["", "bin", "milyon", "milyar", "trilyon"]


def buyuk(metin: str) -> str:
    """Türkçe kurallarına uygun olarak metni büyük harfe çevirir.

    'i' -> 'İ', 'ı' -> 'I' dönüşümü yapılır. Diğer karakterler Python'un
    standart str.upper() davranışı ile çevrilir.
    """
    if not isinstance(metin, str):
        raise TypeError("Girdi bir karakter dizisi (str) olmalıdır.")
    return metin.translate(_BUYUK_MAP).upper()


def kucuk(metin: str) -> str:
    """Türkçe kurallarına uygun olarak metni küçük harfe çevirir.

    'İ' -> 'i', 'I' -> 'ı' dönüşümü yapılır. Diğer karakterler Python'un
    standart str.lower() davranışı ile çevrilir.
    """
    if not isinstance(metin, str):
        raise TypeError("Girdi bir karakter dizisi (str) olmalıdır.")
    return metin.translate(_KUCUK_MAP).lower()


def slug(metin: str) -> str:
    """URL'de kullanılabilir kısa ad üretir.

    Kurallar:
    1. Metni Türkçe kurallarla küçült.
    2. ç ğ ı ö ş ü harflerini c g i o s u yap.
    3. a-z ve 0-9 dışındaki her karakter dizisini tek bir '-' yap.
    4. Baştaki ve sondaki '-' karakterlerini sil.
    Sonuçta harf ya da rakam kalmıyorsa boş dize döner.
    """
    if not isinstance(metin, str):
        raise TypeError("Girdi bir karakter dizisi (str) olmalıdır.")

    # 1. Metni Türkçe kurallarla küçült
    s = kucuk(metin)
    # 2. Türkçe özel harfleri ASCII dengi yap
    s = s.translate(_SLUG_MAP)
    # 3. a-z ve 0-9 dışındaki her karakter dizisini tek bir '-' yap
    s = re.sub(r"[^a-z0-9]+", "-", s)
    # 4. Baştaki ve sondaki '-' karakterlerini sil
    return s.strip("-")


def _uc_basamak(n: int) -> list[str]:
    """0 ile 999 arasındaki sayıyı Türkçe kelime parçalarına ayırır."""
    kelimeler: list[str] = []
    yuzler = n // 100
    onlar = (n % 100) // 10
    birler = n % 10

    if yuzler == 1:
        kelimeler.append("yüz")
    elif yuzler > 1:
        kelimeler.append(_BIRLER[yuzler])
        kelimeler.append("yüz")

    if onlar > 0:
        kelimeler.append(_ONLAR[onlar])

    if birler > 0:
        kelimeler.append(_BIRLER[birler])

    return kelimeler


def sayi_yaziya(n: int) -> str:
    """Tam sayıyı Türkçe yazıya çevirir.

    Desteklenen aralık mutlak değerce 10**15'ten küçük sayılardır (|n| < 10**15).
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("Girdi bir tam sayı (int) olmalıdır.")

    if abs(n) >= 10**15:
        raise ValueError("Desteklenen aralık mutlak değerce 10**15'ten küçük sayılardır.")

    if n == 0:
        return "sıfır"

    negatif = n < 0
    kalan = abs(n)

    gruplar: list[int] = []
    while kalan > 0:
        gruplar.append(kalan % 1000)
        kalan //= 1000

    kelimeler: list[str] = []
    if negatif:
        kelimeler.append("eksi")

    for kademe in range(len(gruplar) - 1, -1, -1):
        grup = gruplar[kademe]
        if grup == 0:
            continue

        # Binler basamağı özel kuralı: 1000 -> 'bin' (bir bin değil)
        # Ancak milyon, milyar, trilyon için 'bir milyon', 'bir milyar' vb. kullanılır.
        if kademe == 1 and grup == 1:
            kelimeler.append("bin")
        else:
            kelimeler.extend(_uc_basamak(grup))
            if _BASAMAKLAR[kademe]:
                kelimeler.append(_BASAMAKLAR[kademe])

    return " ".join(kelimeler)
