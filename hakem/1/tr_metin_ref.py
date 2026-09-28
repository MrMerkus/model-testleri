"""Görev 1 referans çözümü (hakem)."""
import re

_BUYUK = str.maketrans({"i": "İ", "ı": "I"})
_KUCUK = str.maketrans({"I": "ı", "İ": "i"})
_ASCII = str.maketrans("çğıöşü", "cgiosu")


def buyuk(metin):
    return metin.translate(_BUYUK).upper()


def kucuk(metin):
    return metin.translate(_KUCUK).lower()


def slug(metin):
    s = kucuk(metin).translate(_ASCII)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


_BIR = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
_ON = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
_BASAMAK = ["", "bin", "milyon", "milyar", "trilyon"]


def _uc(n):
    y, o, b = n // 100, n // 10 % 10, n % 10
    k = []
    if y:
        k += ([] if y == 1 else [_BIR[y]]) + ["yüz"]
    if o:
        k.append(_ON[o])
    if b:
        k.append(_BIR[b])
    return k


def sayi_yaziya(n):
    if type(n) is not int:
        raise TypeError("int bekleniyor")
    if abs(n) >= 10**15:
        raise ValueError("aralık dışı")
    if n == 0:
        return "sıfır"
    if n < 0:
        return "eksi " + sayi_yaziya(-n)
    k, i = [], 0
    while n:
        g = n % 1000
        if g:
            parca = [] if (i == 1 and g == 1) else _uc(g)
            k = parca + ([_BASAMAK[i]] if i else []) + k
        n //= 1000
        i += 1
    return " ".join(k)
