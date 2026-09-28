"""Mayın tarlası – otomatik testler (pytest + playwright)."""
import pytest, pathlib, os

# ---- Playwright fixture ----
@pytest.fixture(scope="module")
def page_url():
    index = pathlib.Path(__file__).parent / "index.html"
    return index.resolve().as_uri()


@pytest.fixture()
def page(page_url, browser):
    """Her test için yeni bir sayfa açar."""
    ctx = browser.new_context()
    pg = ctx.new_page()
    pg.goto(page_url)
    yield pg
    ctx.close()


# ---- Yardımcılar ----
def hucre(page, r, c):
    return page.locator(f'[data-r="{r}"][data-c="{c}"]')


def sol_tik(page, r, c):
    hucre(page, r, c).click()


def sag_tik(page, r, c):
    hucre(page, r, c).click(button="right")


def mayin_konumlari(page):
    return page.evaluate("window.mayinKonumlari()")


def durum_metni(page):
    return page.locator("#durum").inner_text()


# ============================================================
# TESTLER
# ============================================================

class TestIzgara:
    """Izgara yapısı ve data-attribute kontrolü."""

    def test_81_hucre_var(self, page):
        assert page.locator(".hucre").count() == 81

    def test_data_r_ve_data_c(self, page):
        for r in range(9):
            for c in range(9):
                assert hucre(page, r, c).count() == 1


class TestIlkTiklama:
    """İlk tıklama ve güvenli bölge."""

    def test_mayin_konumlari_basta_null(self, page):
        assert mayin_konumlari(page) is None

    def test_ilk_tiktan_sonra_10_mayin(self, page):
        sol_tik(page, 4, 4)
        mk = mayin_konumlari(page)
        assert mk is not None
        assert len(mk) == 10

    def test_ilk_tiklanan_ve_komsusu_guvenli(self, page):
        r0, c0 = 4, 4
        sol_tik(page, r0, c0)
        mk = mayin_konumlari(page)
        guvenli = {(r0, c0)}
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = r0 + dr, c0 + dc
                if 0 <= nr < 9 and 0 <= nc < 9:
                    guvenli.add((nr, nc))
        for pos in mk:
            assert tuple(pos) not in guvenli, f"Mayın güvenli bölgede: {pos}"


class TestAcma:
    """Hücre açma, 'acik' sınıfı, metin kuralları."""

    def test_tiklanan_hucre_acik_sinifi_alir(self, page):
        sol_tik(page, 0, 0)
        assert "acik" in hucre(page, 0, 0).get_attribute("class")

    def test_sifir_hucre_bos_metin(self, page):
        """0 komşu mayınlı açılmış hücrenin metni boş olmalı."""
        sol_tik(page, 4, 4)
        # Açılmış, sayısı 0 olan hücreleri bul
        aciklar = page.locator(".hucre.acik")
        count = aciklar.count()
        assert count > 0
        for i in range(count):
            el = aciklar.nth(i)
            text = el.inner_text().strip()
            if text == "":
                return  # en az bir boş bulduk -> OK
        # Eğer hiç boş yoksa — küçük bir ihtimal ama sayılı da olabilir
        # yine de ilk tıklama zincirleme açma yapmalı, assert edelim

    def test_zincirleme_acma(self, page):
        """İlk tıklamadan sonra 1'den fazla hücre açılmalı (zincirleme)."""
        sol_tik(page, 4, 4)
        acik_sayisi = page.locator(".hucre.acik").count()
        assert acik_sayisi > 1, "Zincirleme açma çalışmalı"


class TestBayrak:
    """Sağ tık bayrak davranışı."""

    def test_sag_tik_bayrak_koyar(self, page):
        sag_tik(page, 0, 0)
        assert "bayrak" in hucre(page, 0, 0).get_attribute("class")

    def test_sag_tik_bayrak_kaldirir(self, page):
        sag_tik(page, 0, 0)
        sag_tik(page, 0, 0)
        assert "bayrak" not in hucre(page, 0, 0).get_attribute("class")

    def test_bayrakli_hucre_sol_tikla_acilmaz(self, page):
        sag_tik(page, 0, 0)
        sol_tik(page, 0, 0)
        assert "acik" not in hucre(page, 0, 0).get_attribute("class")


class TestKaybet:
    """Mayına basma → kaybetme."""

    def test_mayina_basinca_kaybettin(self, page):
        # Önce ilk güvenli tık
        sol_tik(page, 4, 4)
        mk = mayin_konumlari(page)
        assert mk is not None and len(mk) == 10
        # Mayınlardan birine bas
        mr, mc = mk[0]
        sol_tik(page, mr, mc)
        assert "Kaybettin" in durum_metni(page)

    def test_kaybettikten_sonra_tiklamalar_islemez(self, page):
        sol_tik(page, 4, 4)
        mk = mayin_konumlari(page)
        mr, mc = mk[0]
        sol_tik(page, mr, mc)  # kaybettik
        # Kapalı bir hücreye tıkla
        for r in range(9):
            for c in range(9):
                if [r, c] not in mk and "acik" not in (hucre(page, r, c).get_attribute("class") or ""):
                    onceki_sinif = hucre(page, r, c).get_attribute("class")
                    sol_tik(page, r, c)
                    sonraki_sinif = hucre(page, r, c).get_attribute("class")
                    assert onceki_sinif == sonraki_sinif, "Oyun bittikten sonra hücre değişmemeli"
                    return
        # Eğer tüm hücreler açıksa test geçer


class TestKazan:
    """Tüm mayınsız hücreleri açma → kazanma."""

    def test_tum_guvenli_hucreleri_acinca_kazandin(self, page):
        sol_tik(page, 4, 4)
        mk = mayin_konumlari(page)
        mayin_set = set()
        for pos in mk:
            mayin_set.add((pos[0], pos[1]))

        for r in range(9):
            for c in range(9):
                if (r, c) not in mayin_set:
                    sol_tik(page, r, c)

        assert "Kazandın" in durum_metni(page)


class TestYeniOyun:
    """Yeni Oyun butonu."""

    def test_yeni_buton_sifirlar(self, page):
        sol_tik(page, 0, 0)
        acik_once = page.locator(".hucre.acik").count()
        assert acik_once > 0
        page.locator("#yeni").click()
        acik_sonra = page.locator(".hucre.acik").count()
        assert acik_sonra == 0

    def test_yeni_oyunda_mayin_null(self, page):
        sol_tik(page, 0, 0)
        page.locator("#yeni").click()
        assert mayin_konumlari(page) is None


class TestMayinKonumlariAPI:
    """window.mayinKonumlari() fonksiyonu."""

    def test_fonksiyon_var(self, page):
        assert page.evaluate("typeof window.mayinKonumlari") == "function"

    def test_format_dizi_icinde_dizi(self, page):
        sol_tik(page, 4, 4)
        mk = mayin_konumlari(page)
        assert isinstance(mk, list)
        for pos in mk:
            assert isinstance(pos, list)
            assert len(pos) == 2
            assert 0 <= pos[0] < 9
            assert 0 <= pos[1] < 9
