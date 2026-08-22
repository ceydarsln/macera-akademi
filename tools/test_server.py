#!/usr/bin/env python3
"""Macera Akademi kaynaklarını ve birleşik test raporu yazımını sunar."""

from __future__ import annotations

import argparse
import http.server
import re
import sys
import urllib.parse
from pathlib import Path


PROJE_KOKU = Path(__file__).resolve().parent.parent
AZAMI_GOVDE = 32 * 1024 * 1024
GUVENLI_AD = re.compile(r"^[A-Za-z0-9._-]{1,120}$")


class TestIstegi(http.server.SimpleHTTPRequestHandler):
    server_version = "MaceraTest/1.0"

    def __init__(self, *args, directory: str | None = None, **kwargs):
        super().__init__(*args, directory=directory or str(PROJE_KOKU), **kwargs)

    @property
    def sonuc_klasoru(self) -> Path:
        return self.server.sonuc_klasoru  # type: ignore[attr-defined]

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, POST, OPTIONS")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def do_GET(self) -> None:
        yol = urllib.parse.urlparse(self.path).path
        if yol == "/saglik":
            self._yanit(200, b"ok\n", "text/plain; charset=utf-8")
            return
        super().do_GET()

    def do_POST(self) -> None:
        adres = urllib.parse.urlparse(self.path)
        if adres.path != "/kaydet":
            self._yanit(404, b"yalniz /kaydet destekleniyor\n")
            return

        sorgu = urllib.parse.parse_qs(adres.query)
        ad = sorgu.get("ad", [""])[0]
        if not GUVENLI_AD.fullmatch(ad) or Path(ad).name != ad:
            self._yanit(400, b"gecersiz dosya adi\n")
            return

        try:
            boy = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._yanit(400, b"gecersiz govde uzunlugu\n")
            return
        if boy < 0 or boy > AZAMI_GOVDE:
            self._yanit(413, b"govde cok buyuk\n")
            return

        veri = self.rfile.read(boy)
        self.sonuc_klasoru.mkdir(parents=True, exist_ok=True)
        hedef = self.sonuc_klasoru / ad
        kip = "ab" if sorgu.get("tek", ["0"])[0] == "1" else "wb"
        with hedef.open(kip) as dosya:
            dosya.write(veri)
        self._yanit(200, (ad + "\n").encode("utf-8"))

    def _yanit(self, kod: int, veri: bytes, tur: str = "text/plain; charset=utf-8") -> None:
        self.send_response(kod)
        self.send_header("Content-Type", tur)
        self.send_header("Content-Length", str(len(veri)))
        self.end_headers()
        self.wfile.write(veri)

    def log_message(self, bicim: str, *args: object) -> None:
        sys.stderr.write("[test] " + (bicim % args) + "\n")


def argumanlar() -> argparse.Namespace:
    ayr = argparse.ArgumentParser(description="Macera Akademi birleşik test sunucusu")
    ayr.add_argument("--host", default="127.0.0.1", help="dinlenecek adres (varsayılan: 127.0.0.1)")
    ayr.add_argument("--port", type=int, default=8870, help="dinlenecek port (varsayılan: 8870)")
    ayr.add_argument(
        "--results",
        type=Path,
        default=PROJE_KOKU / "test-results",
        help="JSON ve ekran görüntüsü çıktılarının klasörü",
    )
    return ayr.parse_args()


def main() -> None:
    sec = argumanlar()
    sunucu = http.server.ThreadingHTTPServer(
        (sec.host, sec.port),
        lambda *a, **k: TestIstegi(*a, directory=str(PROJE_KOKU), **k),
    )
    sunucu.sonuc_klasoru = sec.results.resolve()  # type: ignore[attr-defined]
    adres = f"http://{sec.host}:{sec.port}"
    print(f"Macera Akademi test sunucusu: {adres}")
    print(f"Uygulama: {adres}/app/src/main/assets/macera-akademi.html")
    print(f"Rapor klasörü: {sunucu.sonuc_klasoru}")
    print("Durdurmak için Ctrl+C")
    try:
        sunucu.serve_forever()
    except KeyboardInterrupt:
        print("\nTest sunucusu durduruldu.")
    finally:
        sunucu.server_close()


if __name__ == "__main__":
    main()
