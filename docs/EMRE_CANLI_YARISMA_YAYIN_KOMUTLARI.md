# Emre için canlı yarışma yayın komutları

9 Ekim 2026. Bu dosya **canlı sunucuda çalıştırılmadı**; sunucu yöneticisinin kendi ortamında doğrulayıp uygulaması içindir. Depodaki eski notta Emre'nin Docker/MySQL ağ ayarını sağlayacağı yazıyor; sunucuyu gerçekten Emre'nin kurduğu yalnız bu nottan doğrulanamaz.

GitHub dalı: `codex/cuce-adimi-pilot`. Canlı yarışma kodu `14673586c2d3f1a492416833566fd00ed0d6e018` commit'inde. `main` dalına göre bu dal **onlarca commit ve yüzlerce dosya** ileridedir; yalnız yarışma değil, önceki oyun değişiklikleri de taşınır. Güncel sayı ön kontrol komutuyla görülür. Ceyda bu kapsamı onaylamadan canlıya almayın. Depodaki diğer kirli yerel dosyalar bu dala gönderilmedi.

## 1. Sunucuda salt-okunur ön kontrol

Komutları Macera Akademi depo kökünde, aynı Bash oturumunda çalıştırın:

```bash
git fetch origin
git status --short
git rev-parse HEAD
git rev-parse origin/main
git rev-parse origin/codex/cuce-adimi-pilot
git rev-list --count origin/main..origin/codex/cuce-adimi-pilot
git merge-base --is-ancestor 14673586c2d3f1a492416833566fd00ed0d6e018 origin/codex/cuce-adimi-pilot
docker compose ps
```

Son komut yalnız Docker kurulumunda kullanılır. `git status --short` beklenmedik değişiklik gösterirse önce Emre bunları korumalı; `reset --hard`, zorla `checkout` veya `push --force` kullanmayın. Sunucunun gerçekten bu depo/Docker Compose ile yayınlandığını ve doğru MySQL veritabanına bağlı olduğunu doğrulayın. Klasik PHP kurulumunda aşağıdaki Docker komutlarını çalıştırmayın.

## 2. Canlı veritabanını yedekle

Yedek klasörü depo ve web kökü **dışında**, yalnız yetkili yönetici tarafından okunabilir olmalı. `MACERA_YEDEK_KLASORU` örnek değerini gerçek güvenli mutlak yolla değiştirin. Parolayı komuta, Git'e veya sohbete yazmayın.

```bash
MACERA_YEDEK_KLASORU=/guvenli/yedek/klasoru
test -d "$MACERA_YEDEK_KLASORU" || exit 1
umask 077
MACERA_YEDEK_DOSYASI="$MACERA_YEDEK_KLASORU/macera-live-$(date -u +%Y%m%dT%H%M%SZ).sql"
```

**Seçenek A — Compose `bundled-db` MySQL container'ı kullanılıyorsa:**

```bash
docker compose --profile bundled-db exec -T db sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysqldump -uroot --single-transaction --routines --triggers --events --no-tablespaces "$MYSQL_DATABASE"' > "$MACERA_YEDEK_DOSYASI"
test -s "$MACERA_YEDEK_DOSYASI" || exit 1
```

**Seçenek B — şirketin ayrı MySQL/MariaDB sunucusu kullanılıyorsa:** Emre mevcut güvenli istemci yapılandırmasının yolunu ve veritabanı adını kendisi belirler. `--defaults-extra-file` ilk MySQL seçeneği olmalıdır.

```bash
MACERA_MYSQL_AYAR_DOSYASI=/guvenli/mysql-client.cnf
MACERA_DB_ADI=gercek_macera_veritabani_adi
test -f "$MACERA_MYSQL_AYAR_DOSYASI" || exit 1
mysqldump --defaults-extra-file="$MACERA_MYSQL_AYAR_DOSYASI" --single-transaction --routines --triggers --events --no-tablespaces "$MACERA_DB_ADI" > "$MACERA_YEDEK_DOSYASI"
test -s "$MACERA_YEDEK_DOSYASI" || exit 1
```

Yedek dosyasının **geri yüklenebilir** olduğunu Emre kendi yöntemiyle doğrulamadan devam etmeyin. Yedeği bu repoya veya ZIP'e koymayın.

## 3. Şema geçişini bir kez uygula

Geçiş dosyası: `web/database/migrations/2026-09-30-live-matches.sql`. Sunucunun mevcut `main` checkout'unda henüz bulunmayabilir; aşağıdaki `git show` komutu dosyayı **GitHub'dan çekilmiş yarışma dalından** okur. Önceki yedek başarılıysa ve doğru veritabanı doğrulandıysa yalnız uygun seçeneği çalıştırın.

```bash
git cat-file -e origin/codex/cuce-adimi-pilot:web/database/migrations/2026-09-30-live-matches.sql || exit 1
set -o pipefail
```

**Bundled DB:**

```bash
git show origin/codex/cuce-adimi-pilot:web/database/migrations/2026-09-30-live-matches.sql | docker compose --profile bundled-db exec -T db sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysql -uroot "$MYSQL_DATABASE"'
printf '%s\n' "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE() AND table_name IN ('live_matches','live_match_answers','live_match_claims');" | docker compose --profile bundled-db exec -T db sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysql -uroot -N "$MYSQL_DATABASE"'
```

**Şirket DB:**

```bash
git show origin/codex/cuce-adimi-pilot:web/database/migrations/2026-09-30-live-matches.sql | mysql --defaults-extra-file="$MACERA_MYSQL_AYAR_DOSYASI" "$MACERA_DB_ADI"
mysql --defaults-extra-file="$MACERA_MYSQL_AYAR_DOSYASI" -N "$MACERA_DB_ADI" -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE() AND table_name IN ('live_matches','live_match_answers','live_match_claims')"
```

Her iki durumda da son sayı **3** olmalı. `schema.sql` dosyasını mevcut dolu veritabanına yeniden içe aktarmayın.

## 4. Onaylanan Git dalını dağıt

Önce önceki commit'i kayıt altına alın. Aşağıdaki örnek, **Docker uygulama container'ı** için ve yalnız Ceyda geniş dal kapsamını onayladıktan sonra geçerlidir. Sunucunun kendi atomik yayın prosedürü varsa Emre onu tercih etsin.

```bash
MACERA_ONCEKI_COMMIT=$(git rev-parse HEAD)
printf 'Onceki commit: %s\n' "$MACERA_ONCEKI_COMMIT"
git fetch origin codex/cuce-adimi-pilot
git switch --detach origin/codex/cuce-adimi-pilot
docker compose up -d --build app
```

Bundled DB kullanan kurulumda mevcut profilin korunması gerekebilir: `docker compose --profile bundled-db up -d --build app`. **`docker compose down -v` çalıştırmayın; MySQL volume'unu silebilir.** Klasik PHP kurulumunda `git switch` doğrudan canlı document root üzerinde kısmi güncellemeye yol açabilir; Emre'nin mevcut sürümleme/atomik dağıtım yöntemini kullanın.

## 5. Canlı kabul ve geri alma

```bash
curl -fsS 'https://maceraakademi.com.tr/api/index.php?action=health'
curl -fsS 'https://maceraakademi.com.tr/' | grep -q 'macera-live-match-v1'
docker compose ps
docker compose logs --tail=100 app
```

İki ayrı, aynı sınıftaki test hesabıyla arkadaşlık → davet → kabul → hazır → **8 soru** → sonuç → ödülü oynayın. Geç/çift cevap, bağlantı kopması, geri dönüş, ayrılma ve ödülün ikinci kez verilmemesini de kontrol edin. `api/live.php` dosyasının doğrudan HTTP isteğine kapalı olması normaldir; çalışan API `api/index.php` üzerinden çağrılır. Sağlık yanıtı tek başına yarışmanın çalıştığını kanıtlamaz.

Kodda sorun çıkarsa, önceki commit'e dönerek **yalnız uygulama container'ını** yeniden kurun:

```bash
git switch --detach "$MACERA_ONCEKI_COMMIT"
docker compose up -d --build app
```

Eklenen DB tablolarını veya yedeği otomatik silmeyin. Veritabanını geri yükleme kararı, mevcut canlı veriyi kaybettirebileceğinden ayrı değerlendirilmelidir.

Emre'nin Ceyda'ya bildirmesi gerekenler: dağıtılan commit, veritabanı yedeğinin **alındığı/doğrulandığı** bilgisi (dosyanın kendisi değil), üç tablonun sonucu, iki hesaplı maç sonucu ve varsa geri alma durumu. Şifre, `.env`, SQL yedeği veya kullanıcı verisi paylaşılmasın.
