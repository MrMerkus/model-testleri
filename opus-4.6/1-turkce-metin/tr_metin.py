"""Türkçe metin araçları – yalnız standart kütüphane."""

import re

# ── Türkçe büyük/küçük harf ──────────────────────────────────────────

_LOWER_TO_UPPER = str.maketrans("iıçğöşü", "İIÇĞÖŞÜ")
_UPPER_TO_LOWER = str.maketrans("İIÇĞÖŞÜ", "iıçğöşü")


def buyuk(metin: str) -> str:
    """Türkçe kurallarıyla büyük harfe çevirir (i→İ, ı→I)."""
    return metin.translate(_LOWER_TO_UPPER).upper()


def kucuk(metin: str) -> str:
    """Türkçe kurallarıyla küçük harfe çevirir (İ→i, I→ı)."""
    return metin.translate(_UPPER_TO_LOWER).lower()


# ── Slug ──────────────────────────────────────────────────────────────

_TR_CHARS = str.maketrans("çğıöşü", "cgiоsu")
# Not: ö → o harfi unicode latin 'о' olmamalı, düz ASCII 'o' olmalı.
_TR_CHARS = str.maketrans("çğıöşü", "cgiosu")


def slug(metin: str) -> str:
    """URL dostu kısa ad üretir."""
    metin = kucuk(metin)
    metin = metin.translate(_TR_CHARS)
    metin = re.sub(r"[^a-z0-9]+", "-", metin)
    metin = metin.strip("-")
    return metin


# ── Sayıyı yazıya çevirme ────────────────────────────────────────────

_BIRLER = [
    "", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"
]
_ONLAR = [
    "", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen",
    "doksan"
]
_BUYUK_BIRIMLER = [
    "",         # 10^0
    "bin",      # 10^3
    "milyon",   # 10^6
    "milyar",   # 10^9
    "trilyon",  # 10^12
]

_SINIR = 10**15


def _uc_basamak(n: int) -> str:
    """0 ≤ n ≤ 999 için Türkçe sözcükler döndürür (0 → boş dize)."""
    if n == 0:
        return ""
    parcalar = []
    yuzler = n // 100
    onlar = (n % 100) // 10
    birler = n % 10
    if yuzler == 1:
        parcalar.append("yüz")
    elif yuzler > 1:
        parcalar.append(_BIRLER[yuzler])
        parcalar.append("yüz")
    if onlar:
        parcalar.append(_ONLAR[onlar])
    if birler:
        parcalar.append(_BIRLER[birler])
    return " ".join(parcalar)


def sayi_yaziya(n: int) -> str:
    """Tam sayıyı Türkçe yazıya çevirir.

    Desteklenen aralık: |n| < 10^15.  int olmayan girdi (bool, float vb.)
    için TypeError, aralık dışı için ValueError fırlatır.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"int bekleniyor, {type(n).__name__} verildi")
    if abs(n) >= _SINIR:
        raise ValueError(
            f"Desteklenen aralık dışı: |{n}| >= 10^15"
        )

    if n == 0:
        return "sıfır"

    negatif = n < 0
    n = abs(n)

    gruplar: list[str] = []
    birim_idx = 0

    while n > 0:
        uc = n % 1000
        n //= 1000
        if uc:
            birim = _BUYUK_BIRIMLER[birim_idx]
            metin = _uc_basamak(uc)
            # "bin" özel: başına "bir" eklenmez.
            if birim == "bin" and metin == "bir":
                gruplar.append("bin")
            elif birim:
                gruplar.append(f"{metin} {birim}")
            else:
                gruplar.append(metin)
        birim_idx += 1

    gruplar.reverse()
    sonuc = " ".join(gruplar)

    if negatif:
        sonuc = "eksi " + sonuc

    return sonuc
