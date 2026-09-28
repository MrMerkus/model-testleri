"""Görev 1 gizli testleri. Her test bir puan."""
import pytest

from tr_metin import buyuk, kucuk, sayi_yaziya, slug


# --- büyük / küçük harf ---
def test_buyuk_ornek():
    assert buyuk("istanbul ılık") == "İSTANBUL ILIK"

def test_kucuk_ornek():
    assert kucuk("IĞDIR İZMİR") == "ığdır izmir"

def test_buyuk_diger_harfler():
    assert buyuk("çğöşü abc") == "ÇĞÖŞÜ ABC"

def test_kucuk_diger_harfler():
    assert kucuk("ÇĞÖŞÜ ABC") == "çğöşü abc"

def test_gidis_donus():
    assert kucuk(buyuk("ıiIİ")) == "ıiıi"

def test_buyuk_bos():
    assert buyuk("") == ""

def test_kucuk_birlesik_nokta_yok():
    # "İ".lower() Python'da "i̇" (iki karakter) verir; Türkçe kurala göre tek "i" olmalı.
    assert len(kucuk("İ")) == 1


# --- slug ---
def test_slug_ornek():
    assert slug("  Çok Güzel Şarkı: İyi ki Doğdun!  ") == "cok-guzel-sarki-iyi-ki-dogdun"

def test_slug_buyuk_I():
    assert slug("IRMAK") == "irmak"

def test_slug_ardisik_isaretler():
    assert slug("a -- b __ c!!") == "a-b-c"

def test_slug_rakam():
    assert slug("2026 Yılı Raporu v2") == "2026-yili-raporu-v2"

def test_slug_bos_sonuc():
    assert slug("!!! ??? ...") == ""

def test_slug_bos_girdi():
    assert slug("") == ""


# --- sayı yazıya ---
@pytest.mark.parametrize("n, beklenen", [
    (0, "sıfır"),
    (1, "bir"),
    (10, "on"),
    (11, "on bir"),
    (99, "doksan dokuz"),
    (100, "yüz"),
    (101, "yüz bir"),
    (200, "iki yüz"),
    (999, "dokuz yüz doksan dokuz"),
    (1000, "bin"),
    (1001, "bin bir"),
    (1100, "bin yüz"),
    (2000, "iki bin"),
    (10_000, "on bin"),
    (11_000, "on bir bin"),
    (100_000, "yüz bin"),
    (101_000, "yüz bir bin"),
    (1_000_000, "bir milyon"),
    (1_001_000, "bir milyon bin"),
    (1_250_003, "bir milyon iki yüz elli bin üç"),
    (1_000_000_000, "bir milyar"),
    (1_000_000_000_000, "bir trilyon"),
    (999_999_999_999_999, "dokuz yüz doksan dokuz trilyon dokuz yüz doksan dokuz milyar "
                          "dokuz yüz doksan dokuz milyon dokuz yüz doksan dokuz bin "
                          "dokuz yüz doksan dokuz"),
    (-1001, "eksi bin bir"),
    (-7, "eksi yedi"),
])
def test_sayi(n, beklenen):
    assert sayi_yaziya(n) == beklenen

def test_sayi_ust_sinir():
    with pytest.raises(ValueError):
        sayi_yaziya(10**15)

def test_sayi_alt_sinir():
    with pytest.raises(ValueError):
        sayi_yaziya(-(10**15))

def test_sayi_float():
    with pytest.raises(TypeError):
        sayi_yaziya(3.0)

def test_sayi_bool():
    with pytest.raises(TypeError):
        sayi_yaziya(True)

def test_sayi_str():
    with pytest.raises(TypeError):
        sayi_yaziya("5")
