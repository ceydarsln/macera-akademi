#!/bin/bash
# Depodaki web kaynaklarını Android APK varlıklarına kopyalar.
# svgciz.js'e içerik damgası eklenir: tarayıcı ve WebView bayat kopya tutmasın.
set -e

BETIK_DIZINI="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJE_KOKU="$(cd "$BETIK_DIZINI/.." && pwd)"
KAYNAK="$PROJE_KOKU/web"
SABLONLAR="$KAYNAK/phaser"
VARLIKLAR="$PROJE_KOKU/app/src/main/assets"

mkdir -p "$VARLIKLAR/phaser"
if command -v md5 >/dev/null 2>&1; then
  DAMGA=$(md5 -q "$SABLONLAR/svgciz.js" | cut -c1-8)
elif command -v md5sum >/dev/null 2>&1; then
  DAMGA=$(md5sum "$SABLONLAR/svgciz.js" | cut -c1-8)
else
  echo "Hata: md5 veya md5sum bulunamadı." >&2
  exit 1
fi
for f in "$SABLONLAR"/*-phaser.html; do
  ad=$(basename "$f" -phaser.html)
  sed -e 's|https://cdn.jsdelivr.net/npm/phaser@3.80.1/dist/phaser.min.js|phaser.min.js|' \
      -e "s|src=\"svgciz.js\"|src=\"svgciz.js?s=$DAMGA\"|" "$f" > "$VARLIKLAR/phaser/$ad.html"
  # Uygulama iframe'i "phaser/<ad>.html" istiyor; web klasöründe kaynaklar
  # "<ad>-phaser.html" adıyla durduğu için web sürümü 404 veriyordu.
  # Aynı adla bir kopya da web klasörüne yazılır (üretilmiş dosya, .gitignore'da).
  cp "$f" "$SABLONLAR/$ad.html"
done
cp "$SABLONLAR/svgciz.js" "$VARLIKLAR/phaser/svgciz.js"
cp "$SABLONLAR/scene-workshop.js" "$VARLIKLAR/phaser/scene-workshop.js"
cp "$SABLONLAR/scene-workshop.css" "$VARLIKLAR/phaser/scene-workshop.css"
cp "$SABLONLAR/scene-discovery.js" "$VARLIKLAR/phaser/scene-discovery.js"
cp "$SABLONLAR/scene-discovery.css" "$VARLIKLAR/phaser/scene-discovery.css"
cp "$SABLONLAR/scene-measure.js" "$VARLIKLAR/phaser/scene-measure.js"
cp "$SABLONLAR/scene-measure.css" "$VARLIKLAR/phaser/scene-measure.css"
cp "$SABLONLAR/scene-collections.js" "$VARLIKLAR/phaser/scene-collections.js"
cp "$SABLONLAR/scene-collections.css" "$VARLIKLAR/phaser/scene-collections.css"
cp "$SABLONLAR/scene-stories.js" "$VARLIKLAR/phaser/scene-stories.js"
cp "$SABLONLAR/scene-stories.css" "$VARLIKLAR/phaser/scene-stories.css"
cp "$SABLONLAR/scene-magnets.js" "$VARLIKLAR/phaser/scene-magnets.js"
cp "$SABLONLAR/scene-magnets.css" "$VARLIKLAR/phaser/scene-magnets.css"
cp "$SABLONLAR/scene-pages.js" "$VARLIKLAR/phaser/scene-pages.js"
cp "$SABLONLAR/scene-pages.css" "$VARLIKLAR/phaser/scene-pages.css"
cp "$SABLONLAR/scene-destinations.js" "$VARLIKLAR/phaser/scene-destinations.js"
cp "$SABLONLAR/scene-destinations.css" "$VARLIKLAR/phaser/scene-destinations.css"
cp "$SABLONLAR/scene-forest-dig.js" "$VARLIKLAR/phaser/scene-forest-dig.js"
cp "$SABLONLAR/scene-forest-dig.css" "$VARLIKLAR/phaser/scene-forest-dig.css"
cp "$SABLONLAR/scene-bridges-motion.js" "$VARLIKLAR/phaser/scene-bridges-motion.js"
cp "$SABLONLAR/scene-bridges-motion.css" "$VARLIKLAR/phaser/scene-bridges-motion.css"
cp "$SABLONLAR/scene-book-power.js" "$VARLIKLAR/phaser/scene-book-power.js"
cp "$SABLONLAR/scene-book-power.css" "$VARLIKLAR/phaser/scene-book-power.css"
cp "$KAYNAK/macera-akademi.html" "$VARLIKLAR/macera-akademi.html"
cp "$KAYNAK/api-client.js" "$VARLIKLAR/api-client.js"
echo "kopyalandı: $(find "$VARLIKLAR/phaser" -maxdepth 1 -name '*.html' | wc -l | tr -d ' ') şablon · svgciz damgası $DAMGA"
