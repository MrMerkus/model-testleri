"""Görev 3 gizli testleri: düzeltmenin kökten mi, teste özel mi yapıldığını sınar."""
from datetime import date

import pytest

from kutuphane import Kutuphane


def yeni():
    k = Kutuphane()
    for i in range(1, 4):
        k.uye_ekle(i, f"Uye{i}")
    return k


def test_g1_farkli_isbn_ile_adet_birikir():
    k = yeni()
    k.kitap_ekle("X9", "Kitap", 1)
    k.kitap_ekle("X9", "Kitap", 1)
    k.kitap_ekle("X9", "Kitap", 4)
    assert k.musait("X9") == 6


def test_g1_ilk_ekleme_bozulmadi():
    k = yeni()
    k.kitap_ekle("Q", "Kitap", 7)
    assert k.musait("Q") == 7


def test_g2_iade_sonrasi_tekrar_odunc():
    k = yeni()
    k.kitap_ekle("Z", "Zeta", 1)
    for gun in range(1, 6):
        k.odunc_ver(1, "Z", date(2026, 3, gun))
        k.iade_et(1, "Z", date(2026, 3, gun))
    assert k.musait("Z") == 1


def test_g2_kismi_iade():
    k = yeni()
    k.kitap_ekle("M", "Mu", 3)
    k.odunc_ver(1, "M", date(2026, 3, 1))
    k.odunc_ver(2, "M", date(2026, 3, 1))
    k.iade_et(1, "M", date(2026, 3, 2))
    assert k.musait("M") == 2


def test_g3_limit_iadeden_sonra_acilir():
    k = yeni()
    for isbn in "PRST":
        k.kitap_ekle(isbn, isbn, 1)
    g = date(2026, 5, 1)
    for isbn in "PRS":
        k.odunc_ver(3, isbn, g)
    with pytest.raises(ValueError):
        k.odunc_ver(3, "T", g)
    k.iade_et(3, "P", g)
    k.odunc_ver(3, "T", g)
    assert len(k.aktif_odunc(3)) == 3


def test_g3_iki_kitap_serbest():
    k = yeni()
    k.kitap_ekle("P", "P", 1)
    k.kitap_ekle("R", "R", 1)
    g = date(2026, 5, 1)
    k.odunc_ver(2, "P", g)
    k.odunc_ver(2, "R", g)
    assert len(k.aktif_odunc(2)) == 2


def test_g4_son_tarih_ay_donumu():
    k = yeni()
    assert k.son_tarih(date(2026, 2, 20)) == date(2026, 3, 6)


def test_g4_on_gun_gecikme():
    k = yeni()
    k.kitap_ekle("L", "L", 1)
    k.odunc_ver(1, "L", date(2026, 6, 10))
    assert k.iade_et(1, "L", date(2026, 7, 4)) == 25.0


def test_g4_erken_iade_cezasiz():
    k = yeni()
    k.kitap_ekle("L", "L", 1)
    k.odunc_ver(1, "L", date(2026, 6, 10))
    assert k.iade_et(1, "L", date(2026, 6, 11)) == 0


def test_g5_esitlikte_alfabetik():
    k = yeni()
    for isbn, ad in [("1", "Zorba"), ("2", "Anna"), ("3", "Mira"), ("4", "Kafka")]:
        k.kitap_ekle(isbn, ad, 5)
    g = date(2026, 1, 1)
    for uye, isbn in [(1, "1"), (2, "1"), (1, "2"), (2, "3"), (3, "2"), (3, "1"), (3, "4")]:
        k.odunc_ver(uye, isbn, g)
    assert k.populer() == [("Zorba", 3), ("Anna", 2), ("Kafka", 1), ("Mira", 1)]


def test_g5_bos_liste():
    assert yeni().populer() == []
