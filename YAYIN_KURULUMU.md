# Macera Akademi — PHP/MySQL yayın kurulumu

Bu depo doğrudan sunucuya klonlanabilir. Canlı kullanıcı parolaları veya MySQL bağlantı bilgileri depoda bulunmaz.

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
9. Ana sayfada deneme hesabı oluşturup çıkış/giriş ve ilerleme kaydını kontrol edin.

## Güncelleme

Sunucuda, depo kökünde:

```bash
git pull --ff-only origin main
./tools/aynala.sh
```

Şema değişikliği varsa yeni SQL geçişi ayrıca uygulanmalıdır. `config.local.php` ve kullanıcı verileri Git tarafından değiştirilmez.

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

Öğrenci uygulamasının sınıf, ödev ve yarışma tabloları MySQL şemasında hazırdır. Mevcut harici öğretmen paneli Firebase kullandığı için ayrıca PHP API'ye geçirilmeden bu tablolara veri yazamaz. Öğretmen paneli kaynakları bu depoda değildir; panel geçişi ayrı teslim edilmelidir.
