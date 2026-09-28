import pathlib
import pytest
from playwright.sync_api import sync_playwright

URL = pathlib.Path(__file__).with_name("index.html").resolve().as_uri()


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture
def page(browser):
    pg = browser.new_page(viewport={"width": 700, "height": 700})
    pg.goto(URL)
    yield pg
    pg.close()


def hucre(pg, r, c):
    return pg.locator(f'[data-r="{r}"][data-c="{c}"]')


def komsu(r, c):
    return [(r + a, c + b) for a in (-1, 0, 1) for b in (-1, 0, 1)
            if (a or b) and 0 <= r + a < 9 and 0 <= c + b < 9]


def test_baslangic(page):
    assert page.locator("[data-r]").count() == 81
    assert page.evaluate("window.mayinKonumlari()") is None


def test_ilk_tiklama_guvenli(page):
    for r, c in [(0, 0), (4, 4), (8, 8), (0, 8), (3, 0)]:
        for _ in range(15):
            page.click("#yeni")
            hucre(page, r, c).click()
            m = {tuple(x) for x in page.evaluate("window.mayinKonumlari()")}
            assert len(m) == 10
            assert (r, c) not in m
            assert not m & set(komsu(r, c))


def test_sayilar_ve_zincir(page):
    page.click("#yeni")
    hucre(page, 4, 4).click()
    m = {tuple(x) for x in page.evaluate("window.mayinKonumlari()")}
    for r in range(9):
        for c in range(9):
            el = hucre(page, r, c)
            if "acik" in (el.get_attribute("class") or ""):
                n = sum(k in m for k in komsu(r, c))
                assert el.inner_text().strip() == (str(n) if n else "")
                if n == 0:
                    for kr, kc in komsu(r, c):
                        assert "acik" in hucre(page, kr, kc).get_attribute("class")


def test_bayrak(page):
    page.click("#yeni")
    hucre(page, 0, 0).click(button="right")
    assert "bayrak" in hucre(page, 0, 0).get_attribute("class")
    hucre(page, 0, 0).click()
    assert "acik" not in hucre(page, 0, 0).get_attribute("class")
    assert page.evaluate("window.mayinKonumlari()") is None
    hucre(page, 0, 0).click(button="right")
    assert "bayrak" not in hucre(page, 0, 0).get_attribute("class")


def test_kaybet(page):
    page.click("#yeni")
    hucre(page, 4, 4).click()
    m = [tuple(x) for x in page.evaluate("window.mayinKonumlari()")]
    hucre(page, *m[0]).click()
    assert "Kaybettin" in page.inner_text("#durum")
    n_acik = page.locator(".acik").count()
    for r in range(9):
        for c in range(9):
            hucre(page, r, c).click(force=True)
            hucre(page, r, c).click(button="right", force=True)
    assert page.locator(".acik").count() == n_acik
    assert page.locator(".bayrak").count() == 0
    assert page.locator(".mayin").count() == 10


def test_kazan_ve_sifirla(page):
    page.click("#yeni")
    hucre(page, 4, 4).click()
    m = {tuple(x) for x in page.evaluate("window.mayinKonumlari()")}
    for r in range(9):
        for c in range(9):
            if (r, c) not in m:
                hucre(page, r, c).click()
    assert "Kazandın" in page.inner_text("#durum")
    assert page.locator(".acik").count() == 71
    page.click("#yeni")
    assert page.evaluate("window.mayinKonumlari()") is None
    assert page.locator(".acik").count() == 0
    assert "Kazandın" not in page.inner_text("#durum")


def test_ekran_goruntusu(page):
    page.click("#yeni")
    hucre(page, 4, 4).click()
    hucre(page, 0, 0).click(button="right")
    page.screenshot(path=str(pathlib.Path(__file__).with_name("ekran.png")))
