"""
test_tr_metin.py — tr_metin modülü için pytest testleri
"""

import pytest
from tr_metin import buyuk, kucuk, slug, sayi_yaziya


# ---------------------------------------------------------------------------
# buyuk() testleri
# ---------------------------------------------------------------------------

class TestBuyuk:
    def test_temel_ornek(self):
        assert buyuk("istanbul ılık") == "İSTANBUL ILIK"

    def test_karisik(self):
        assert buyuk("iğdir") == "İĞDİR"

    def test_bos_metin(self):
        assert buyuk("") == ""

    def test_sadece_buyuk(self):
        # Zaten büyük olan harfler değişmemeli
        assert buyuk("ABC") == "ABC"

    def test_i_donusumu(self):
        assert buyuk("i") == "İ"

    def test_i_noktas_z_donusum(self):
        assert buyuk("ı") == "I"

    def test_rakam_ve_harf(self):
        assert buyuk("abc123") == "ABC123"


# ---------------------------------------------------------------------------
# kucuk() testleri
# ---------------------------------------------------------------------------

class TestKucuk:
    def test_temel_ornek(self):
        assert kucuk("IĞDIR İZMİR") == "ığdır izmir"

    def test_i_donusumu(self):
        assert kucuk("İ") == "i"

    def test_buyuk_i_donusum(self):
        assert kucuk("I") == "ı"

    def test_bos_metin(self):
        assert kucuk("") == ""

    def test_karisik(self):
        assert kucuk("İSTANBUL") == "istanbul"

    def test_rakam_korunur(self):
        assert kucuk("ABC123") == "abc123"


# ---------------------------------------------------------------------------
# slug() testleri
# ---------------------------------------------------------------------------

class TestSlug:
    def test_temel_ornek(self):
        assert slug("  Çok Güzel Şarkı: İyi ki Doğdun!  ") == "cok-guzel-sarki-iyi-ki-dogdun"

    def test_bos_metin(self):
        assert slug("") == ""

    def test_sadece_ozel_karakter(self):
        # Harf veya rakam kalmıyorsa boş dize döner
        assert slug("!!!---...") == ""

    def test_turkce_harfler(self):
        assert slug("çğıöşü") == "cgiosu"

    def test_buyuk_harfler(self):
        assert slug("ISTANBUL") == "istanbul"

    def test_rakamlar(self):
        assert slug("test 123") == "test-123"

    def test_birdenbire_uc_tire(self):
        # Birden fazla özel karakter → tek tire
        assert slug("a---b") == "a-b"

    def test_bas_son_tire_yok(self):
        # Başta ve sonda tire olmamalı
        result = slug("!hello!")
        assert not result.startswith("-")
        assert not result.endswith("-")

    def test_turkce_i_slug(self):
        # İ → i dönüşümü (İ önce küçüğe i'ye, sonra i kalır)
        assert slug("İzmir") == "izmir"


# ---------------------------------------------------------------------------
# sayi_yaziya() testleri
# ---------------------------------------------------------------------------

class TestSayiYaziya:
    def test_sifir(self):
        assert sayi_yaziya(0) == "sıfır"

    def test_birler(self):
        assert sayi_yaziya(1) == "bir"
        assert sayi_yaziya(9) == "dokuz"

    def test_onlar(self):
        assert sayi_yaziya(10) == "on"
        assert sayi_yaziya(20) == "yirmi"
        assert sayi_yaziya(99) == "doksan dokuz"

    def test_yuz(self):
        assert sayi_yaziya(100) == "yüz"

    def test_iki_yuz(self):
        assert sayi_yaziya(200) == "iki yüz"

    def test_bin(self):
        assert sayi_yaziya(1000) == "bin"

    def test_iki_bin(self):
        assert sayi_yaziya(2000) == "iki bin"

    def test_bin_bir(self):
        assert sayi_yaziya(1001) == "bin bir"

    def test_milyon(self):
        assert sayi_yaziya(1_000_000) == "bir milyon"

    def test_karmasik(self):
        assert sayi_yaziya(1_250_003) == "bir milyon iki yüz elli bin üç"

    def test_negatif(self):
        assert sayi_yaziya(-1001) == "eksi bin bir"

    def test_negatif_sifir_degil(self):
        assert sayi_yaziya(-5) == "eksi beş"

    def test_buyuk_sayi(self):
        assert sayi_yaziya(1_000_000_000) == "bir milyar"

    def test_trilyon(self):
        assert sayi_yaziya(1_000_000_000_000) == "bir trilyon"

    def test_karisik_buyuk(self):
        assert sayi_yaziya(2_001_000) == "iki milyon bin"

    def test_sinir_disi_yukari(self):
        with pytest.raises(ValueError):
            sayi_yaziya(10 ** 15)

    def test_sinir_disi_asagi(self):
        with pytest.raises(ValueError):
            sayi_yaziya(-(10 ** 15))

    def test_float_hatasi(self):
        with pytest.raises(TypeError):
            sayi_yaziya(3.14)

    def test_bool_hatasi(self):
        with pytest.raises(TypeError):
            sayi_yaziya(True)

    def test_str_hatasi(self):
        with pytest.raises(TypeError):
            sayi_yaziya("42")

    def test_yuz_elli(self):
        assert sayi_yaziya(150) == "yüz elli"

    def test_on_bes(self):
        assert sayi_yaziya(15) == "on beş"

    def test_sinir_ici_negatif(self):
        # 10**15 - 1 geçerli olmalı
        result = sayi_yaziya(-(10 ** 15 - 1))
        assert result.startswith("eksi")
