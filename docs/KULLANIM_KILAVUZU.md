# Macera Akademi kullanım kılavuzu

## Adresler

- Öğrenci uygulaması: `https://maceraakademi.com.tr/`
- Öğretmen paneli: `https://maceraakademi.com.tr/ogretmen/`
- Sistem kontrolü: `https://maceraakademi.com.tr/api/index.php?action=health`
- Öğretmen API kontrolü: `https://maceraakademi.com.tr/api/teacher.php?action=health`

## Öğretmen için ilk kullanım

1. Öğretmen panelini açın.
2. **Kayıt** sekmesinde ad-soyad, sınıf adı, sınıf düzeyi, kullanıcı adı ve en
   az sekiz karakterli şifreyi yazın.
3. **Hesap ve sınıf oluştur** düğmesine basın.
4. Panel otomatik olarak altı karakterli bir sınıf kodu gösterir.
5. **Kodu kopyala** ile kodu öğrencilerle paylaşın.

Eski Netlify/Firebase öğretmen hesabı MySQL hesabına otomatik dönüşmez. İlk
MySQL kurulumunda öğretmenin yeni panelden hesap açması gerekir.

## Öğrenciyi sınıfa bağlama

1. Öğrenci Macera Akademi hesabıyla giriş yapar.
2. Profil ekranını açar.
3. **Öğretmen Kodu** alanına öğretmenin verdiği kodu yazar ve kaydeder.
4. Kod geçerliyse öğretmen/sınıf bilgisi görünür.
5. Öğrencinin sonraki ilerleme kayıtları öğretmen panelindeki **Öğrenciler**
   sayfasına düşer.

Bir öğrenci görünmüyorsa önce doğru hesapla giriş yaptığını, kodu boşluksuz
girdiğini ve oyun tamamladıktan sonra internet bağlantısının olduğunu kontrol
edin.

## Ödev oluşturma

1. Öğretmen panelinde **Ödevler** sayfasını açın.
2. Sınıf düzeyi ve dersi seçin.
3. Konu gruplarındaki oyunları işaretleyin. İsterseniz görünen dersin bütün
   oyunlarını **Tümünü seç** ile seçin.
4. Başlık, isteğe bağlı teslim tarihi ve öğretmen notunu yazın.
5. **Ödevi gönder** düğmesine basın.

Öğrenciler aktif ödevi uygulamanın görevler bölümünde görür. Hazırlanan ödevin
yanındaki **Kim yaptı?** düğmesi her öğrencinin kaç oyunu tamamladığını gösterir.
Ödev **Kapat** ile görünmez yapılabilir veya **Sil** ile kalıcı kaldırılabilir.

## Yarışma açma

1. **Yarışmalar** sayfasını açın.
2. Sınıf düzeyi, günlük/haftalık tür, başlangıç tarihi ve konuyu seçin.
3. İsterseniz özel bir başlık yazın.
4. **Yarışmayı aç** düğmesine basın.

Günlük yarışma aynı gün, haftalık yarışma başlangıç günü dahil yedi gün açık
kalır. Her öğrenci aynı tohumla üretilen sekiz soruyu çözer. **Sıralama** düğmesi
puanları yüksekten düşüğe gösterir. Yarışma kapatılabilir veya silinebilir.

## Öğretmen ayarları

- **Profil ve sınıf:** öğretmen adı, e-posta, sınıf adı ve düzeyi güncellenir.
- **Şifre değiştir:** mevcut ve yeni şifre istenir. Diğer açık öğretmen
  oturumları kapatılır.
- **Sınıf kodunu yenile:** eski kod pasif olur, yeni kod oluşturulur. Eski veri
  silinmez; öğrencilerin yeni kodu profillerine yeniden yazması gerekir.
- **Oturumu kapat:** bu tarayıcıdaki öğretmen oturumu sona erer.

## Öğrenci kullanımı

1. Ana uygulamada hesap oluşturun veya giriş yapın.
2. Sınıf düzeyini seçip oyunları tamamlayın.
3. Profilde öğretmen kodunu kaydedin.
4. Görevler ekranından öğretmenin ödevlerini takip edin.
5. Yarışma Arenası'nda açık sınıf yarışmasına katılın.

Android/iOS uygulaması ile web sürümü aynı öğrenci API'sini kullanır. Aynı
kullanıcı adıyla giriş yapıldığında sunucudaki profil ve ilerleme açılır.

## Sunucu yöneticisi için hızlı kontrol

Kurulumdan sonra şu noktaları sırayla doğrulayın:

1. İki health adresi de `ok: true` dönüyor.
2. `/ogretmen/` altında deneme öğretmen hesabı açılabiliyor.
3. Üretilen sınıf kodu öğrenci profilinde kabul ediliyor.
4. Öğretmenin açtığı ödev öğrenci tarafında görünüyor.
5. Yarışma tamamlanınca öğretmen sıralaması güncelleniyor.
6. Container yeniden başlatıldığında hesaplar ve veriler duruyor.

Hata halinde `docker compose logs --tail=200 app` çıktısını kontrol edin.
Veritabanı bağlantısı hatalarında `.env` içindeki host, port, kullanıcı ve
parolayı; 404 hatalarında reverse proxy document root'unu kontrol edin.
