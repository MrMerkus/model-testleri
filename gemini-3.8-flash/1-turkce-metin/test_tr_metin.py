"""tr_metin modülü birim testleri."""

import pytest
from tr_metin import buyuk, kucuk, sayi_yaziya, slug


# ---------------------------------------------------------------------------
# buyuk() Testleri
# ---------------------------------------------------------------------------

def test_buyuk_emir_ornek():
    assert buyuk("istanbul ılık") == "İSTANBUL ILIK"


def test_buyuk_temel_ve_turkce_harfler():
    kucuk_harfler = "a b c ç d e f g ğ h ı i j k l m n o ö p r s ş t u ü v y z"
    buyuk_harfler = "A B C Ç D E F G Ğ H I İ J K L M N O Ö P R S Ş T U Ü V Y Z"
    assert buyuk(kucuk_harfler) == buyuk_harfler


def test_buyuk_noktali_ve_noktasiz_i():
    assert buyuk("i") == "İ"
    assert buyuk("ı") == "I"
    assert buyuk("İ") == "İ"
    assert buyuk("I") == "I"
    assert buyuk("iğdır izmir") == "İĞDIR İZMİR"
    assert buyuk("Iğdır İzmir") == "IĞDIR İZMİR"


def test_buyuk_bos_ve_ozel_karakterler():
    assert buyuk("") == ""
    assert buyuk("merhaba 123! nasılsın?") == "MERHABA 123! NASILSIN?"


def test_buyuk_tip_hatasi():
    with pytest.raises(TypeError):
        buyuk(123)  # type: ignore
    with pytest.raises(TypeError):
        buyuk(None)  # type: ignore


# ---------------------------------------------------------------------------
# kucuk() Testleri
# ---------------------------------------------------------------------------

def test_kucuk_emir_ornek():
    assert kucuk("IĞDIR İZMİR") == "ığdır izmir"


def test_kucuk_temel_ve_turkce_harfler():
    kucuk_harfler = "a b c ç d e f g ğ h ı i j k l m n o ö p r s ş t u ü v y z"
    buyuk_harfler = "A B C Ç D E F G Ğ H I İ J K L M N O Ö P R S Ş T U Ü V Y Z"
    assert kucuk(buyuk_harfler) == kucuk_harfler


def test_kucuk_noktali_ve_noktasiz_i():
    assert kucuk("İ") == "i"
    assert kucuk("I") == "ı"
    assert kucuk("i") == "i"
    assert kucuk("ı") == "ı"
    assert kucuk("İSTANBUL ILIK") == "istanbul ılık"
    assert kucuk("İstanbul Ilık") == "istanbul ılık"


def test_kucuk_bos_ve_ozel_karakterler():
    assert kucuk("") == ""
    assert kucuk("DENEME 123! NASILSIN?") == "deneme 123! nasılsın?"


def test_kucuk_tip_hatasi():
    with pytest.raises(TypeError):
        kucuk(123)  # type: ignore
    with pytest.raises(TypeError):
        kucuk(None)  # type: ignore


# ---------------------------------------------------------------------------
# slug() Testleri
# ---------------------------------------------------------------------------

def test_slug_emir_ornek():
    assert slug("  Çok Güzel Şarkı: İyi ki Doğdun!  ") == "cok-guzel-sarki-iyi-ki-dogdun"


def test_slug_turkce_ozel_harfler():
    assert slug("ç ğ ı ö ş ü") == "c-g-i-o-s-u"
    assert slug("Ç Ğ I İ Ö Ş Ü") == "c-g-i-i-o-s-u"


def test_slug_aradaki_ve_kenardaki_isaretler():
    assert slug("---deneme---başlık---") == "deneme-baslik"
    assert slug("haber // başlığı & detaylar") == "haber-basligi-detaylar"
    assert slug("a___b...c---d") == "a-b-c-d"


def test_slug_sayilar_ve_karisik():
    assert slug("Python 3.12 Çıktı!") == "python-3-12-cikti"
    assert slug("123") == "123"
    assert slug("kadıköy 34") == "kadikoy-34"


def test_slug_bos_sonuclar():
    assert slug("") == ""
    assert slug("   ") == ""
    assert slug("!@#$%^&*()") == ""
    assert slug("---") == ""


def test_slug_tip_hatasi():
    with pytest.raises(TypeError):
        slug(123)  # type: ignore
    with pytest.raises(TypeError):
        slug(None)  # type: ignore


# ---------------------------------------------------------------------------
# sayi_yaziya() Testleri
# ---------------------------------------------------------------------------

def test_sayi_yaziya_sifir():
    assert sayi_yaziya(0) == "sıfır"


def test_sayi_yaziya_tek_basamaklilar():
    assert sayi_yaziya(1) == "bir"
    assert sayi_yaziya(2) == "iki"
    assert sayi_yaziya(3) == "üç"
    assert sayi_yaziya(4) == "dört"
    assert sayi_yaziya(5) == "beş"
    assert sayi_yaziya(6) == "altı"
    assert sayi_yaziya(7) == "yedi"
    assert sayi_yaziya(8) == "sekiz"
    assert sayi_yaziya(9) == "dokuz"


def test_sayi_yaziya_onluklar():
    assert sayi_yaziya(10) == "on"
    assert sayi_yaziya(11) == "on bir"
    assert sayi_yaziya(19) == "on dokuz"
    assert sayi_yaziya(20) == "yirmi"
    assert sayi_yaziya(42) == "kırk iki"
    assert sayi_yaziya(99) == "doksan dokuz"


def test_sayi_yaziya_yuzlukler():
    # 100 -> "yüz" (bir yüz değil) kuralı
    assert sayi_yaziya(100) == "yüz"
    assert sayi_yaziya(101) == "yüz bir"
    assert sayi_yaziya(110) == "yüz on"
    assert sayi_yaziya(115) == "yüz on beş"
    assert sayi_yaziya(200) == "iki yüz"
    assert sayi_yaziya(305) == "üç yüz beş"
    assert sayi_yaziya(999) == "dokuz yüz doksan dokuz"


def test_sayi_yaziya_binlikler():
    # 1000 -> "bin" (bir bin değil) kuralı
    assert sayi_yaziya(1000) == "bin"
    assert sayi_yaziya(1001) == "bin bir"
    assert sayi_yaziya(1010) == "bin on"
    assert sayi_yaziya(1100) == "bin yüz"
    assert sayi_yaziya(1250) == "bin iki yüz elli"
    assert sayi_yaziya(2000) == "iki bin"
    assert sayi_yaziya(2005) == "iki bin beş"
    assert sayi_yaziya(10_000) == "on bin"
    assert sayi_yaziya(10_001) == "on bin bir"
    assert sayi_yaziya(100_000) == "yüz bin"
    assert sayi_yaziya(101_000) == "yüz bir bin"
    assert sayi_yaziya(999_999) == "dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz"


def test_sayi_yaziya_milyon_milyar_trilyon():
    # 1_000_000 -> "bir milyon" (milyonda "bir" söylenir)
    assert sayi_yaziya(1_000_000) == "bir milyon"
    assert sayi_yaziya(1_000_001) == "bir milyon bir"
    assert sayi_yaziya(1_001_000) == "bir milyon bin"
    assert sayi_yaziya(1_250_003) == "bir milyon iki yüz elli bin üç"
    assert sayi_yaziya(1_000_000_000) == "bir milyar"
    assert sayi_yaziya(1_000_001_000) == "bir milyar bin"
    assert sayi_yaziya(1_000_000_000_000) == "bir trilyon"


def test_sayi_yaziya_maksimum_deger():
    max_sayi = 10**15 - 1
    beklenen = (
        "dokuz yüz doksan dokuz trilyon "
        "dokuz yüz doksan dokuz milyar "
        "dokuz yüz doksan dokuz milyon "
        "dokuz yüz doksan dokuz bin "
        "dokuz yüz doksan dokuz"
    )
    assert sayi_yaziya(max_sayi) == beklenen


def test_sayi_yaziya_negatif_sayilar():
    assert sayi_yaziya(-1) == "eksi bir"
    assert sayi_yaziya(-100) == "eksi yüz"
    assert sayi_yaziya(-1000) == "eksi bin"
    assert sayi_yaziya(-1001) == "eksi bin bir"
    assert sayi_yaziya(-1_250_003) == "eksi bir milyon iki yüz elli bin üç"
    max_negatif = -(10**15 - 1)
    beklenen = (
        "eksi dokuz yüz doksan dokuz trilyon "
        "dokuz yüz doksan dokuz milyar "
        "dokuz yüz doksan dokuz milyon "
        "dokuz yüz doksan dokuz bin "
        "dokuz yüz doksan dokuz"
    )
    assert sayi_yaziya(max_negatif) == beklenen


def test_sayi_yaziya_sinir_deger_hatalari():
    # Desteklenen aralık mutlak değerce 10**15'ten küçük sayılardır (|n| < 10**15)
    with pytest.raises(ValueError):
        sayi_yaziya(10**15)
    with pytest.raises(ValueError):
        sayi_yaziya(-10**15)
    with pytest.raises(ValueError):
        sayi_yaziya(10**16)
    with pytest.raises(ValueError):
        sayi_yaziya(-10**16)


def test_sayi_yaziya_tip_hatalari():
    with pytest.raises(TypeError):
        sayi_yaziya(True)  # bool dahil
    with pytest.raises(TypeError):
        sayi_yaziya(False)  # bool dahil
    with pytest.raises(TypeError):
        sayi_yaziya(10.0)  # float dahil
    with pytest.raises(TypeError):
        sayi_yaziya("100")
    with pytest.raises(TypeError):
        sayi_yaziya(None)
    with pytest.raises(TypeError):
        sayi_yaziya([1])
