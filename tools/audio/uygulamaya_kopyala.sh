#!/bin/bash
set -e
KOK="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJE_KOKU="$(cd "$KOK/../.." && pwd)"
HEDEF="$PROJE_KOKU/app/src/main/assets/ses"
mkdir -p "$HEDEF"
cp -n "$KOK"/ses/*.ogg "$HEDEF"/ 2>/dev/null || true
echo "kayıt: $(ls "$HEDEF" | wc -l | tr -d ' ') · boyut: $(du -sh "$HEDEF" | cut -f1)"
