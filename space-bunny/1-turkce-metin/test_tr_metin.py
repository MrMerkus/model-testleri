import pytest

from tr_metin import buyuk, kucuk, sayi_yaziya, slug


@pytest.mark.parametrize(
    "girdi, beklenen",
    [
        ("istanbul ılık", "İSTANBUL ILIK"),
        ("IĞDIR İZMİR", "IĞDIR İZMİR"),
        ("şeker Ğ", "ŞEKER Ğ"),
        ("", ""),
        ("abc def", "ABC DEF"),
    ],
)
def test_buyuk(girdi, beklenen):
    assert buyuk(girdi) == beklenen


@pytest.mark.parametrize(
    "girdi, beklenen",
    [
        ("IĞDIR İZMİR", "ığdır izmir"),
        ("İSTANBUL ILIK", "istanbul ılık"),
        ("Şeker Ğ", "şeker ğ"),
        ("", ""),
        ("ABC Def", "abc def"),
    ],
)
def test_kucuk(girdi, beklenen):
    assert kucuk(girdi) == beklenen


def test_buyuk_kucuk_gidis_donus():
    metin = "İstanbul ılık şarkı güğüm ÇğıÖŞÜÖ"
    assert kucuk(buyuk(metin)) == kucuk(metin)
    assert buyuk(kucuk(metin)) == buyuk(metin)


@pytest.mark.parametrize(
    "girdi, beklenen",
    [
        ("  Çok Güzel Şarkı: İyi ki Doğdun!  ", "cok-guzel-sarki-iyi-ki-dogdun"),
        ("İstanbul", "istanbul"),
        ("  IŞIK  ", "isik"),
        ("a   b", "a-b"),
        ("---merhaba---", "merhaba"),
        ("2026 yılı", "2026-yili"),
        ("!!!", ""),
        ("", ""),
        ("   ", ""),
        ("Ç Ğ İ Ö Ş Ü çğıöşü", "c-g-i-o-s-u-cgiosu"),
        ("Sayı 42! -- deneme", "sayi-42-deneme"),
    ],
)
def test_slug(girdi, beklenen):
    assert slug(girdi) == beklenen


def test_slug_turk_harfleri_yok():
    assert not set("çğıöşüÇĞİÖŞÜ") & set(slug("Çok Güzel Şarkı: İyi ki Doğdun!"))


def test_slug_yalnizca_guvenli_karakterler():
    sonuc = slug("Yazılım & Geliştirme #2026!")
    assert all(k.isalnum() and k.isascii() or k == "-" for k in sonuc)


@pytest.mark.parametrize(
    "n, beklenen",
    [
        (0, "sıfır"),
        (1, "bir"),
        (10, "on"),
        (11, "on bir"),
        (19, "on dokuz"),
        (20, "yirmi"),
        (30, "otuz"),
        (99, "doksan dokuz"),
        (100, "yüz"),
        (101, "yüz bir"),
        (110, "yüz on"),
        (999, "dokuz yüz doksan dokuz"),
        (1000, "bin"),
        (1001, "bin bir"),
        (1_250_003, "bir milyon iki yüz elli bin üç"),
        (-1001, "eksi bin bir"),
        (-1, "eksi bir"),
        (1_000_000, "bir milyon"),
        (1_000_000_000, "bir milyar"),
        (1_000_000_000_000, "bir trilyon"),
        (2_000_000, "iki milyon"),
        (1_000_001_000, "bir milyar bir"),
        (999_999_999_999_999, "dokuz yüz doksan dokuz trilyon dokuz yüz doksan dokuz milyar "
                              "dokuz yüz doksan dokuz milyon dokuz yüz doksan dokuz bin "
                              "dokuz yüz doksan dokuz"),
    ],
)
def test_sayi_yaziya(n, beklenen):
    assert sayi_yaziya(n) == beklenen


@pytest.mark.parametrize("n", [True, False, 1.0, 2.5, "5", None, [1], 1 + 0j])
def test_sayi_yaziya_tip_hatasi(n):
    with pytest.raises(TypeError):
        sayi_yaziya(n)
