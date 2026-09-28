"""Mayın tarlası — sözleşme ve oyun kuralları için otomatik testler.

Çalıştırma:  python3 -m pytest
Gereken:     pip install playwright  &&  playwright install chromium
"""

import pathlib
import random

import pytest
from playwright.sync_api import sync_playwright

DOSYA = "index.html"
BOYUT = 9
MAYIN_SAYISI = 10
KOMSU = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


@pytest.fixture(scope="module")
def sayfa():
    with sync_playwright() as p:
        tarayici = p.chromium.launch()
        sayfa = tarayici.new_page()
        sayfa.goto(pathlib.Path(DOSYA).resolve().as_uri())
        yield sayfa
        tarayici.close()


@pytest.fixture
def tahta(sayfa):
    """Her test için temiz bir oyun."""
    sayfa.click("#yeni")
    return sayfa


def hucre(sayfa, r, c):
    return sayfa.locator(f'.hucre[data-r="{r}"][data-c="{c}"]')


def mayinlar(sayfa):
    return sayfa.evaluate("window.mayinKonumlari()")


def komsu_sayisi(mayin_listesi, r, c):
    return sum(1 for mr, mc in mayin_listesi
               if abs(mr - r) <= 1 and abs(mc - c) <= 1 and (mr, mc) != (r, c))


def hucre_durumu(sayfa, r, c):
    el = hucre(sayfa, r, c)
    return el.get_attribute("class"), (el.text_content() or "").strip()


def hucreleri_okur(sayfa):
    return {(r, c): hucre_durumu(sayfa, r, c)
            for r in range(BOYUT) for c in range(BOYUT)}


# --- sözleşme ---------------------------------------------------------------

def test_tahta_9x9_ve_koordinatlar(tahta):
    assert tahta.locator(".hucre").count() == BOYUT * BOYUT
    hucreler = tahta.locator(".hucre").all()
    koordinatlar = {(int(h.get_attribute("data-r")), int(h.get_attribute("data-c"))) for h in hucreler}
    assert koordinatlar == {(r, c) for r in range(BOYUT) for c in range(BOYUT)}


def test_mayin_konumlari_ilk_tikt_once_null(tahta):
    assert mayinlar(tahta) is None
    hucre(tahta, 4, 4).click()
    konum = mayinlar(tahta)
    assert isinstance(konum, list) and len(konum) == MAYIN_SAYISI
    assert len({tuple(p) for p in konum}) == MAYIN_SAYISI
    for r, c in konum:
        assert 0 <= r < BOYUT and 0 <= c < BOYUT


def test_yeni_butonu_sifirlar(tahta):
    hucre(tahta, 2, 2).click()
    assert mayinlar(tahta) is not None
    tahta.click("#yeni")
    assert mayinlar(tahta) is None
    durum = tahta.inner_text("#durum")
    assert "Kazandın" not in durum and "Kaybettin" not in durum
    for r in range(BOYUT):
        for c in range(BOYUT):
            sinif, metin = hucre_durumu(tahta, r, c)
            assert "acik" not in sinif and "bayrak" not in sinif
            assert metin == ""


# --- kurallar ---------------------------------------------------------------

@pytest.mark.parametrize("r,c", [(0, 0), (0, 8), (8, 0), (8, 8), (0, 4), (4, 0), (4, 4), (3, 7), (7, 2)])
def test_ilk_tiklamada_ve_komsularinda_mayin_yok(tahta, r, c):
    hucre(tahta, r, c).click()
    konum = set(map(tuple, mayinlar(tahta)))
    guvenli = {(r + dy, c + dx) for dy, dx in KOMSU} | {(r, c)}
    guvenli = {(y, x) for y, x in guvenli if 0 <= y < BOYUT and 0 <= x < BOYUT}
    assert not (konum & guvenli)


def test_acilan_hucre_komsu_mayin_sayisini_gosterir(tahta):
    hucre(tahta, 4, 4).click()
    konum = mayinlar(tahta)
    for r in range(BOYUT):
        for c in range(BOYUT):
            sinif, metin = hucre_durumu(tahta, r, c)
            if "acik" not in sinif:
                continue
            beklenen = komsu_sayisi(konum, r, c)
            if beklenen == 0:
                assert metin == "", f"({r},{c}) 0 hücre boş olmalı, {metin!r} bulundu"
            else:
                assert metin == str(beklenen), f"({r},{c}) {beklenen} bekleniyordu, {metin!r} bulundu"
                assert f"n{beklenen}" in sinif


def test_sifir_komsulu_hucre_komsularini_zincirleme_acar(tahta):
    # Bazı tahtalarda ilk tıklamanın zincirleme açılışı bütün 0 hücreleri zaten açar;
    # o zaman kapalı bir 0 hücre bulmak için yeni oyun denenir.
    for _ in range(20):
        hucre(tahta, 4, 4).click()
        konum = mayinlar(tahta)
        kutu = set(map(tuple, konum))
        kapali_sifir = [(r, c) for r in range(BOYUT) for c in range(BOYUT)
                        if (r, c) not in kutu and komsu_sayisi(konum, r, c) == 0
                        and "acik" not in hucre_durumu(tahta, r, c)[0]]
        if kapali_sifir:
            break
        tahta.click("#yeni")
    assert kapali_sifir, "20 denemede kapalı 0 hücre bulunamadı"
    r, c = kapali_sifir[0]
    hucre(tahta, r, c).click()
    for dy, dx in KOMSU:
        y, x = r + dy, c + dx
        if not (0 <= y < BOYUT and 0 <= x < BOYUT):
            continue
        sinif, _ = hucre_durumu(tahta, y, x)
        if (y, x) in kutu:
            assert "acik" not in sinif, f"zincirleme açılış mayını ({y},{x}) açmamalı"
        else:
            assert "acik" in sinif, f"zincirleme açılışta ({y},{x}) açık olmalı"


def test_sag_tik_bayrak_koyar_kaldirir_ve_sol_tik_acmaz(tahta):
    hucre(tahta, 3, 3).click()
    konum = set(map(tuple, mayinlar(tahta)))
    aday = [(r, c) for r in range(BOYUT) for c in range(BOYUT)
            if (r, c) not in konum and "acik" not in hucre_durumu(tahta, r, c)[0]]
    assert aday
    r, c = aday[0]
    el = hucre(tahta, r, c)
    el.click(button="right")
    sinif, metin = hucre_durumu(tahta, r, c)
    assert "bayrak" in sinif and "acik" not in sinif
    assert metin != ""
    el.click()  # bayraklı hücre sol tıkla açılmaz
    sinif, _ = hucre_durumu(tahta, r, c)
    assert "bayrak" in sinif and "acik" not in sinif
    el.click(button="right")
    sinif, metin = hucre_durumu(tahta, r, c)
    assert "bayrak" not in sinif and metin == ""


def test_mayina_basmak_kaybettirir_ve_mayinlari_gosterir(tahta):
    hucre(tahta, 0, 0).click()
    konum = set(map(tuple, mayinlar(tahta)))
    r, c = sorted(konum)[0]
    hucre(tahta, r, c).click()
    assert "Kaybettin" in tahta.inner_text("#durum")
    for mr, mc in konum:
        sinif, metin = hucre_durumu(tahta, mr, mc)
        assert "mayin" in sinif, f"({mr},{mc}) mayın olarak gösterilmeliydi"
        assert metin != ""


def test_oyun_bittikten_sonra_tiklamalar_tahtayi_degistirmez(tahta):
    hucre(tahta, 0, 0).click()
    konum = set(map(tuple, mayinlar(tahta)))
    r, c = sorted(konum)[0]
    hucre(tahta, r, c).click()
    assert "Kaybettin" in tahta.inner_text("#durum")
    once = hucreleri_okur(tahta)
    durum_metni = tahta.inner_text("#durum")
    for y in range(BOYUT):
        for x in range(BOYUT):
            hucre(tahta, y, x).click()
            hucre(tahta, y, x).click(button="right")
    assert once == hucreleri_okur(tahta)
    assert tahta.inner_text("#durum") == durum_metni
    assert set(map(tuple, mayinlar(tahta))) == konum


def test_mayinsiz_hucreleri_acmak_kazandirir(tahta):
    hucre(tahta, 4, 4).click()
    konum = mayinlar(tahta)
    for r in range(BOYUT):
        for c in range(BOYUT):
            if (r, c) not in set(map(tuple, konum)):
                hucre(tahta, r, c).click()
    assert "Kazandın" in tahta.inner_text("#durum")
    for r in range(BOYUT):
        for c in range(BOYUT):
            sinif, metin = hucre_durumu(tahta, r, c)
            if (r, c) in set(map(tuple, konum)):
                assert "mayin" in sinif
            else:
                assert "acik" in sinif
                beklenen = komsu_sayisi(konum, r, c)
                assert metin == ("" if beklenen == 0 else str(beklenen))
    once = hucreleri_okur(tahta)
    for r in range(BOYUT):
        for c in range(BOYUT):
            hucre(tahta, r, c).click()
    assert once == hucreleri_okur(tahta)
    assert tahta.locator(".hucre.acik").count() == BOYUT * BOYUT - MAYIN_SAYISI


def test_bayrakli_mayinler_kazanma_durumunda_dogru_isaretlenir(tahta):
    hucre(tahta, 4, 4).click()
    konum = [tuple(p) for p in mayinlar(tahta)]
    for r, c in konum:
        hucre(tahta, r, c).click(button="right")
    assert tahta.inner_text("#mayinSayaci").strip() == "0"
    for r in range(BOYUT):
        for c in range(BOYUT):
            if (r, c) not in set(konum):
                hucre(tahta, r, c).click()
    assert "Kazandın" in tahta.inner_text("#durum")
    for r, c in konum:
        sinif, metin = hucre_durumu(tahta, r, c)
        assert "mayin" in sinif and "bayrak" in sinif


def test_rastgele_oyunlar_kurala_uyar(tahta):
    """20 rastgele oyun: ilk tıklama güvenli, 10 mayın, kazanma durumu tutarlı."""
    for _ in range(20):
        tahta.click("#yeni")
        r, c = random.randrange(BOYUT), random.randrange(BOYUT)
        hucre(tahta, r, c).click()
        konum = mayinlar(tahta)
        assert konum is not None and len(konum) == MAYIN_SAYISI
        kutu = set(map(tuple, konum))
        guvenli = {(r + dy, c + dx) for dy, dx in KOMSU} | {(r, c)}
        assert not (kutu & guvenli)
        for y in range(BOYUT):
            for x in range(BOYUT):
                if (y, x) not in kutu:
                    hucre(tahta, y, x).click()
        assert "Kazandın" in tahta.inner_text("#durum")
        assert tahta.locator(".hucre.acik").count() == BOYUT * BOYUT - MAYIN_SAYISI
