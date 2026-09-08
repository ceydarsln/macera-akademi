package com.maceraakademi.app;

import android.content.Context;
import android.content.res.AssetManager;
import android.media.AudioAttributes;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.util.Log;

import com.k2fsa.sherpa.onnx.GeneratedAudio;
import com.k2fsa.sherpa.onnx.OfflineTts;
import com.k2fsa.sherpa.onnx.OfflineTtsConfig;
import com.k2fsa.sherpa.onnx.OfflineTtsModelConfig;
import com.k2fsa.sherpa.onnx.OfflineTtsVitsModelConfig;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Piper sesi (sherpa-onnx üzerinden çalışan VITS modeli).
 *
 * NEDEN: Telefonun kendi metin okuma motoru cihaza göre değişiyor ve çoğu
 * cihazda sıkıştırılmış, robotik bir Türkçe ses veriyor. Piper modeli
 * uygulamanın içinde geldiği için her telefonda AYNI ve daha doğal ses
 * duyuluyor; internet de gerekmiyor.
 *
 * NASIL: Model dosyaları assets içinde geliyor ama espeak-ng sözlüklerini
 * gerçek dosya yolundan okuduğu için ilk açılışta bir kez cihazın kendi
 * klasörüne kopyalanıyor. Sonrasında her okuma isteği tek bir iş
 * kuyruğunda sesletilip AudioTrack ile çalınıyor.
 */
class PiperSes {

    private static final String ETIKET = "PiperSes";

    /* Ses modeli APK'ya gömülü (int8, 18 MB). Tam hassasiyetli sürüm 60 MB
       ve APK'yı 120 MB'a çıkarıyordu; tek seferlik 67 MB indirme de ağ
       kesintilerine açık olduğu için gömülü sürüm tercih edildi. */
    private static final String SURUM  = "fahrettin-fp32-v1";  /* kopyalama damgası */
    /* Ses seçimi: Türkçe için üç Piper sesi var (fettah, fahrettin, dfki).
       dfki ticari kullanıma kapalı (CC BY-NC-SA); fettah ve fahrettin CC0.
       fettah int8 sürümünde metalik duyulduğu için fahrettin sesine ve TAM
       hassasiyete (fp32) geçildi: int8 sıkıştırmasının çıtırtısı yok.
       fp16 denendi ama onnxruntime CPU'da float16 çıkışını kabul etmiyor
       ("Type (tensor(float16)) does not match expected type"). */

    private OfflineTts motor;
    private AudioTrack calar;
    private int ornekHizi = 22050;

    private final ExecutorService kuyruk = Executors.newSingleThreadExecutor();
    /** Her yeni istek nesli artırır; eski sesletme yarı yolda bırakılır. */
    private final AtomicInteger nesil = new AtomicInteger(0);

    private volatile boolean hazir = false;
    private volatile String durum = "kuruluyor";

    boolean hazirMi(){ return hazir; }
    String durum(){ return durum; }

    /* ---------------- kurulum ---------------- */

    void kur(final Context baglam){ kur(baglam, null); }

    void kur(final Context baglam, final Runnable hazirOlunca){
        kuyruk.execute(new Runnable(){
            @Override public void run(){
                try {
                    File kok = new File(baglam.getFilesDir(), "piper");
                    File damga = new File(kok, "surum-" + SURUM);
                    File modelDosya = new File(kok, "model.onnx");

                    /* espeak sözlükleri ve harf tablosu APK'dan bir kez kopyalanır */
                    if (!damga.exists()){
                        silAgac(kok);
                        kok.mkdirs();
                        kopyalaKlasor(baglam.getAssets(), "piper", kok);
                        new FileOutputStream(damga).close();
                    }

                    if (!modelDosya.exists()){
                        durum = "hata";
                        Log.w(ETIKET, "ses modeli bulunamadı");
                        return;
                    }

                    OfflineTtsVitsModelConfig vits = new OfflineTtsVitsModelConfig();
                    vits.setModel(new File(kok, "model.onnx").getAbsolutePath());
                    vits.setTokens(new File(kok, "tokens.txt").getAbsolutePath());
                    vits.setDataDir(new File(kok, "espeak-ng-data").getAbsolutePath());
                    /* Piper'ın önerdiği değerler; lengthScale 1'in üstü daha
                       yavaş ve çocuk için daha anlaşılır konuşma veriyor. */
                    vits.setNoiseScale(0.667f);
                    vits.setNoiseScaleW(0.8f);
                    vits.setLengthScale(1.08f);

                    OfflineTtsModelConfig model = new OfflineTtsModelConfig();
                    model.setVits(vits);
                    /* Çok çekirdek her zaman kazanç değil: küçük çekirdeklere dağılınca
                       yavaşlıyor. Cihazın çekirdek sayısına göre 2–4 arası. */
                    model.setNumThreads(Math.max(2,
                            Math.min(4, Runtime.getRuntime().availableProcessors() / 2)));
                    model.setDebug(false);
                    model.setProvider("cpu");

                    OfflineTtsConfig ayar = new OfflineTtsConfig();
                    ayar.setModel(model);

                    motor = new OfflineTts(null, ayar);
                    ornekHizi = motor.sampleRate();

                    /* ISINMA: ONNX ilk çağrıda grafiği kuruyor ve bu ilk
                       cümlede belirgin bir gecikme yapıyor. Sessizce kısa bir
                       cümle sesletip (çalmadan) motoru ısıtıyoruz; böylece
                       çocuğun duyduğu ilk yönerge anında geliyor. Süre ve
                       örnek sayısı günlüğe yazılıyor — cihazda hızın ölçüsü. */
                    long t0 = System.currentTimeMillis();
                    GeneratedAudio isinma = motor.generate("Merhaba, hazırım.", 0, 1.0f);
                    long sure = System.currentTimeMillis() - t0;
                    int ornek = (isinma != null && isinma.getSamples() != null)
                                ? isinma.getSamples().length : 0;

                    hazir = true;
                    durum = "hazir";
                    Log.i(ETIKET, "Piper hazır · örnek hızı " + ornekHizi
                          + " · ısınma " + sure + " ms, " + ornek + " örnek ("
                          + String.format("%.2f", ornek / (float) ornekHizi) + " sn ses)");
                    if (hazirOlunca != null) hazirOlunca.run();
                } catch (Throwable t){
                    hazir = false;
                    durum = "hata";
                    Log.w(ETIKET, "Piper kurulamadı: " + t);
                }
            }
        });
    }

    /* ---------------- okuma ---------------- */

    void oku(final String metin){
        if (metin == null || metin.trim().isEmpty()) return;
        final int benimNesil = nesil.incrementAndGet();
        synchronized (this){ kapatCalar(); }
        kuyruk.execute(new Runnable(){
            @Override public void run(){
                if (!hazir || motor == null) return;
                if (benimNesil != nesil.get()) return;      /* yenisi geldi */
                try {
                    final long t0 = System.currentTimeMillis();
                    baslatCalar(benimNesil);

                    /* AKIŞ KİPİ: cümlenin tamamı üretilene kadar beklemek uzun
                       yönergelerde saniyeler sürüyordu. sherpa parça parça ses
                       verdiği için üretilen ilk parçayı hemen çalıyoruz; ses
                       neredeyse anında başlıyor, gerisi arkadan yetişiyor.
                       AudioTrack tamponu dolduğunda write() beklediği için
                       üretim de kendiliğinden hıza uyuyor. */
                    final long[] ilkParca = { 0 };
                    final int[] toplamOrnek = { 0 };

                    /* Metni cümlelere bölüp sırayla sesletiyoruz. sherpa geri
                       çağrıyı cümle başına yaptığı için tek uzun cümlede ilk
                       ses ancak her şey üretilince geliyordu; kısa ilk cümle
                       ise anında duyuluyor ve gerisi çalarken üretiliyor. */
                    for (String cumle : cumlelereBol(metin)){
                        if (benimNesil != nesil.get()) return;
                        motor.generateWithCallback(cumle, 0, 1.0f,
                            new kotlin.jvm.functions.Function1<float[], Integer>(){
                                @Override public Integer invoke(float[] parca){
                                    if (benimNesil != nesil.get()) return 0;   /* yeni istek: bırak */
                                    if (ilkParca[0] == 0) ilkParca[0] = System.currentTimeMillis() - t0;
                                    toplamOrnek[0] += (parca == null ? 0 : parca.length);
                                    yazParca(parca, benimNesil);
                                    return 1;
                                }
                            });
                    }

                    Log.i(ETIKET, "okundu · ilk ses " + ilkParca[0] + " ms · toplam "
                          + (System.currentTimeMillis() - t0) + " ms · "
                          + String.format("%.1f", toplamOrnek[0] / (float) ornekHizi) + " sn: "
                          + metin.substring(0, Math.min(46, metin.length())));
                } catch (Throwable t){
                    Log.w(ETIKET, "sesletme hatası: " + t);
                }
            }
        });
    }

    /**
     * Metni cümlelere böler. Çok kısa parçalar (tek sözcük) tek başına
     * sesletilince tonlama bozulduğu için bir sonrakine ekleniyor.
     */
    private static java.util.List<String> cumlelereBol(String metin){
        java.util.List<String> liste = new java.util.ArrayList<>();
        StringBuilder tampon = new StringBuilder();
        for (int i = 0; i < metin.length(); i++){
            char c = metin.charAt(i);
            tampon.append(c);
            boolean son = (c == '.' || c == '!' || c == '?');
            boolean sonrasiBosluk = (i + 1 >= metin.length()) || metin.charAt(i + 1) == ' ';
            if (son && sonrasiBosluk && tampon.length() >= 16){
                liste.add(tampon.toString().trim());
                tampon.setLength(0);
            }
        }
        String kalan = tampon.toString().trim();
        if (!kalan.isEmpty()){
            if (kalan.length() < 12 && !liste.isEmpty())
                liste.set(liste.size() - 1, liste.get(liste.size() - 1) + " " + kalan);
            else liste.add(kalan);
        }
        if (liste.isEmpty()) liste.add(metin);
        return liste;
    }

    /** Akış için çaları hazırlar (yaklaşık yarım saniyelik tampon). */
    private void baslatCalar(int benimNesil){
        synchronized (this){
            if (benimNesil != nesil.get()) return;
            kapatCalar();
            int enAz = AudioTrack.getMinBufferSize(ornekHizi,
                    AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT);
            int tampon = Math.max(enAz, ornekHizi);      /* ~0,5 sn (16 bit) */
            calar = new AudioTrack.Builder()
                    .setAudioAttributes(new AudioAttributes.Builder()
                            .setUsage(AudioAttributes.USAGE_MEDIA)
                            .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                            .build())
                    .setAudioFormat(new AudioFormat.Builder()
                            .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                            .setSampleRate(ornekHizi)
                            .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                            .build())
                    .setBufferSizeInBytes(tampon)
                    .setTransferMode(AudioTrack.MODE_STREAM)
                    .build();
            calar.play();
        }
    }

    /** Üretilen ses parçasını 16 bit PCM'e çevirip çalara yazar. */
    private void yazParca(float[] ornekler, int benimNesil){
        if (ornekler == null || ornekler.length == 0) return;
        byte[] pcm = new byte[ornekler.length * 2];
        for (int i = 0; i < ornekler.length; i++){
            float o = ornekler[i];
            if (o > 1f) o = 1f; else if (o < -1f) o = -1f;
            short s = (short)(o * 32767f);
            pcm[i * 2]     = (byte)(s & 0xff);
            pcm[i * 2 + 1] = (byte)((s >> 8) & 0xff);
        }
        int yazildi = 0;
        while (yazildi < pcm.length){
            if (benimNesil != nesil.get()) return;
            AudioTrack c;
            synchronized (this){ c = calar; }
            if (c == null) return;
            int n = c.write(pcm, yazildi, pcm.length - yazildi);
            if (n <= 0) return;
            yazildi += n;
        }
    }

    void durdur(){
        /* Yalnız AudioTrack'i kapatmak yetmez: yerel model eski cümleyi
           üretmeye devam edip tek iş kuyruğunda sonraki oyunu bekletiyordu.
           Nesli artırınca callback ilk fırsatta üretimi de iptal eder. */
        nesil.incrementAndGet();
        synchronized (this){ kapatCalar(); }
    }

    private void kapatCalar(){
        if (calar == null) return;
        try { calar.pause(); calar.flush(); calar.stop(); } catch (Throwable ignored){}
        try { calar.release(); } catch (Throwable ignored){}
        calar = null;
    }

    void kapat(){
        durdur();
        kuyruk.execute(new Runnable(){
            @Override public void run(){
                try { if (motor != null){ motor.release(); motor = null; } } catch (Throwable ignored){}
            }
        });
        kuyruk.shutdown();
    }

    /* ---------------- assets → dosya sistemi ---------------- */

    private static void kopyalaKlasor(AssetManager am, String yol, File hedef) throws IOException {
        String[] icerik = am.list(yol);
        if (icerik == null || icerik.length == 0){        /* dosya */
            kopyalaDosya(am, yol, hedef);
            return;
        }
        if (!hedef.exists()) hedef.mkdirs();
        for (String ad : icerik){
            kopyalaKlasor(am, yol + "/" + ad, new File(hedef, ad));
        }
    }

    private static void kopyalaDosya(AssetManager am, String yol, File hedef) throws IOException {
        File ust = hedef.getParentFile();
        if (ust != null && !ust.exists()) ust.mkdirs();
        InputStream g = null; OutputStream c = null;
        try {
            g = am.open(yol);
            c = new FileOutputStream(hedef);
            byte[] tampon = new byte[65536];
            int n;
            while ((n = g.read(tampon)) > 0) c.write(tampon, 0, n);
        } finally {
            if (g != null) try { g.close(); } catch (IOException ignored){}
            if (c != null) try { c.close(); } catch (IOException ignored){}
        }
    }

    private static void silAgac(File f){
        if (f == null || !f.exists()) return;
        if (f.isDirectory()){
            File[] c = f.listFiles();
            if (c != null) for (File x : c) silAgac(x);
        }
        f.delete();
    }
}
