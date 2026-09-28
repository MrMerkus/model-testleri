// Görev 2 hakemi: node mayin_hakem.js <index.html> <ekran-görüntüsü-öneki>
// Her kontrol bir puan; sonuç JSON olarak stdout'a.
const PW = process.env.PW_CORE || require('os').homedir() + '/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core';
const { chromium } = require(PW);
const path = require('path');

const [html, onek] = process.argv.slice(2);
const sonuc = { kontroller: {}, notlar: [] };
const kontrol = (ad, ok, not) => { sonuc.kontroller[ad] = !!ok; if (!ok && not) sonuc.notlar.push(`${ad}: ${not}`); };

(async () => {
  const tarayici = await chromium.launch();
  const sayfa = await tarayici.newPage({ viewport: { width: 900, height: 900 } });
  const hatalar = [], disIstek = [];
  sayfa.on('pageerror', e => hatalar.push(String(e)));
  sayfa.on('console', m => { if (m.type() === 'error') hatalar.push(m.text()); });
  sayfa.on('request', r => { if (!/^(file|data|blob|about):/.test(r.url())) disIstek.push(r.url()); });

  const hucre = (r, c) => sayfa.locator(`[data-r="${r}"][data-c="${c}"]`).first();
  const durum = async () => (await sayfa.locator('#durum').first().textContent().catch(() => '')) || '';
  const mayinlar = async () => sayfa.evaluate(() =>
    typeof window.mayinKonumlari === 'function' ? window.mayinKonumlari() : 'YOK');
  const aciklar = async () => sayfa.locator('[data-r][data-c].acik').count();
  const mset = m => new Set(m.map(([r, c]) => `${Number(r)},${Number(c)}`));
  const komsu = (r, c) => { const k = []; for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
    const a = r + dr, b = c + dc; if ((dr || dc) && a >= 0 && a < 9 && b >= 0 && b < 9) k.push([a, b]); } return k; };

  try {
    await sayfa.goto('file://' + path.resolve(html));
    await sayfa.waitForTimeout(500);
    kontrol('81_hucre', (await sayfa.locator('[data-r][data-c]').count()) === 81);
    kontrol('once_null', (await mayinlar()) === null, `ilk tıklamadan önce: ${JSON.stringify(await mayinlar())}`);

    await hucre(4, 4).click();
    await sayfa.waitForTimeout(200);
    let m = await mayinlar();
    const mOk = Array.isArray(m) && m.length === 10;
    kontrol('on_mayin', mOk, `mayinKonumlari: ${JSON.stringify(m)}`);
    if (!mOk) throw new Error('mayın konumu okunamadı, kalan kontroller atlandı');
    const M = mset(m);
    kontrol('ilk_tik_guvenli', [[4, 4], ...komsu(4, 4)].every(([r, c]) => !M.has(`${r},${c}`)));
    kontrol('zincirleme_acilma', (await Promise.all(komsu(4, 4).map(([r, c]) =>
      hucre(r, c).evaluate(e => e.classList.contains('acik'))))).every(Boolean));
    await sayfa.screenshot({ path: `${onek}-oyun.png` });

    // açık hücrelerin sayıları doğru mu
    let sayiOk = true, yanlis = '';
    for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) {
      const h = hucre(r, c);
      if (!(await h.evaluate(e => e.classList.contains('acik')))) continue;
      const n = komsu(r, c).filter(([a, b]) => M.has(`${a},${b}`)).length;
      const metin = ((await h.textContent()) || '').trim();
      if (metin !== (n ? String(n) : '')) { sayiOk = false; yanlis = `(${r},${c}) "${metin}" != ${n}`; }
    }
    kontrol('sayilar_dogru', sayiOk, yanlis);

    // bayrak: kapalı, mayınsız bir hücre bul
    let hedef = null;
    for (let r = 0; r < 9 && !hedef; r++) for (let c = 0; c < 9 && !hedef; c++)
      if (!M.has(`${r},${c}`) && !(await hucre(r, c).evaluate(e => e.classList.contains('acik')))) hedef = [r, c];
    if (hedef) {
      const h = hucre(...hedef);
      await h.click({ button: 'right' });
      const bayrakli = await h.evaluate(e => e.classList.contains('bayrak'));
      await h.click();
      const acilmadi = !(await h.evaluate(e => e.classList.contains('acik')));
      await h.click({ button: 'right' });
      const kalkti = !(await h.evaluate(e => e.classList.contains('bayrak')));
      kontrol('bayrak_koy', bayrakli);
      kontrol('bayrakli_acilmaz', bayrakli && acilmadi);
      kontrol('bayrak_kaldir', bayrakli && kalkti);
    }

    // kazanma: bütün mayınsız hücreleri aç
    for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++)
      if (!M.has(`${r},${c}`) && !(await hucre(r, c).evaluate(e => e.classList.contains('acik'))))
        await hucre(r, c).click();
    await sayfa.waitForTimeout(300);
    kontrol('kazandin', (await durum()).includes('Kazandın'), `durum: "${await durum()}"`);
    const [mr, mc] = m[0].map(Number);
    const once = await aciklar();
    await hucre(mr, mc).click();
    kontrol('bitince_donar', (await durum()).includes('Kazandın') && (await aciklar()) === once);
    await sayfa.screenshot({ path: `${onek}-kazandi.png` });

    // yeni oyun
    await sayfa.locator('#yeni').first().click();
    await sayfa.waitForTimeout(300);
    kontrol('yeni_oyun', (await mayinlar()) === null && (await aciklar()) === 0);

    // kaybetme
    await hucre(0, 0).click();
    await sayfa.waitForTimeout(200);
    m = await mayinlar();
    const M2 = mset(m);
    const [kr, kc] = m[0].map(Number);
    await hucre(kr, kc).click();
    await sayfa.waitForTimeout(300);
    kontrol('kaybettin', (await durum()).includes('Kaybettin'), `durum: "${await durum()}"`);
    let kapali = null;
    for (let r = 0; r < 9 && !kapali; r++) for (let c = 0; c < 9 && !kapali; c++)
      if (!M2.has(`${r},${c}`) && !(await hucre(r, c).evaluate(e => e.classList.contains('acik')))) kapali = [r, c];
    if (kapali) {
      const once2 = await aciklar();
      await hucre(...kapali).click();
      kontrol('kaybedince_donar', (await aciklar()) === once2);
    }
    await sayfa.screenshot({ path: `${onek}-kaybetti.png` });
  } catch (e) {
    sonuc.notlar.push('durdu: ' + String(e).split('\n')[0]);
  }
  kontrol('konsol_hatasi_yok', hatalar.length === 0, hatalar.slice(0, 3).join(' | '));
  kontrol('dis_kaynak_yok', disIstek.length === 0, disIstek.slice(0, 3).join(' '));
  const d = Object.values(sonuc.kontroller);
  sonuc.puan = `${d.filter(Boolean).length}/16`;
  console.log(JSON.stringify(sonuc));
  await tarayici.close();
})();
