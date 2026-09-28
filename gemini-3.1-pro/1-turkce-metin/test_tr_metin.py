import pytest
from tr_metin import buyuk, kucuk, slug, sayi_yaziya

def test_buyuk():
    assert buyuk("istanbul ılık") == "İSTANBUL ILIK"
    assert buyuk("iı") == "İI"
    assert buyuk("çam ağacı") == "ÇAM AĞACI"

def test_kucuk():
    assert kucuk("IĞDIR İZMİR") == "ığdır izmir"
    assert kucuk("İI") == "iı"
    assert kucuk("Şemsiye") == "şemsiye"

def test_slug():
    assert slug("  Çok Güzel Şarkı: İyi ki Doğdun!  ") == "cok-guzel-sarki-iyi-ki-dogdun"
    assert slug("!@#") == ""
    assert slug("123 test") == "123-test"
    assert slug("  -  --  ") == ""

def test_sayi_yaziya():
    assert sayi_yaziya(1250003) == "bir milyon iki yüz elli bin üç"
    assert sayi_yaziya(-1001) == "eksi bin bir"
    assert sayi_yaziya(0) == "sıfır"
    assert sayi_yaziya(100) == "yüz"
    assert sayi_yaziya(1000) == "bin"
    assert sayi_yaziya(1000000) == "bir milyon"
    assert sayi_yaziya(15) == "on beş"
    assert sayi_yaziya(-200) == "eksi iki yüz"
    
    with pytest.raises(TypeError):
        sayi_yaziya(1.5)
    
    with pytest.raises(TypeError):
        sayi_yaziya(True)
        
    with pytest.raises(ValueError):
        sayi_yaziya(10**15)
        
    with pytest.raises(ValueError):
        sayi_yaziya(-10**15)
