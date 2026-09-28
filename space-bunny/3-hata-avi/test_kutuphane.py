from datetime import date

import pytest

from kutuphane import Kutuphane


@pytest.fixture
def k():
    k = Kutuphane()
    k.uye_ekle(1, "Ayse")
    k.uye_ekle(2, "Mehmet")
    k.kitap_ekle("A", "Dune", 2)
    k.kitap_ekle("B", "Emma", 1)
    k.kitap_ekle("C", "Ulysses", 1)
    k.kitap_ekle("D", "Beloved", 1)
    return k


def test_ayni_kitap_tekrar_eklenince_adet_artar(k):
    k.kitap_ekle("A", "Dune", 3)
    assert k.musait("A") == 5


def test_iade_edilen_kitap_rafa_doner(k):
    k.odunc_ver(1, "B", date(2026, 1, 1))
    assert k.musait("B") == 0
    k.iade_et(1, "B", date(2026, 1, 5))
    assert k.musait("B") == 1


def test_odunc_limiti_uc_kitap(k):
    gun = date(2026, 1, 1)
    for isbn in ["A", "B", "C"]:
        k.odunc_ver(1, isbn, gun)
    with pytest.raises(ValueError):
        k.odunc_ver(1, "D", gun)


def test_son_gun_iade_cezasiz(k):
    k.odunc_ver(1, "A", date(2026, 1, 1))
    assert k.iade_et(1, "A", date(2026, 1, 15)) == 0


def test_bir_gun_gecikme_cezasi(k):
    k.odunc_ver(1, "A", date(2026, 1, 1))
    assert k.iade_et(1, "A", date(2026, 1, 16)) == 2.5


def test_populer_coktan_aza(k):
    gun = date(2026, 1, 1)
    k.odunc_ver(1, "A", gun)
    k.odunc_ver(2, "A", gun)
    k.odunc_ver(1, "C", gun)
    assert k.populer() == [("Dune", 2), ("Ulysses", 1)]


def test_stok_bitince_hata(k):
    k.odunc_ver(1, "B", date(2026, 1, 1))
    with pytest.raises(ValueError):
        k.odunc_ver(2, "B", date(2026, 1, 1))


def test_olmayan_odunc_iade_edilemez(k):
    with pytest.raises(ValueError):
        k.iade_et(1, "A", date(2026, 1, 1))
