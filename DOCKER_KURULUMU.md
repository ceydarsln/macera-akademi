# Macera Akademi — Docker kurulumu

Bu yapı Macera Akademi'yi sunucudaki diğer uygulamalardan ayrı bir PHP/Apache
container içinde çalıştırır. Veritabanı için şirketin mevcut MySQL/MariaDB
sunucusu veya isteğe bağlı ayrı MySQL container kullanılabilir.

## Gereksinimler

- Docker Engine ve Docker Compose v2
- `maceraakademi.com.tr` için reverse proxy erişimi
- Canlı kullanımda geçerli HTTPS sertifikası

## Ortak hazırlık

```bash
git clone https://github.com/ceydarsln/macera-akademi.git
cd macera-akademi
cp .env.docker.example .env
```

`.env` içindeki örnek parolaları mutlaka değiştirin. Bu dosya Git tarafından
izlenmez ve mesajla paylaşılmamalıdır.

## Seçenek A — şirketin mevcut MySQL/MariaDB sunucusu

1. MySQL'de boş `macera_akademi` veritabanı ve yalnız bu veritabanına yetkili
   bir kullanıcı oluşturun.
2. `web/database/schema.sql` dosyasını bu veritabanına içe aktarın.
3. `.env` içindeki `MACERA_DB_HOST`, port, veritabanı adı, kullanıcı ve parolayı
   şirket sunucusuna göre düzenleyin.
4. Uygulamayı başlatın:

```bash
docker compose up -d --build app
```

MySQL aynı fiziksel sunucudaysa container içinden `127.0.0.1` kullanmayın.
Linux sunucuda Compose tarafından tanımlanan `host.docker.internal` adresi veya
sunucu yöneticisinin sağlayacağı Docker ağı/özel MySQL host adı kullanılmalıdır. MySQL'in
Docker ağından gelen bağlantılara izin vermesi gerekir.

## Seçenek B — ayrı MySQL container

`.env` içinde `MACERA_DB_HOST=db` kullanın ve iki servisi birlikte başlatın:

```bash
docker compose --profile bundled-db up -d --build
```

Şema, boş MySQL volume ilk oluşturulduğunda otomatik yüklenir. Daha önce oluşmuş
bir volume üzerinde şema dosyasını değiştirmek otomatik geçiş yapmaz; SQL
geçişleri ayrıca uygulanmalıdır.

## Kontrol

Sunucuda:

```bash
docker compose ps
curl http://127.0.0.1:8080/api/index.php?action=health
curl http://127.0.0.1:8080/api/teacher.php?action=health
```

Beklenen API yanıtında `ok: true` ve `database: mysql` bulunur. Hata incelemek
için:

```bash
docker compose logs --tail=200 app
```

## Domain, reverse proxy ve HTTPS

Container varsayılan olarak yalnızca sunucunun `127.0.0.1:8080` adresinde
dinler. Mevcut Nginx, Apache, Traefik veya şirket proxy'si şu hedefe
yönlendirilmelidir:

```text
maceraakademi.com.tr -> http://127.0.0.1:8080
```

HTTPS sertifikası reverse proxy üzerinde kurulmalı; HTTP istekleri HTTPS'e
yönlendirilmelidir. İstenirse `www.maceraakademi.com.tr` aynı hedefe bağlanır.
Öğrenci uygulaması `/`, öğretmen paneli ise aynı container'daki `/ogretmen/`
yolundan sunulur. Eski `maceraogretmen.netlify.app` adresine yönlendirme gerekmez.

## Güncelleme

```bash
git pull --ff-only origin main
docker compose up -d --build app
```

Ayrı MySQL container kullanılıyorsa `--profile bundled-db` seçeneğini koruyun.
MySQL volume'u uygulama container'ı yeniden oluşturulsa da kalır.

Bu öğretmen paneli güncellemesinden **önce kurulmuş** bir veritabanında aşağıdaki
geçiş dosyasını MySQL istemcisi veya phpMyAdmin ile bir kez uygulayın:

```text
web/database/migrations/2026-09-09-teacher-panel.sql
```

Yeni/boş kurulumlarda `schema.sql` tabloyu zaten oluşturduğu için ayrıca geçiş
çalıştırılmaz.

Canlı arkadaş yarışması için mevcut veritabanında önce yedek alın, sonra
`web/database/migrations/2026-09-30-live-matches.sql` dosyasını bir kez
uygulayın. Kodun container'a alınması tek başına mevcut MySQL volume'unu
güncellemez. İki hesaplı gerçek maç kabulü ayrıca gereklidir.

## Önemli sınırlar

- Öğrenci ve öğretmen paneli tek MySQL veritabanını kullanır.
- Mevcut Firebase kullanıcıları otomatik taşınmaz. Ayrıntılı plan
  `docs/FIREBASE_MYSQL_GECISI.md` dosyasındadır.
- Parolaları Dockerfile, Compose veya GitHub içine yazmayın; yalnız `.env` veya
  şirketin secret yönetimini kullanın.
