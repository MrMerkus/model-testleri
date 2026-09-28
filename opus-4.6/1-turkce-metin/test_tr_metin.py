"""tr_metin modülü için kapsamlı testler."""

import pytest
from tr_metin import buyuk, kucuk, slug, sayi_yaziya


# ━━━━━━━━━━━━━━━  buyuk  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestBuyuk:
    def test_istanbul_ilik(self):
        assert buyuk("istanbul ılık") == "İSTANBUL ILIK"

    def test_zaten_buyuk(self):
        assert buyuk("ABC") == "ABC"

    def test_karisik(self):
        assert buyuk("çiçek") == "ÇİÇEK"

    def test_bos(self):
        assert buyuk("") == ""

    def test_rakam_ve_noktalama(self):
        assert buyuk("izmir 35!") == "İZMİR 35!"

    def test_i_ve_I_farki(self):
        # 'i' → 'İ', 'ı' → 'I'
        assert buyuk("iıiı") == "İIİI"


# ━━━━━━━━━━━━━━━  kucuk  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestKucuk:
    def test_igdir_izmir(self):
        assert kucuk("IĞDIR İZMİR") == "ığdır izmir"

    def test_zaten_kucuk(self):
        assert kucuk("abc") == "abc"

    def test_bos(self):
        assert kucuk("") == ""

    def test_I_ve_İ_farki(self):
        # 'I' → 'ı', 'İ' → 'i'
        assert kucuk("IİIİ") == "ıiıi"

    def test_karisik_turkce(self):
        assert kucuk("ŞÜKRÜ ÇELİK") == "şükrü çelik"


# ━━━━━━━━━━━━━━━  slug  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestSlug:
    def test_ornek(self):
        assert slug("  Çok Güzel Şarkı: İyi ki Doğdun!  ") == "cok-guzel-sarki-iyi-ki-dogdun"

    def test_bos_sonuc(self):
        assert slug("!!!") == ""

    def test_rakamlar(self):
        assert slug("2024 Yılı") == "2024-yili"

    def test_art_arda_ozel_karakter(self):
        assert slug("a---b   c") == "a-b-c"

    def test_turkce_harfler(self):
        assert slug("Öğrenci Şöleni Üçüncü") == "ogrenci-soleni-ucuncu"

    def test_buyuk_I_ve_İ(self):
        assert slug("IĞDIR İSTANBUL") == "igdir-istanbul"


# ━━━━━━━━━━━━━━━  sayi_yaziya  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestSayiYaziya:
    # --- Temel değerler ---
    def test_sifir(self):
        assert sayi_yaziya(0) == "sıfır"

    def test_bir(self):
        assert sayi_yaziya(1) == "bir"

    def test_on(self):
        assert sayi_yaziya(10) == "on"

    def test_yuz(self):
        assert sayi_yaziya(100) == "yüz"

    def test_bin(self):
        assert sayi_yaziya(1000) == "bin"

    def test_bir_milyon(self):
        assert sayi_yaziya(1_000_000) == "bir milyon"

    # --- Örnekler (EMIR.md) ---
    def test_ornek_1(self):
        assert sayi_yaziya(1_250_003) == "bir milyon iki yüz elli bin üç"

    def test_ornek_negatif(self):
        assert sayi_yaziya(-1001) == "eksi bin bir"

    # --- Çeşitli sayılar ---
    def test_11(self):
        assert sayi_yaziya(11) == "on bir"

    def test_99(self):
        assert sayi_yaziya(99) == "doksan dokuz"

    def test_101(self):
        assert sayi_yaziya(101) == "yüz bir"

    def test_200(self):
        assert sayi_yaziya(200) == "iki yüz"

    def test_999(self):
        assert sayi_yaziya(999) == "dokuz yüz doksan dokuz"

    def test_1001(self):
        assert sayi_yaziya(1001) == "bin bir"

    def test_2000(self):
        assert sayi_yaziya(2000) == "iki bin"

    def test_10_000(self):
        assert sayi_yaziya(10_000) == "on bin"

    def test_100_000(self):
        assert sayi_yaziya(100_000) == "yüz bin"

    def test_1_000_001(self):
        assert sayi_yaziya(1_000_001) == "bir milyon bir"

    def test_bir_milyar(self):
        assert sayi_yaziya(1_000_000_000) == "bir milyar"

    def test_bir_trilyon(self):
        assert sayi_yaziya(1_000_000_000_000) == "bir trilyon"

    def test_negatif_42(self):
        assert sayi_yaziya(-42) == "eksi kırk iki"

    def test_buyuk_sayi(self):
        # 999_999_999_999_999 (10^15 - 1, sınırdaki son geçerli sayı)
        sonuc = sayi_yaziya(999_999_999_999_999)
        assert "trilyon" in sonuc
        assert "milyar" in sonuc

    # --- Hata durumları ---
    def test_type_error_float(self):
        with pytest.raises(TypeError):
            sayi_yaziya(3.14)

    def test_type_error_bool(self):
        with pytest.raises(TypeError):
            sayi_yaziya(True)

    def test_type_error_str(self):
        with pytest.raises(TypeError):
            sayi_yaziya("42")

    def test_value_error_buyuk(self):
        with pytest.raises(ValueError):
            sayi_yaziya(10**15)

    def test_value_error_negatif_buyuk(self):
        with pytest.raises(ValueError):
            sayi_yaziya(-(10**15))
