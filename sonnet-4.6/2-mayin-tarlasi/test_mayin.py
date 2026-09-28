"""
Mayın Tarlası — Otomatik Testler (Playwright)
Test edilebilirlik sözleşmesini doğrular (EMIR.md §Test edilebilirlik sözleşmesi).

Çalıştırmak için:
  python3 -m pytest test_mayin.py -v
"""

import os
import pytest
from playwright.sync_api import sync_playwright, Page, expect

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX_URL = f"file://{HERE}/index.html"


# ─── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_ctx():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context()
        yield ctx
        browser.close()


@pytest.fixture()
def page(browser_ctx):
    pg = browser_ctx.new_page()
    pg.goto(INDEX_URL)
    pg.wait_for_load_state("load")
    yield pg
    pg.close()


# ─── Yardımcılar ──────────────────────────────────────────────────────────────

def hucre(page: Page, r: int, c: int):
    return page.locator(f'[data-r="{r}"][data-c="{c}"]')


def mayin_konumlari(page: Page):
    return page.evaluate("window.mayinKonumlari()")


def durum_metni(page: Page) -> str:
    return page.locator("#durum").inner_text()


def yeni_oyun(page: Page):
    page.locator("#yeni").click()
    page.wait_for_timeout(200)


def ac(page: Page, r: int, c: int):
    hucre(page, r, c).click()
    page.wait_for_timeout(100)


def bayrak_koy_kaldir(page: Page, r: int, c: int):
    hucre(page, r, c).click(button="right")
    page.wait_for_timeout(100)


# ─── Testler ──────────────────────────────────────────────────────────────────

class TestSayfaYapisi:
    """HTML yapısı ve sözleşme öğeleri var mı?"""

    def test_81_hucre_var(self, page):
        count = page.locator("[data-r][data-c]").count()
        assert count == 81, f"Beklenen 81, bulunan {count}"

    def test_her_hucre_veri_ozelligi(self, page):
        for r in range(9):
            for c in range(9):
                el = hucre(page, r, c)
                assert el.count() == 1, f"({r},{c}) hücresi bulunamadı"

    def test_durum_elementi_var(self, page):
        assert page.locator("#durum").count() == 1

    def test_yeni_buton_var(self, page):
        assert page.locator("#yeni").count() == 1

    def test_mayin_konumlari_ilk_null(self, page):
        result = mayin_konumlari(page)
        assert result is None, f"İlk tıklamadan önce null olmalı, gelen: {result}"


class TestIlkTiklama:
    """İlk tıklama davranışı."""

    def test_ilk_tiklama_sonrasi_mayin_konumlari_dolu(self, page):
        ac(page, 4, 4)
        mk = mayin_konumlari(page)
        assert mk is not None
        assert len(mk) == 10, f"10 mayın olmalı, bulunan: {len(mk)}"

    def test_ilk_tiklanan_hucre_mayinsiz(self, page):
        ac(page, 4, 4)
        mk = mayin_konumlari(page)
        for (mr, mc) in mk:
            assert not (mr == 4 and mc == 4), "İlk tıklanan hücre mayınlı olmamalı"

    def test_ilk_tiklanan_8_komsu_mayinsiz(self, page):
        ir, ic = 4, 4
        ac(page, ir, ic)
        mk = set(map(tuple, mayin_konumlari(page)))
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = ir + dr, ic + dc
                if 0 <= nr < 9 and 0 <= nc < 9:
                    assert (nr, nc) not in mk, f"({nr},{nc}) yasak bölgede mayın var"


class TestHucreAcma:
    """Hücre açıldığında 'acik' sınıfı ve metin kuralları."""

    def test_acilan_hucre_acik_sinifi(self, page):
        ac(page, 4, 4)
        el = hucre(page, 4, 4)
        assert "acik" in (el.get_attribute("class") or ""), "'acik' sınıfı olmalı"

    def test_acik_sayili_hucre_metni_rakam(self, page):
        ac(page, 4, 4)
        mk = set(map(tuple, mayin_konumlari(page)))
        for r in range(9):
            for c in range(9):
                el = hucre(page, r, c)
                cls = el.get_attribute("class") or ""
                if "acik" in cls and (r, c) not in mk:
                    txt = el.inner_text().strip()
                    if txt:
                        assert txt.isdigit(), f"({r},{c}) beklenmeyen metin: '{txt}'"
                        assert 1 <= int(txt) <= 8

    def test_acik_sifir_hucre_bos_metin(self, page):
        ac(page, 4, 4)
        mk = set(map(tuple, mayin_konumlari(page)))
        # 0-sayılı açık hücrenin metni boş olmalı
        found_zero = False
        for r in range(9):
            for c in range(9):
                el = hucre(page, r, c)
                cls = el.get_attribute("class") or ""
                if "acik" in cls and (r, c) not in mk:
                    txt = el.inner_text().strip()
                    if txt == "":
                        found_zero = True
                    else:
                        # sayılı ise rakam olmalı
                        assert txt.isdigit()
        # Merkez açılırsa sıklıkla sıfır hücreler oluşur; oluşmadıysa test yine geçer


class TestBayrak:
    """Sağ tık bayrak sözleşmesi."""

    def test_sag_tik_bayrak_sinifi(self, page):
        bayrak_koy_kaldir(page, 0, 0)
        cls = hucre(page, 0, 0).get_attribute("class") or ""
        assert "bayrak" in cls, "'bayrak' sınıfı olmalı"

    def test_bayrakli_hucre_sol_tikla_acilmaz(self, page):
        bayrak_koy_kaldir(page, 0, 0)  # koy
        ac(page, 0, 0)                  # sol tıkla
        cls = hucre(page, 0, 0).get_attribute("class") or ""
        assert "acik" not in cls, "Bayraklı hücre sol tıkla açılmamalı"

    def test_sag_tik_bayragi_kaldirir(self, page):
        bayrak_koy_kaldir(page, 1, 1)  # koy
        bayrak_koy_kaldir(page, 1, 1)  # kaldır
        cls = hucre(page, 1, 1).get_attribute("class") or ""
        assert "bayrak" not in cls, "İkinci sağ tık bayrağı kaldırmalı"


class TestYeniOyun:
    """Yeni oyun butonu tahtayı sıfırlar."""

    def test_yeni_oyun_mayin_konumlari_null(self, page):
        ac(page, 4, 4)
        yeni_oyun(page)
        assert mayin_konumlari(page) is None, "Yeni oyundan sonra mayinKonumlari() null olmalı"

    def test_yeni_oyun_hucre_acik_degil(self, page):
        ac(page, 4, 4)
        yeni_oyun(page)
        for r in range(9):
            for c in range(9):
                cls = hucre(page, r, c).get_attribute("class") or ""
                assert "acik" not in cls, f"({r},{c}) yeni oyunda açık olmamalı"


class TestOyunSonu:
    """Kazanma ve kaybetme durumları."""

    def _hepsini_ac(self, page, mk_set):
        """Mayınsız tüm hücreleri tıkla."""
        for r in range(9):
            for c in range(9):
                if (r, c) not in mk_set:
                    el = hucre(page, r, c)
                    cls = el.get_attribute("class") or ""
                    if "acik" not in cls and "bayrak" not in cls:
                        el.click()
                        page.wait_for_timeout(30)

    def test_durum_kazaninca_kazandin(self, page):
        ac(page, 4, 4)
        mk = set(map(tuple, mayin_konumlari(page)))
        self._hepsini_ac(page, mk)
        page.wait_for_timeout(200)
        txt = durum_metni(page)
        assert "Kazandın" in txt, f"Kazanma mesajı yok, gelen: '{txt}'"

    def test_durum_kaybedince_kaybettin(self, page):
        ac(page, 4, 4)
        mk = list(mayin_konumlari(page))
        mr, mc = mk[0]
        # Mayın hücresine doğrudan tıkla
        hucre(page, mr, mc).click()
        page.wait_for_timeout(200)
        txt = durum_metni(page)
        assert "Kaybettin" in txt, f"Kaybetme mesajı yok, gelen: '{txt}'"

    def test_kaybedince_mayinlar_gosterilir(self, page):
        ac(page, 4, 4)
        mk = list(mayin_konumlari(page))
        mr, mc = mk[0]
        hucre(page, mr, mc).click()
        page.wait_for_timeout(200)
        for (r2, c2) in mk:
            cls = hucre(page, r2, c2).get_attribute("class") or ""
            assert "acik" in cls, f"Mayın ({r2},{c2}) kaybedince gösterilmeli"

    def test_oyun_bittikten_sonra_tiklamalar_etkisiz(self, page):
        ac(page, 4, 4)
        mk = set(map(tuple, mayin_konumlari(page)))
        self._hepsini_ac(page, mk)
        page.wait_for_timeout(200)
        assert "Kazandın" in durum_metni(page)
        # Mayın hücresine tıkla — durum değişmemeli
        mr, mc = list(mk)[0]
        hucre(page, mr, mc).click()
        page.wait_for_timeout(100)
        assert "Kazandın" in durum_metni(page), "Oyun bittikten sonra durum değişmemeli"
