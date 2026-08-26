#!/usr/bin/env python3
"""Katalog başlığı/alt başlığı cevabı sızdırıyor mu?

Motor denetim araçları (tools/*_denetim.html) şablonu doğrudan iframe'e yükler;
katalogdaki `title` ve `sub` alanları o kabuğun dışında kaldığı için hiç
çizilmez. Oysa gerçek uygulamada ikisi de oyunun üstünde ekranda durur. Bu
yüzden "alt başlık cevabı söylüyor" kusuru yalnız macera-akademi.html üzerinden
oynayarak görülebiliyordu. Bu betik o boşluğu statik olarak kapatır.

Ölçüt: başlık ve alt başlık BECERİYİ anlatmalı, cevabı değil.
  iyi  → "Duyduğun sayıyı onlar-birler yaz"
  kötü → "14 sayısını yaz"          (hedef ekranda yazılı olmayacaktı)
  kötü → "Lale Tarlası" + cevabı "lale" olan bir tur

Kullanım:
    python3 tools/katalog_sizinti.py t   web/phaser/turkce1-pdf-phaser.html
    python3 tools/katalog_sizinti.py h   web/phaser/hayatbilgisi2-pdf-phaser.html
    python3 tools/katalog_sizinti.py sb  web/phaser/sosyal4-pdf-phaser.html

Çıkış kodu: sızıntı bulunursa 1, temizse 0.
"""
import re
import sys
import pathlib

KOK = pathlib.Path(__file__).resolve().parent.parent
KATALOG = KOK / "web/macera-akademi.html"

# Hedef değer taşıyan alanlar. Yeni mekanik eklenirse buraya da eklenmeli.
HEDEF_ALANLARI = [
    r"kelime:'([^']*)'",       # fabrika, dikte
    r"hedefSes:'([^']*)'",     # tren, uzay
    r"hedefler:\[([^\]]*)\]",  # kurbaga, balon
    r"metin:'([^']*)'",        # sandik
    r"numara:'([^']*)'",       # tus
]
DOGRU_ETIKET = r"\{(?:im:'[^']*',)?(?:ad|label|t):'([^']*)',correct:true\}"


def sade(x: str) -> str:
    x = x.lower().replace("i̇", "i")
    return re.sub(r"[^0-9a-zçğıöşü]+", " ", x).strip()


def katalog_kayitlari(onek: str):
    """id -> (title, sub). Boşluklu ve boşluksuz iki yazım biçimini de kabul eder."""
    s = KATALOG.read_text(encoding="utf-8")
    kalip = (r"\{id:\s*'(%s\d+)'\s*,\s*grp:\s*'[^']*'\s*,\s*"
             r"title:\s*'([^']*)'\s*,\s*sub:\s*'([^']*)'" % re.escape(onek))
    return {m.group(1): (m.group(2), m.group(3)) for m in re.finditer(kalip, s)}


def motor_hedefleri(motor: pathlib.Path, onek: str):
    """id -> hedef sözcük kümesi."""
    s = motor.read_text(encoding="utf-8")
    parca = re.split(r"\nGAMES\.(%s\d+)=" % re.escape(onek), s)
    out = {}
    for i in range(1, len(parca), 2):
        gid, gov = parca[i], parca[i + 1]
        h = set()
        for pat in HEDEF_ALANLARI:
            for m in re.finditer(pat, gov):
                icerik = m.group(1)
                for tek in (re.findall(r"'([^']*)'", icerik) or [icerik]):
                    if tek:
                        h.add(tek)
        for m in re.finditer(DOGRU_ETIKET, gov):
            h.add(m.group(1))
        out[gid] = {x for x in h if len(sade(x)) >= 2}
    return out


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    onek, motor = sys.argv[1], pathlib.Path(sys.argv[2])
    if not motor.is_absolute():
        motor = KOK / motor
    katalog = katalog_kayitlari(onek)
    hedefler = motor_hedefleri(motor, onek)
    if not katalog:
        print("katalogda '%s' önekli oyun bulunamadı" % onek)
        return 2

    bulgu = []
    for gid, (title, sub) in sorted(katalog.items()):
        metin = sade(title + " " + sub)
        hed = hedefler.get(gid, set())
        gecen = [h for h in hed
                 if re.search(r"(?:^| )" + re.escape(sade(h)) + r"(?:$| )", metin)]
        if not gecen:
            continue
        # Seçenek kümesinin tamamı anılmışsa cevap ele verilmiş olmaz
        # (ör. "Nokta mı, soru işareti mi" — iki seçenek de yazılı).
        if len(gecen) >= 2 and len(gecen) == len(hed):
            continue
        for h in gecen:
            bulgu.append((gid, title, sub, h))

    print("taranan oyun: %d" % len(katalog))
    for gid, title, sub, h in bulgu:
        print("SIZINTI %s | %s — %s | hedef: %s" % (gid, title, sub, h))
    if not bulgu:
        print("katalog başlık/alt başlıklarında hedef sızıntısı yok")
    return 1 if bulgu else 0


if __name__ == "__main__":
    sys.exit(main())
