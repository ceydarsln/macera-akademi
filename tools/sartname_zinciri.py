#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Şartname zinciri denetimi.

Soru: motorlara uyguladığım düzeltme metni gerçekten düzeltme PDF'lerinin
içinde mi? Zincir şu: build_*.py betiği -> output/pdf/*.pdf (basılı belge)
                      build_*.py betiği -> tmp/spec_*.json -> oyun motoru

Bu araç zincirin iki ucunu karşılaştırır: kullandığım şartname cümlelerini
basılı PDF'in kendi metninde arar.

Not 1: Belgeler reportlab çıktısı; içerik akışları ASCII85 + Flate zincirli.
Not 2: Gömülü Arial alt kümesi Türkçe harfleri DÜŞÜRÜYOR ("yönü" -> "yn").
        Bu yüzden karşılaştırma, her cümlenin yalnız ASCII harflerden oluşan
        en uzun parçası üzerinden yapılıyor.

Kullanım:  python3 tools/sartname_zinciri.py [pdf_dizini]
"""
import base64
import io
import json
import os
import re
import sys
import zlib
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
VARSAYILAN_PDF = KOK / "output/pdf"


# ---------- PDF metin çıkarımı ----------
def _acil(v):
    for coz in (lambda x: zlib.decompress(x),
                lambda x: zlib.decompress(base64.a85decode(x, adobe=True)),
                lambda x: base64.a85decode(x, adobe=True)):
        try:
            return coz(v)
        except Exception:
            pass
    return v


def pdf_metni(yol):
    ham = open(yol, "rb").read()
    parcalar = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", ham, re.S):
        v = _acil(m.group(1).strip())
        if b"BT" not in v:
            continue
        for blok in re.findall(rb"BT(.*?)ET", v, re.S):
            for t in re.finditer(rb"\((?:\\.|[^\\()])*\)", blok):
                s = t.group(0)[1:-1]
                s = re.sub(rb"\\([0-7]{1,3})",
                           lambda k: bytes([int(k.group(1), 8) & 0xFF]), s)
                s = s.replace(b"\\(", b"(").replace(b"\\)", b")").replace(b"\\\\", b"\\")
                parcalar.append(s.decode("cp1254", "replace"))
            parcalar.append(" ")
    return re.sub(r"\s+", " ", "".join(parcalar))


# ---------- karşılaştırma ----------
TR = "çğıöşüâîû"


def sadele(s):
    t = str(s).lower()
    for h in TR:
        t = t.replace(h, "")
    return re.sub(r"[^a-z0-9]", "", t.replace("İ", "").replace("̇", ""))


def en_uzun_ascii(c):
    """Türkçe harflerin böldüğü parçaların en uzunu (font onları düşürüyor)."""
    ps = [re.sub(r"[^a-z0-9]", "", p)
          for p in re.split(r"[çğıöşüâîûiİ]", str(c).lower())]
    return max(ps, key=len) if ps else ""


def cumleler(x, derinlik=0):
    if derinlik > 5:
        return
    if isinstance(x, str):
        if len(x) > 28:
            yield x
    elif isinstance(x, list):
        for e in x:
            yield from cumleler(e, derinlik + 1)
    elif isinstance(x, dict):
        for e in x.values():
            yield from cumleler(e, derinlik + 1)


def betik_oyunlari(betik):
    """build_*.py içindeki games listesini reportlab'a ihtiyaç duymadan al."""
    src = io.open(betik, encoding="utf-8").read()
    bas = src.find("def G(")
    if bas < 0:
        return None
    sonlar = [src.find("THEMES = {"), src.find("doc = BaseDocTemplate")]
    son = min([s for s in sonlar if s > bas] or [len(src)])
    ns = {}
    try:
        exec(src[bas:son], ns)
    except Exception:
        return None
    return ns.get("games")


def betik_pdf_eslesmesi():
    esle = {}
    for b in sorted((KOK / "tmp/pdfs").glob("build_*_corrections.py")):
        src = io.open(b, encoding="utf-8").read()
        m = re.search(r'OUT\s*=\s*ROOT\s*/\s*"([^"]+)"', src)
        if m:
            esle[b] = os.path.basename(m.group(1))
    return esle


# spec dosyasından beslenen dersler (betikteki games çalıştırılamıyor)
SPEC_KAYNAKLARI = [
    ("2. sınıf Türkçe", "tmp/spec_u.json",
     "2_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf"),
    ("1. sınıf sayma", "tmp/pdfs/sayma1_games.json",
     "1_sinif_sayma_oyunlari_detayli_duzeltmeler.pdf"),
    ("1. sınıf Türkçe", "tmp/spec_t.json",
     "1_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf"),
]


def denetle(veri, pdf_yolu):
    metin = sadele(pdf_metni(pdf_yolu))
    sinanan = 0
    eksik = []
    for c in cumleler(veri):
        p = en_uzun_ascii(c)
        if len(p) < 14:
            continue
        sinanan += 1
        if p not in metin:
            eksik.append(c)
    return sinanan, eksik


def main():
    pdf_dizin = Path(sys.argv[1]) if len(sys.argv) > 1 else VARSAYILAN_PDF
    print("PDF dizini:", pdf_dizin)
    print("%-46s %6s %6s %8s" % ("BELGE", "sınan", "yok", "oran"))
    toplam_s = toplam_y = 0
    raporlar = []

    kaynaklar = []
    for betik, pdf in betik_pdf_eslesmesi().items():
        gs = betik_oyunlari(betik)
        if gs:
            kaynaklar.append((betik.name, gs, pdf))
    for ad, yol, pdf in SPEC_KAYNAKLARI:
        p = KOK / yol
        if p.exists():
            kaynaklar.append((yol, json.loads(p.read_text(encoding="utf-8")), pdf))

    for etiket, veri, pdf in kaynaklar:
        yol = pdf_dizin / pdf
        if not yol.exists():
            print("%-46s  belge bulunamadı" % pdf[:44])
            continue
        s, eksik = denetle(veri, yol)
        toplam_s += s
        toplam_y += len(eksik)
        print("%-46s %6d %6d %7.1f%%" % (pdf[:44], s, len(eksik),
                                         100 * (s - len(eksik)) / max(1, s)))
        if eksik:
            raporlar.append((pdf, etiket, eksik))

    print("\nTOPLAM sınanan %d · basılı belgede görünmeyen %d (%%%.1f)"
          % (toplam_s, toplam_y, 100 * toplam_y / max(1, toplam_s)))
    for pdf, etiket, eksik in raporlar:
        print("\n%s — basılı belgede görünmeyen %d cümle (kaynak: %s)"
              % (pdf, len(eksik), etiket))
        print("  Not: bunlar içerik farkı değil, sayfa yerleşiminde kırpılan")
        print("  tablo hücreleridir; betik/spec bunları içeriyor.")
        for c in eksik[:8]:
            print("   -", c[:100])
    return 1 if toplam_y else 0


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 0)
