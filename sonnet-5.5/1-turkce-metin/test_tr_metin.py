import pytest

from tr_metin import buyuk, kucuk, slug, sayi_yaziya


def test_buyuk():
    assert buyuk("istanbul ılık") == "İSTANBUL ILIK"
    assert buyuk("çğöşü abc") == "ÇĞÖŞÜ ABC"
    assert buyuk("") == ""


def test_kucuk():
    assert kucuk("IĞDIR İZMİR") == "ığdır izmir"
    assert kucuk("ÇĞÖŞÜ ABC") == "çğöşü abc"
    assert "̇" not in kucuk("İ")


def test_slug():
    assert slug("  Çok Güzel Şarkı: İyi ki Doğdun!  ") == "cok-guzel-sarki-iyi-ki-dogdun"
    assert slug("IŞIK") == "isik"
    assert slug("a---b__c") == "a-b-c"
    assert slug("Sayı 42") == "sayi-42"
    assert slug("!!!") == ""
    assert slug("") == ""


DOKUZ = "dokuz yüz doksan dokuz"


@pytest.mark.parametrize("n,beklenen", [
    (0, "sıfır"), (1, "bir"), (10, "on"), (11, "on bir"), (21, "yirmi bir"),
    (100, "yüz"), (101, "yüz bir"), (110, "yüz on"), (200, "iki yüz"),
    (999, DOKUZ),
    (1000, "bin"), (1001, "bin bir"), (2000, "iki bin"), (11_000, "on bir bin"),
    (100_000, "yüz bin"), (101_000, "yüz bir bin"),
    (1_000_000, "bir milyon"), (1_001_000, "bir milyon bin"),
    (1_250_003, "bir milyon iki yüz elli bin üç"),
    (1_000_000_000, "bir milyar"), (10**12, "bir trilyon"),
    (-1001, "eksi bin bir"), (-1, "eksi bir"),
    (10**15 - 1, f"{DOKUZ} trilyon {DOKUZ} milyar {DOKUZ} milyon {DOKUZ} bin {DOKUZ}"),
])
def test_sayi_yaziya(n, beklenen):
    assert sayi_yaziya(n) == beklenen


@pytest.mark.parametrize("n", [10**15, -(10**15), 10**20])
def test_aralik_disi(n):
    with pytest.raises(ValueError):
        sayi_yaziya(n)


@pytest.mark.parametrize("n", [True, False, 1.0, "5", None, 2.5])
def test_tip_hatasi(n):
    with pytest.raises(TypeError):
        sayi_yaziya(n)
