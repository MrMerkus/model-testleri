import re

def buyuk(metin: str) -> str:
    return metin.replace("i", "İ").replace("ı", "I").upper()

def kucuk(metin: str) -> str:
    return metin.replace("İ", "i").replace("I", "ı").lower()

def slug(metin: str) -> str:
    metin = kucuk(metin)
    tr_to_en = {
        'ç': 'c',
        'ğ': 'g',
        'ı': 'i',
        'ö': 'o',
        'ş': 's',
        'ü': 'u'
    }
    for tr_char, en_char in tr_to_en.items():
        metin = metin.replace(tr_char, en_char)
    
    metin = re.sub(r'[^a-z0-9]+', '-', metin)
    return metin.strip('-')

def sayi_yaziya(n: int) -> str:
    if type(n) is not int:
        raise TypeError("Sayı int tipinde olmalıdır.")
    if not (-10**15 < n < 10**15):
        raise ValueError("Sayı desteklenen aralığın dışında.")
        
    if n == 0:
        return "sıfır"
        
    prefix = "eksi " if n < 0 else ""
    n = abs(n)
    
    magnitudes = ["", "bin", "milyon", "milyar", "trilyon"]
    
    chunks = []
    temp = n
    while temp > 0:
        chunks.append(temp % 1000)
        temp //= 1000
        
    res = []
    for i, chunk in enumerate(chunks):
        if chunk == 0:
            continue
            
        if i == 1 and chunk == 1:
            res.append("bin")
        else:
            yuzler, kalan = divmod(chunk, 100)
            onlar, birler = divmod(kalan, 10)
            
            parts = []
            if yuzler == 1:
                parts.append("yüz")
            elif yuzler > 1:
                birler_isim = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
                parts.append(birler_isim[yuzler])
                parts.append("yüz")
                
            if onlar > 0:
                onlar_isim = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
                parts.append(onlar_isim[onlar])
                
            if birler > 0:
                birler_isim = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
                parts.append(birler_isim[birler])
                
            kelime = " ".join(parts)
            if i > 0:
                kelime += " " + magnitudes[i]
            res.append(kelime)
            
    return prefix + " ".join(reversed(res))
