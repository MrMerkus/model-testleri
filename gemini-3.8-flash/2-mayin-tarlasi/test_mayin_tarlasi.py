"""
Mayın Tarlası - Otomatik Test Paketi (pytest)
EMIR.md sözleşmesine uygunluk testleri
"""
import os
import re
import json
import subprocess
import pytest

INDEX_PATH = os.path.join(os.path.dirname(__file__), "index.html")

def test_index_html_mevcut():
    """index.html dosyası mevcut olmalıdır."""
    assert os.path.exists(INDEX_PATH), "index.html bulunamadı"

def test_dis_kaynak_yok():
    """Dış kaynak (CDN, harici font, harici stil/script/resim) kullanılmamalıdır."""
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Dış linkler / CDN kontrolü
    external_links = re.findall(r'<link[^>]+href=["\'](http[s]?://[^"\']+)["\']', content, re.IGNORECASE)
    assert len(external_links) == 0, f"Harici link bulundu: {external_links}"

    external_scripts = re.findall(r'<script[^>]+src=["\'](http[s]?://[^"\']+)["\']', content, re.IGNORECASE)
    assert len(external_scripts) == 0, f"Harici script bulundu: {external_scripts}"

    external_css_fonts = re.findall(r'@import\s+url\(["\']?(http[s]?://[^"\'\)]+)["\']?\)', content, re.IGNORECASE)
    assert len(external_css_fonts) == 0, f"Harici font/stil import bulundu: {external_css_fonts}"

def test_html_sozlesme_elementleri():
    """81 adet hücre (data-r, data-c 0-8), #durum ve #yeni elementleri HTML içinde mevcut olmalıdır."""
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    assert 'id="durum"' in html, 'id="durum" elementi bulunamadı'
    assert 'id="yeni"' in html, 'id="yeni" elementi bulunamadı'

    # 81 hücrenin data-r ve data-c özelliklerini kontrol et
    for r in range(9):
        for c in range(9):
            pattern = rf'data-r="{r}"[^>]*data-c="{c}"|data-c="{c}"[^>]*data-r="{r}"'
            assert re.search(pattern, html) is not None, f"Hücre (r={r}, c={c}) HTML içinde bulunamadı"

def run_js_test(test_code: str):
    """Node.js ortamında test betiğini çalıştırıp sonucu JSON olarak alır."""
    runner = f"""
    const fs = require('fs');
    const vm = require('vm');

    const html = fs.readFileSync('{INDEX_PATH}', 'utf8');

    class ClassList {{
      constructor(el) {{ this.el = el; this._classes = new Set(); }}
      add(...cls) {{ cls.forEach(c => this._classes.add(c)); }}
      remove(...cls) {{ cls.forEach(c => this._classes.delete(c)); }}
      contains(c) {{ return this._classes.has(c); }}
      get value() {{ return Array.from(this._classes).join(' '); }}
      set value(v) {{ this._classes = new Set(v ? v.split(/\\s+/).filter(Boolean) : []); }}
    }}

    class MockElement {{
      constructor(tag, id = null) {{
        this.tagName = tag.toUpperCase();
        this.id = id;
        this.attributes = new Map();
        this.classList = new ClassList(this);
        this._textContent = '';
        this.listeners = {{}};
      }}
      getAttribute(name) {{ return this.attributes.get(name) || null; }}
      setAttribute(name, val) {{ this.attributes.set(name, String(val)); }}
      removeAttribute(name) {{ this.attributes.delete(name); }}
      get textContent() {{ return this._textContent; }}
      set textContent(v) {{ this._textContent = String(v); }}
      get className() {{ return this.classList.value; }}
      set className(v) {{ this.classList.value = v; }}
      addEventListener(event, fn) {{
        if (!this.listeners[event]) this.listeners[event] = [];
        this.listeners[event].push(fn);
      }}
      dispatchEvent(event) {{
        const list = this.listeners[event.type] || [];
        for (const fn of list) fn.call(this, event);
      }}
      click() {{
        this.dispatchEvent({{ type: 'click', preventDefault: () => {{}}, button: 0 }});
      }}
      contextmenu() {{
        this.dispatchEvent({{ type: 'contextmenu', preventDefault: () => {{}}, button: 2 }});
      }}
    }}

    const durumEl = new MockElement('div', 'durum');
    const yeniBtn = new MockElement('button', 'yeni');
    const sayacMayin = new MockElement('span', 'sayac-mayin');
    const sayacSure = new MockElement('span', 'sayac-sure');
    const tahtaEl = new MockElement('div', 'tahta');

    const cells = [];
    const cellMap = {{}};
    for (let r = 0; r < 9; r++) {{
      for (let c = 0; c < 9; c++) {{
        const btn = new MockElement('button');
        btn.className = 'hucre';
        btn.setAttribute('data-r', r);
        btn.setAttribute('data-c', c);
        cells.push(btn);
        cellMap[`${{r}},${{c}}`] = btn;
      }}
    }}

    const doc = {{
      getElementById: (id) => {{
        if (id === 'durum') return durumEl;
        if (id === 'yeni') return yeniBtn;
        if (id === 'sayac-mayin') return sayacMayin;
        if (id === 'sayac-sure') return sayacSure;
        if (id === 'tahta') return tahtaEl;
        return null;
      }}
    }};
    tahtaEl.querySelectorAll = (sel) => {{
      if (sel === '.hucre') return cells;
      return [];
    }};

    const scriptMatch = html.match(/<script>([\\s\\S]*?)<\\/script>/);
    if (!scriptMatch) throw new Error('No script found');

    const windowObj = {{}};
    let lastTimerId = 0;
    const sandbox = {{
      window: windowObj,
      document: doc,
      setInterval: (fn, ms) => ++lastTimerId,
      clearInterval: () => {{}},
      Date: Date,
      Math: Math,
      Set: Set,
      Array: Array,
      parseInt: parseInt,
      String: String,
      console: console
    }};

    vm.createContext(sandbox);
    vm.runInContext(scriptMatch[1], sandbox);

    function getCell(r, c) {{ return cellMap[`${{r}},${{c}}`]; }}

    // Test execution block
    const runTest = () => {{
      {test_code}
    }};

    try {{
      const res = runTest();
      console.log(JSON.stringify({{ success: true, result: res }}));
    }} catch (err) {{
      console.log(JSON.stringify({{ success: false, error: err.message, stack: err.stack }}));
    }}
    """
    proc = subprocess.run(["node", "-e", runner], capture_output=True, text=True, check=True)
    out = json.loads(proc.stdout.strip())
    if not out["success"]:
        raise AssertionError(f"JS Test Hatası: {out.get('error')}\n{out.get('stack')}")
    return out["result"]

def test_mayin_konumlari_baslangicta_null():
    """İlk tıklamadan önce window.mayinKonumlari() null dönmelidir."""
    res = run_js_test("""
      return windowObj.mayinKonumlari();
    """)
    assert res is None, f"Beklenen null, dönen: {res}"

def test_ilk_tiklama_ve_guvenli_bolge():
    """İlk tıklanan hücre ve 8 komşusu mayınsız olmalıdır; tam 10 mayın yerleşmelidir."""
    # Köşe testi (0, 0)
    res_kose = run_js_test("""
      getCell(0, 0).click();
      const mayinlar = windowObj.mayinKonumlari();
      return { mayinlar, acik: getCell(0, 0).classList.contains('acik') };
    """)
    assert res_kose["acik"] is True, "İlk tıklanan hücre açılmadı"
    assert len(res_kose["mayinlar"]) == 10, f"10 mayın bekleniyordu, {len(res_kose['mayinlar'])} bulundu"
    for r, c in res_kose["mayinlar"]:
        assert not (r <= 1 and c <= 1), f"Köşe safe zone içinde mayın bulundu: ({r}, {c})"

    # Merkez testi (4, 4)
    res_merkez = run_js_test("""
      yeniBtn.click();
      getCell(4, 4).click();
      const mayinlar = windowObj.mayinKonumlari();
      return { mayinlar, acik: getCell(4, 4).classList.contains('acik') };
    """)
    assert res_merkez["acik"] is True
    assert len(res_merkez["mayinlar"]) == 10
    for r, c in res_merkez["mayinlar"]:
        assert not (abs(r - 4) <= 1 and abs(c - 4) <= 1), f"Merkez safe zone içinde mayın bulundu: ({r}, {c})"

def test_hucre_metin_ve_sinif_sozlesmesi():
    """Açılmış sayılı hücrenin metni yalnız o rakamdır; açılmış 0 hücrenin metni boştur; acik sınıfı vardır."""
    res = run_js_test("""
      getCell(4, 4).click();
      const acikHucreler = cells.filter(c => c.classList.contains('acik'));
      const durumlar = acikHucreler.map(c => ({
        r: c.getAttribute('data-r'),
        c: c.getAttribute('data-c'),
        text: c.textContent,
        classes: Array.from(c.classList._classes)
      }));
      return durumlar;
    """)
    assert len(res) >= 9, "İlk tıklama en az 9 hücreyi açmalıdır"
    for item in res:
        assert "acik" in item["classes"], f"Açılan hücrede 'acik' sınıfı yok: {item}"
        text = item["text"]
        # Metin boş ("") veya sadece "1".."8" rakamı olmalıdır
        assert text in ["", "1", "2", "3", "4", "5", "6", "7", "8"], f"Geçersiz hücre metni: '{text}'"

def test_sag_tik_bayrak_ve_sol_tik_korumasi():
    """Sağ tık bayrak koyar/kaldırır. Bayraklı hücrede bayrak sınıfı olur. Bayraklı hücre sol tıkla açılmaz."""
    res = run_js_test("""
      const c = getCell(1, 1);
      // Sağ tık -> bayrak koy
      c.contextmenu();
      const bayrakliMi = c.classList.contains('bayrak');
      const textBayrak = c.textContent;

      // Sol tıkla açmayı dene -> açılmamalı
      c.click();
      const acildiMi = c.classList.contains('acik');

      // Sağ tık -> bayrak kaldır
      c.contextmenu();
      const bayrakKaldirildiMi = !c.classList.contains('bayrak');
      const textTemiz = c.textContent;

      return { bayrakliMi, textBayrak, acildiMi, bayrakKaldirildiMi, textTemiz };
    """)
    assert res["bayrakliMi"] is True, "Sağ tık bayrak sınıfı eklemedi"
    assert res["acildiMi"] is False, "Bayraklı hücre sol tıkla açılmamalıdır"
    assert res["bayrakKaldirildiMi"] is True, "İkinci sağ tık bayrağı kaldırmadı"
    assert res["textTemiz"] == "", "Bayrak kalkınca hücre metni boş olmalıdır"

def test_mayina_basinca_kaybetme():
    """Mayına basınca oyun kaybedilir, durum metni 'Kaybettin' içerir, bütün mayınlar gösterilir, tıklamalar durur."""
    res = run_js_test("""
      getCell(0, 0).click();
      const mayinlar = windowObj.mayinKonumlari();
      const [mr, mc] = mayinlar[0];

      // Mayına tıkla
      getCell(mr, mc).click();
      const durumMetni = durumEl.textContent;

      // Bütün mayınlar gösterildi mi?
      const gosterilenMayinSayisi = cells.filter(c => c.classList.contains('mayin')).length;

      // Oyun bittikten sonra başka bir hücreye tıklamayı dene
      const baskaHucre = cells.find(c => !c.classList.contains('acik'));
      let baskaHucreAcildiMi = false;
      if (baskaHucre) {
        baskaHucre.click();
        baskaHucreAcildiMi = baskaHucre.classList.contains('acik');
      }

      return {
        durumMetni,
        gosterilenMayinSayisi,
        baskaHucreAcildiMi
      };
    """)
    assert "Kaybettin" in res["durumMetni"], f"Durum metni 'Kaybettin' içermiyor: '{res['durumMetni']}'"
    assert res["gosterilenMayinSayisi"] == 10, f"Bütün 10 mayın gösterilmedi: {res['gosterilenMayinSayisi']}"
    assert res["baskaHucreAcildiMi"] is False, "Oyun bittikten sonra tıklamalar tahtayı değiştirmemelidir"

def test_tum_guvenli_hucreleri_acinca_kazanma():
    """Mayın olmayan bütün hücreler (71 adet) açılınca oyun kazanılır, durum metni 'Kazandın' içerir."""
    res = run_js_test("""
      getCell(4, 4).click();
      const mayinlar = windowObj.mayinKonumlari();
      const mayinSet = new Set(mayinlar.map(([r, c]) => `${r},${c}`));

      // Mayın olmayan tüm hücreleri tıkla
      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          if (!mayinSet.has(`${r},${c}`)) {
            getCell(r, c).click();
          }
        }
      }

      const durumMetni = durumEl.textContent;
      const acikSayisi = cells.filter(c => c.classList.contains('acik')).length;

      // Oyun bittikten sonra mayına tıklamayı dene
      const [mr, mc] = mayinlar[0];
      const mayinHucresi = getCell(mr, mc);
      mayinHucresi.click();
      const mayinPatladiMi = mayinHucresi.classList.contains('patladi');

      return {
        durumMetni,
        acikSayisi,
        mayinPatladiMi
      };
    """)
    assert "Kazandın" in res["durumMetni"], f"Durum metni 'Kazandın' içermiyor: '{res['durumMetni']}'"
    assert res["acikSayisi"] == 71, f"71 güvenli hücrenin tümü açık olmalıdır: {res['acikSayisi']}"
    assert res["mayinPatladiMi"] is False, "Kazanıldıktan sonra tıklamalar tahtayı değiştirmemelidir"

def test_yeni_butonu_oyunu_sifirlar():
    """id='yeni' butonu oyunu sıfırlamalı, mayinKonumlari tekrar null olmalı, tahta temizlenmelidir."""
    res = run_js_test("""
      getCell(2, 2).click();
      const mayinlarIlk = windowObj.mayinKonumlari();

      // Sıfırla
      yeniBtn.click();
      const mayinlarSonra = windowObj.mayinKonumlari();
      const acikKalanVarMi = cells.some(c => c.classList.contains('acik'));
      const bayrakKalanVarMi = cells.some(c => c.classList.contains('bayrak'));
      const yaziKalanVarMi = cells.some(c => c.textContent !== '');
      const durumMetni = durumEl.textContent;

      return {
        mayinlarIlkUzunluk: mayinlarIlk.length,
        mayinlarSonra,
        acikKalanVarMi,
        bayrakKalanVarMi,
        yaziKalanVarMi,
        durumMetni
      };
    """)
    assert res["mayinlarIlkUzunluk"] == 10
    assert res["mayinlarSonra"] is None, f"Sıfırlama sonrası mayinKonumlari() null olmalı, fakat: {res['mayinlarSonra']}"
    assert res["acikKalanVarMi"] is False, "Sıfırlama sonrası açık hücre kalmamalıdır"
    assert res["bayrakKalanVarMi"] is False, "Sıfırlama sonrası bayraklı hücre kalmamalıdır"
    assert res["yaziKalanVarMi"] is False, "Sıfırlama sonrası metin içeren hücre kalmamalıdır"
    assert "Kazandın" not in res["durumMetni"] and "Kaybettin" not in res["durumMetni"]
