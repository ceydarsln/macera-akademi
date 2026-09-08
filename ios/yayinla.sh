#!/bin/bash
# Macera Akademi — iOS App Store yayın betiği
#
# Kullanım:
#   TEAM_ID=XXXXXXXXXX ./ios/yayinla.sh arsiv     # .xcarchive üret
#   TEAM_ID=XXXXXXXXXX ./ios/yayinla.sh ipa       # arşivden .ipa çıkar
#   ./ios/yayinla.sh dogrula                      # .ipa'yı App Store'a karşı sına
#   ./ios/yayinla.sh yukle                        # App Store Connect'e gönder
#
# TEAM_ID: Apple geliştirici takım kimliği (Xcode > Settings > Accounts veya
# developer.apple.com > Membership sayfasındaki 10 karakterlik değer).
#
# Yükleme kimlik doğrulaması için App Store Connect API anahtarı gerekir:
#   ASC_KEY_ID, ASC_ISSUER_ID ve ~/.appstoreconnect/private_keys/AuthKey_<ID>.p8

set -euo pipefail

KOK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJE="$KOK/ios/MaceraAkademi.xcodeproj"
SEMA="MaceraAkademi"
CIKTI="$KOK/ios/.yayin"
ARSIV="$CIKTI/MaceraAkademi.xcarchive"
IPA="$CIKTI/MaceraAkademi.ipa"

mkdir -p "$CIKTI"

takim_gerekli() {
  if [ -z "${TEAM_ID:-}" ]; then
    echo "HATA: TEAM_ID tanımlı değil. Örnek: TEAM_ID=ABCDE12345 $0 $1" >&2
    exit 1
  fi
}

export_secenekleri() {
  cat > "$CIKTI/ExportOptions.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>method</key>
	<string>app-store-connect</string>
	<key>teamID</key>
	<string>$TEAM_ID</string>
	<key>signingStyle</key>
	<string>automatic</string>
	<key>destination</key>
	<string>export</string>
	<key>uploadSymbols</key>
	<true/>
	<key>manageAppVersionAndBuildNumber</key>
	<false/>
</dict>
</plist>
PLIST
}

case "${1:-}" in
  arsiv)
    takim_gerekli arsiv
    rm -rf "$ARSIV"
    xcodebuild -project "$PROJE" -scheme "$SEMA" \
      -configuration Release -destination "generic/platform=iOS" \
      -archivePath "$ARSIV" \
      DEVELOPMENT_TEAM="$TEAM_ID" \
      -allowProvisioningUpdates \
      archive
    echo "Arşiv hazır: $ARSIV"
    ;;

  ipa)
    takim_gerekli ipa
    [ -d "$ARSIV" ] || { echo "HATA: önce '$0 arsiv' çalıştırın." >&2; exit 1; }
    export_secenekleri
    rm -f "$IPA"
    xcodebuild -exportArchive \
      -archivePath "$ARSIV" \
      -exportPath "$CIKTI" \
      -exportOptionsPlist "$CIKTI/ExportOptions.plist" \
      -allowProvisioningUpdates
    echo "IPA hazır: $IPA"
    ;;

  dogrula|yukle)
    [ -f "$IPA" ] || { echo "HATA: $IPA yok; önce '$0 ipa' çalıştırın." >&2; exit 1; }
    if [ -z "${ASC_KEY_ID:-}" ] || [ -z "${ASC_ISSUER_ID:-}" ]; then
      echo "HATA: ASC_KEY_ID ve ASC_ISSUER_ID tanımlı olmalı." >&2
      echo "App Store Connect > Users and Access > Integrations bölümünden API" >&2
      echo "anahtarı üretip .p8 dosyasını ~/.appstoreconnect/private_keys/ içine koyun." >&2
      exit 1
    fi
    EYLEM="validate-app"
    [ "$1" = "yukle" ] && EYLEM="upload-app"
    xcrun altool --"$EYLEM" \
      --type ios --file "$IPA" \
      --apiKey "$ASC_KEY_ID" --apiIssuer "$ASC_ISSUER_ID"
    ;;

  *)
    sed -n '2,16p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
    exit 1
    ;;
esac
