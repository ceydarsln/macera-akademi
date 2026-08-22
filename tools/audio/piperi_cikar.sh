#!/bin/bash
# Kayıtlar hazır olunca Piper'ı APK'dan çıkarır: ~13 MB kazanç.
# (Kayıt bulunamayan bir cümle kalırsa sistem sesi devreye girer.)
set -e
P="$HOME/Downloads/MaceraAkademi-3"
SES="$P/app/src/main/assets/ses"
n=$(ls "$SES"/*.ogg 2>/dev/null | wc -l | tr -d ' ')
if [ "$n" -lt 2000 ]; then echo "Kayıt sayısı $n — 2000'in altında, Piper çıkarılmıyor."; exit 1; fi
rm -f "$P/app/src/main/assets/piper/model.onnx"
rm -rf "$P/app/src/main/assets/piper"
rm -f "$P/app/libs/sherpa-onnx.aar"
python3 - <<'PY'
import io,re
g='/Users/ceyda/Downloads/MaceraAkademi-3/app/build.gradle'
b=io.open(g,encoding='utf-8').read()
b=b.replace("""    /* Piper/VITS sesletme motoru — GitHub sürümünden alınan yerel AAR */
    implementation files('libs/sherpa-onnx.aar')
""","")
b=re.sub(r"\n    packaging \{\n        jniLibs \{.*?\n        \}\n    \}\n", "\n", b, flags=re.S)
b=re.sub(r"\n        /\* Piper sesi yerel kitaplıkla.*?\n        ndk \{ abiFilters 'arm64-v8a' \}\n", "\n", b, flags=re.S)
io.open(g,'w',encoding='utf-8').write(b)
print('build.gradle: Piper bağımlılığı kaldırıldı')
PY
echo "Piper çıkarıldı. Şimdi MainActivity'den PiperSes çağrılarını kaldırmak gerekiyor."
