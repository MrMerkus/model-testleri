#!/usr/bin/env python3
"""Model testlerini puanlar: python3 puanla.py [model-testleri-kökü]
Görev 1: gizli test (43) · Görev 2: tarayıcı hakemi (16) · Görev 3: görünen (8) + gizli (11) test,
test dosyası bütünlüğü, değişen satır sayısı. Sonuç: <kök>/_puanlar.json ve stdout'ta Markdown tablo."""
import difflib, hashlib, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HAKEM = Path(__file__).resolve().parent
KOK = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / "ofis/model-testleri").resolve()
PY = str(KOK / ".venv/bin/python")
MODELLER = ["sonnet-5.5", "opus-4.6", "sonnet-4.6", "gemini-3.8-flash", "gemini-3.1-pro", "space-bunny"]
GOREV3_TEST = KOK / "_gorevler/3-hata-avi/test_kutuphane.py"


def pytest(klasor, dosya):
    """(geçen, toplam) döner."""
    try:
        r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--timeout=10", dosya],
                           cwd=klasor, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return 0, 1  # takılan kod (sonsuz döngü) sıfır alır
    gecen = int(m.group(1)) if (m := re.search(r"(\d+) passed", r.stdout)) else 0
    kalan = sum(int(x) for x in re.findall(r"(\d+) (?:failed|error)", r.stdout))
    return gecen, gecen + kalan


def gizli(model_dir, kaynak, test):
    if not (model_dir / kaynak).exists():
        return None
    with tempfile.TemporaryDirectory() as t:
        shutil.copy(model_dir / kaynak, t)
        shutil.copy(test, t)
        return pytest(t, Path(test).name)


def gorev1(d):
    s = {"gizli": gizli(d, "tr_metin.py", HAKEM / "1/test_gizli.py")}
    s["kendi_testi"] = pytest(d, "test_tr_metin.py") if (d / "test_tr_metin.py").exists() else None
    return s


def gorev2(d, model):
    if not (d / "index.html").exists():
        return {"puan": None}
    ek = KOK / "_ekranlar"; ek.mkdir(exist_ok=True)
    r = subprocess.run(["node", str(HAKEM / "2/mayin_hakem.js"), str(d / "index.html"), str(ek / model)],
                       capture_output=True, text=True, timeout=180)
    try:
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        return {"puan": "0/16", "notlar": ["hakem çıktısı okunamadı: " + r.stderr[-300:]]}


def gorev3(d):
    s = {"test_dosyasi_ayni": (d / "test_kutuphane.py").exists() and
         hashlib.sha256((d / "test_kutuphane.py").read_bytes()).digest() ==
         hashlib.sha256(GOREV3_TEST.read_bytes()).digest()}
    # görünen testler her zaman ORİJİNAL test dosyasıyla koşulur
    s["gorunen"] = gizli(d, "kutuphane.py", GOREV3_TEST)
    s["gizli"] = gizli(d, "kutuphane.py", HAKEM / "3/test_gizli.py")
    if (d / "kutuphane.py").exists():
        eski = (KOK / "_gorevler/3-hata-avi/kutuphane.py").read_text().splitlines()
        yeni = (d / "kutuphane.py").read_text().splitlines()
        s["degisen_satir"] = sum(1 for x in difflib.unified_diff(eski, yeni, n=0)
                                 if x[:1] in "+-" and not x.startswith(("+++", "---")))
    return s


def sureler():
    s = {}
    f = KOK / "_sureler.tsv"
    if f.exists():
        for satir in f.read_text().splitlines():
            m, g, sn, kod = satir.split("\t")
            s[(m, g)] = (int(sn), int(kod))
    return s


def oran(x):
    return "—" if not x else f"{x[0]}/{x[1]}"


def main():
    S, sonuc = sureler(), {}
    for m in MODELLER:
        md = KOK / m
        if not md.exists():
            continue
        sonuc[m] = {"1": gorev1(md / "1-turkce-metin"), "2": gorev2(md / "2-mayin-tarlasi", m),
                    "3": gorev3(md / "3-hata-avi"),
                    "sure": {g: S.get((m, g)) for g in ["1-turkce-metin", "2-mayin-tarlasi", "3-hata-avi"]}}
    (KOK / "_puanlar.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1))
    print("| Model | G1 gizli test | G1 kendi testi | G2 tarayıcı | G3 görünen | G3 gizli | G3 test dosyası | G3 değişen satır | Süre (G1/G2/G3) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for m, s in sonuc.items():
        su = "/".join("—" if not v else (f"{v[0]//60}dk" + ("⏱" if v[1] == 124 else "")) for v in s["sure"].values())
        print(f"| {m} | {oran(s['1']['gizli'])} | {oran(s['1']['kendi_testi'])} | {s['2'].get('puan') or '—'} | "
              f"{oran(s['3']['gorunen'])} | {oran(s['3']['gizli'])} | {'✅' if s['3']['test_dosyasi_ayni'] else '❌'} | "
              f"{s['3'].get('degisen_satir', '—')} | {su} |")


if __name__ == "__main__":
    main()
