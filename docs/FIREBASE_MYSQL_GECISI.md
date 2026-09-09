# Firebase verilerini MySQL'e geçirme notu

## Şu anki durum

Yeni birleşik yayın öğrenci ve öğretmen işlemleri için tek MySQL veritabanını
kullanır. Eski Netlify öğretmen paneli ve geçmiş Firebase kayıtları çalışma
anında kullanılmaz. Buna rağmen Firebase'deki eski kullanıcılar ve ilerleme
verileri, yetkili bir dışa aktarım dosyası verilmediği için bu teslimde otomatik
olarak MySQL'e taşınmamıştır.

Bu durum yeni kurulumun çalışmasına engel değildir. Yeni hesaplar, ödevler ve
yarışmalar MySQL'de oluşturulur. Eski veriler de gösterilecekse aşağıdaki ayrı
geçiş yapılmalıdır.

## Neden iki veritabanını canlıda birleştirmiyoruz?

Firebase ile MySQL'i aynı anda yazılabilir tutmak veri çakışması, çift kayıt ve
hangi kaynağın doğru olduğu sorununu üretir. Canlı sistemde tek doğruluk kaynağı
MySQL olmalıdır. Firebase yalnızca geçici, salt okunur göç kaynağı olarak
kullanılmalıdır.

## Gerekli girdiler

- Projenin gerçek sahibi tarafından alınmış Firebase Authentication kullanıcı
  dışa aktarımı
- Firestore koleksiyon dışa aktarımı: kullanıcı profilleri, sınıflar,
  ilerlemeler, ödevler, yarışmalar ve puanlar
- Dışa aktarımın alındığı kesin tarih/saat
- Aynı kullanıcı adlarının nasıl birleştirileceğine dair onaylı kural
- Taşıma öncesi MySQL yedeği

Gerçek Firebase servis hesabı, API anahtarı veya MySQL parolası repoya
eklenmemeli ve mesajla paylaşılmamalıdır.

## Önerilen geçiş sırası

1. Firebase yazımlarını kısa süreli bakım moduna alın.
2. Auth ve Firestore dışa aktarımlarını alın; dosya sayılarını ve özetlerini
   kaydedin.
3. MySQL'in yedeğini alın.
4. Dışa aktarımı önce geçici tablolara yükleyin.
5. Kullanıcı adlarını `username_key` kuralına göre normalize edip çakışmaları
   raporlayın; otomatik olarak üstüne yazmayın.
6. Sınıfları ve öğretmenleri, sonra öğrencileri, ilerlemeyi, ödevleri,
   yarışmaları ve puanları dış anahtar sırasına göre aktarın.
7. Kayıt adetleri ve örnek kullanıcılar üzerinden karşılaştırma yapın.
8. Öğretmen ve öğrenci uçtan uca testlerini tamamlayın.
9. MySQL'i tek yazılabilir kaynak olarak açın; Firebase'i doğrulama süresi
   boyunca salt okunur yedek olarak tutun.

## Parolalar

Firebase Authentication parolaları düz metin olarak dışa aktarılamaz ve PHP'nin
`password_hash` biçimine doğrudan çevrilemez. Güvenli varsayılan yöntem, taşınan
hesaplar için parola yenileme akışı uygulamak veya kullanıcıların yeni MySQL
hesabı açmasını sağlamaktır. Parolaları tahmin etmeye, düz metin istemeye veya
geçici ortak parola atamaya çalışmayın.

## Bu teslimde tamamlanan kısım

- Öğretmen paneli `/ogretmen/` yolunda aynı uygulamaya alındı.
- Öğretmen ve öğrenci tarafı aynı MySQL sınıf/ödev/yarışma tablolarına bağlandı.
- Yeni kurulum şeması ve mevcut kurulum için öğretmen oturum tablosu geçişi
  eklendi.
- Firebase yapılandırması veya gizli anahtar öğretmen paneline taşınmadı.

Veri dışa aktarımı geldiğinde ayrıca tek kullanımlık, tekrar çalıştırılabilir ve
önce kuru koşu raporu üreten bir aktarım aracı hazırlanmalıdır.
