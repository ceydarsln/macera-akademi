# Macera Akademi — PHP/MySQL yayın kurulumu

Bu depo doğrudan sunucuya klonlanabilir. Canlı kullanıcı parolaları veya MySQL bağlantı bilgileri depoda bulunmaz.

Sunucuda başka uygulamalar da çalışıyorsa önerilen yöntem Docker kurulumudur.
Hazır container ve Compose adımları için [DOCKER_KURULUMU.md](DOCKER_KURULUMU.md)
dosyasını kullanın. Aşağıdaki adımlar Docker kullanılmayan klasik kurulum içindir.

## Gereksinimler

- PHP 7.4 veya üzeri
- PDO ve `pdo_mysql` PHP eklentileri
- MySQL 5.7+ veya güncel MariaDB
- Apache ya da PHP çalıştırabilen eşdeğer bir web sunucusu
- HTTPS sertifikası
- Sunucuda Git ve Bash (depo üzerinden güncelleme yapılacaksa)

## İlk kurulum

1. Depoyu sunucuya klonlayın.
2. Depo kökünde `./tools/aynala.sh` komutunu çalıştırın. Bu komut web oyunlarının çalıştırılabilir Phaser kopyalarını üretir ve mobil varlıkları eşitler.
3. Hosting panelinden UTF-8 uyumlu boş bir MySQL veritabanı ve yalnızca bu veritabanına yetkili bir kullanıcı oluşturun.
4. `web/database/schema.sql` dosyasını phpMyAdmin veya MySQL istemcisiyle içe aktarın.
5. `web/api/config.sample.php` dosyasını `web/api/config.local.php` adıyla kopyalayın.
6. `config.local.php` içindeki veritabanı adı, kullanıcı adı ve parolayı doldurun. Bu dosyayı commit etmeyin.
7. Alan adının document root'unu deponun `web/` klasörüne yönlendirin.
8. `https://maceraakademi.com.tr/api/index.php?action=health` adresini açın. `ok: true` ve `database: mysql` görülmelidir.
9. `https://maceraakademi.com.tr/api/teacher.php?action=health` adresinde de `ok: true` yanıtını doğrulayın.
10. `/ogretmen/` adresinde deneme öğretmen hesabı ve sınıf kodu oluşturun.
11. Ana sayfada deneme öğrenci hesabı açıp sınıf kodunu kaydedin; öğrencinin öğretmen panelinde göründüğünü kontrol edin.

## Güncelleme

Sunucuda, depo kökünde:

```bash
git pull --ff-only origin main
./tools/aynala.sh
```

Şema değişikliği varsa yeni SQL geçişi ayrıca uygulanmalıdır. `config.local.php` ve kullanıcı verileri Git tarafından değiştirilmez.

Bu öğretmen paneli güncellemesinden önce kurulmuş veritabanlarında
`web/database/migrations/2026-09-09-teacher-panel.sql` dosyasını bir kez
uygulayın. Yeni kurulumlar güncel `schema.sql` dosyasını kullandığı için buna
ihtiyaç duymaz.

## Güvenlik notları

- Siteyi yalnızca HTTPS üzerinden yayınlayın.
- `web/api/config.local.php` dosyasını hiçbir zaman GitHub'a yüklemeyin veya mesajla paylaşmayın.
- MySQL kullanıcısına başka veritabanları için yetki vermeyin.
- API parolaları PHP'nin `password_hash` fonksiyonuyla tek yönlü özetlenir.
- Mobil istemciler için oturumlar rastgele üretilen, veritabanında yalnızca özeti tutulan erişim belirteçleridir.
- Düzenli MySQL yedeği alın.

## Firebase'den veri geçişi

Bu kurulum yeni ve boş bir MySQL veritabanı oluşturur. Eski Firestore profil verileri ancak yetkili Firebase dışa aktarımı alındıktan sonra taşınabilir. Firebase Authentication parolaları düz metin olarak dışa aktarılamaz; canlı kullanıcılar varsa ayrıca hesap geçişi/parola yenileme planı yapılmalıdır. Dışa aktarım alınmadan Firebase projesini silmeyin.

## Öğretmen paneli

Öğretmen paneli bu deponun `web/ogretmen/` klasöründedir ve
`https://maceraakademi.com.tr/ogretmen/` yolundan açılır. Panel, öğrenci
uygulamasıyla aynı MySQL sınıf, ilerleme, ödev ve yarışma kayıtlarını kullanır.
Eski harici Netlify/Firebase öğretmen paneli canlı yayın için gerekli değildir.

Ayrıntılı mimari `docs/UYGULAMA_MIMARISI.md`, günlük kullanım adımları
`docs/KULLANIM_KILAVUZU.md` dosyasındadır.
