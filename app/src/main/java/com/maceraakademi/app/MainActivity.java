package com.maceraakademi.app;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.media.AudioAttributes;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.speech.tts.TextToSpeech;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Toast;

import java.util.Locale;
import java.util.Set;
import java.util.concurrent.atomic.AtomicInteger;

import android.speech.tts.Voice;

import androidx.activity.OnBackPressedCallback;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.webkit.WebViewAssetLoader;
import androidx.webkit.WebViewClientCompat;

/**
 * Macera Akademi — tüm oyun tek bir HTML dosyasında (assets/macera-akademi.html).
 *
 * ÖNEMLİ: Dosya "file://" olarak YÜKLENMEZ.
 * WebViewAssetLoader kullanılarak yerel dosya
 *     https://appassets.androidplatform.net/assets/...
 * adresinden sunulur. Böylece sayfa gerçek bir https kaynağına sahip olur ve:
 *   • Firestore (Firebase veritabanı) bağlantısı kurabilir
 *   • IndexedDB / yerel depolama çalışır (oturum ve çevrimdışı önbellek)
 *   • Tarayıcının "file://" kısıtlamaları devreye girmez
 * "file://" ile yüklendiğinde Firebase veri okuma/yazma işlemleri sessizce
 * askıda kalıyordu; bu yüzden bu yöntem tercih edildi.
 */
public class MainActivity extends AppCompatActivity {

    private static final String BASE_URL =
            "https://appassets.androidplatform.net/assets/macera-akademi.html";
    /** Ana uygulama sayfası — geri tuşu mantığı buna göre değişiyor. */
    private static final String ANA_SAYFA = "macera-akademi.html";
    /** Uygulamanın kendi sayfasının sunulduğu alan adı. Bunun dışındaki
     *  adresler sistem tarayıcısına yönlendirilir. */
    private static final String APP_HOST = "appassets.androidplatform.net";

    private WebView web;
    private OnBackPressedCallback geriCallback;

    /* ---- Sesli okuma ----
       Android WebView'in kendi konuşma motoru (speechSynthesis) sessiz kalıyor.
       Bu yüzden telefonun yerleşik Türkçe metin okuma motoruna köprü kuruyoruz;
       HTML tarafı window.AndroidTTS.speak(...) çağırıyor. */
    /* Piper sesi (uygulamanın içinde gelen doğal Türkçe model). Sistem TTS
       kullanılamıyorsa yedek olarak tembel başlatılır. */
    private PiperSes piper;
    private boolean piperBaslatildi = false;
    /* Chatterbox ile önceden üretilmiş kayıtlar — varsa ilk tercih. */
    private KayitliSes kayit;

    private TextToSpeech tts;
    private volatile boolean ttsReady = false;
    private volatile String ttsStatus = "notready";   // ok | missing | failed | notready
    private volatile String ttsPending = null;        // motor hazır olmadan istenen son metin
    private volatile int ttsPendingNesli = 0;
    private volatile float sesSeviyesi = 1.0f;
    private String ttsSesAdi = "";           // seçilen sesin adı (tanılama için)
    /** Ekran/oyun değişince UI kuyruğunda bekleyen ses görevlerini de geçersiz kılar. */
    private final AtomicInteger sesNesli = new AtomicInteger(0);

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Çocuk oynarken ekran kapanmasın
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        web = new WebView(this);
        setContentView(web);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);               // oturum + ilerleme
        s.setDatabaseEnabled(true);
        s.setLoadWithOverviewMode(true);
        s.setUseWideViewPort(false);
        s.setSupportZoom(false);
        s.setBuiltInZoomControls(false);
        s.setMediaPlaybackRequiresUserGesture(false); // sesli direktifler
        s.setCacheMode(WebSettings.LOAD_DEFAULT);
        s.setTextZoom(100);                          // sistem yazı boyutu düzeni bozmasın
        // Asset loader kullandığımız için dosya erişimine gerek yok (daha güvenli)
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);

        // Yerel dosyaları https kaynağı gibi sun
        final WebViewAssetLoader assetLoader = new WebViewAssetLoader.Builder()
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();

        web.setWebViewClient(new WebViewClientCompat() {
            @Override
            public WebResourceResponse shouldInterceptRequest(@NonNull WebView view,
                                                             @NonNull WebResourceRequest request) {
                return assetLoader.shouldInterceptRequest(request.getUrl());
            }

            /* Uygulama kendi sayfası dışına gitmeye çalışırsa (örn. karşılama
               ekranındaki "Öğretmen misiniz?" bağlantısı) sayfayı WebView'in
               içinde açmıyoruz — aksi hâlde kullanıcı adres çubuğu ve sekmesi
               olmayan bir pencerede sıkışıp kalır. Sistem tarayıcısına
               devrediyoruz; oyun ekranı olduğu gibi arkada kalır. */
            @Override
            public boolean shouldOverrideUrlLoading(@NonNull WebView view,
                                                    @NonNull WebResourceRequest request) {
                Uri url = request.getUrl();
                if (url == null) return false;
                if (APP_HOST.equals(url.getHost())) return false;   // kendi sayfamız: WebView yüklesin
                try {
                    Intent i = new Intent(Intent.ACTION_VIEW, url);
                    i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    startActivity(i);
                } catch (Exception e) {
                    /* Uygun uygulama yok (örn. SIM'siz tablette telefon yok).
                       Sessiz kalmak yerine adresi kullanıcıya göster. */
                    String s = url.getSchemeSpecificPart();
                    Toast.makeText(MainActivity.this,
                            (s != null && !s.isEmpty() ? s : url.toString()),
                            Toast.LENGTH_LONG).show();
                }
                return true;   // WebView bu adresi yüklemesin
            }
        });

        web.setBackgroundColor(0xFF241A3D);
        web.setOverScrollMode(View.OVER_SCROLL_NEVER);

        WebView.setWebContentsDebuggingEnabled(false);

        kayit = new KayitliSes();
        kayit.kur(this);
        piper = new PiperSes();
        setupTts();                      /* hızlı ve tekrar çağrılabilir ana motor */
        web.addJavascriptInterface(new TtsBridge(), "AndroidTTS");

        web.loadUrl(BASE_URL);

        /* Geri tuşu:
           • Phaser oyunları ve başlangıç ekranı gibi sayfalarda WebView'in kendi
             geçmişi kullanılır (oyundan listeye, listeden başlangıca döner).
           • Ana uygulamada eski JS mantığı çalışır; en üst ekranda geri basılırsa
             uygulamadan çıkmak yerine başlangıç ekranına döner. */
        geriCallback = new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                String adres = web != null ? web.getUrl() : null;
                if (adres == null || !adres.contains(ANA_SAYFA)) {
                    geriGitVeyaCik();
                    return;
                }
                web.evaluateJavascript(
                    "(function(){try{" +
                    "  return typeof androidGeriTusu==='function' ? androidGeriTusu() : 'exit';" +
                    "}catch(e){ return 'exit'; }})()",
                    value -> {
                        if (value == null || value.contains("exit")) geriGitVeyaCik();
                    });
            }
        };
        getOnBackPressedDispatcher().addCallback(this, geriCallback);
    }

    /** Geçmişte gidilecek sayfa varsa oraya döner, yoksa uygulamadan çıkar. */
    private void geriGitVeyaCik() {
        if (web != null && web.canGoBack()) {
            web.goBack();
            return;
        }
        if (geriCallback != null) geriCallback.setEnabled(false);
        getOnBackPressedDispatcher().onBackPressed();
    }

    private void setupTts() {
        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status != TextToSpeech.SUCCESS) {
                    ttsStatus = "failed";
                    piperBaslat();
                    return;
                }
                int res = tts.setLanguage(new Locale("tr", "TR"));
                if (res == TextToSpeech.LANG_MISSING_DATA || res == TextToSpeech.LANG_NOT_SUPPORTED) {
                    /* Türkçe ses paketi kurulu değil: uygulama çalışmaya devam eder,
                    kullanıcıya HTML tarafında bilgi verilir. */
                    ttsStatus = "missing";
                    piperBaslat();
                    return;
                }
                enIyiSesiSec();
                /* Robotik tonu yumuşatan ayarlar: hafif yavaş konuşma, doğal perde.
                   1.05 perde çocuk sesine benzetip mekanikleştiriyordu. */
                tts.setSpeechRate(0.92f);
                tts.setPitch(1.0f);
                tts.setAudioAttributes(new AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_ASSISTANCE_ACCESSIBILITY)
                        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                        .build());
                ttsReady = true;
                ttsStatus = "ok";
                if (ttsPending != null) {
                    String t = ttsPending;
                    int n = ttsPendingNesli;
                    ttsPending = null;
                    sistemSesiniOku(t, n);
                }
            }
        });
    }

    /**
     * Cihazda birden çok Türkçe ses bulunur; varsayılan genelde en düşük
     * kaliteli sıkıştırılmış ses olur ve robotik duyulur. Kurulu Türkçe
     * sesleri kaliteye göre sıralayıp en iyi YEREL sesi seçiyoruz. Ağ sesi
     * daha doğal olabilse de her yönergede saniyelerce bağlantı bekletebilir;
     * oyun içi yönlendirmede düşük gecikme ve çevrimdışı çalışma önceliklidir.
     */
    private void enIyiSesiSec() {
        try {
            Set<Voice> sesler = tts.getVoices();
            if (sesler == null || sesler.isEmpty()) return;

            Voice enIyiYerel = null;
            Voice enIyiAg = null;
            int enIyiYerelPuan = Integer.MIN_VALUE;
            int enIyiAgPuan = Integer.MIN_VALUE;
            for (Voice v : sesler) {
                if (v == null || v.getLocale() == null) continue;
                String dil = v.getLocale().getLanguage();
                if (!"tr".equalsIgnoreCase(dil)) continue;
                if (v.getFeatures() != null
                        && v.getFeatures().contains(TextToSpeech.Engine.KEY_FEATURE_NOT_INSTALLED)) continue;

                /* Kalite baskın ölçüt; yerel ve ağ sesleri ayrı sıralanır. */
                int puan = v.getQuality() * 10;
                /* "x-low" gibi düşük kaliteli varyantları geriye it */
                if (v.getName() != null && v.getName().contains("-low")) puan -= 50;

                if (v.isNetworkConnectionRequired()) {
                    if (puan > enIyiAgPuan) { enIyiAgPuan = puan; enIyiAg = v; }
                } else if (puan > enIyiYerelPuan) {
                    enIyiYerelPuan = puan;
                    enIyiYerel = v;
                }
            }
            Voice enIyi = enIyiYerel != null ? enIyiYerel : enIyiAg;
            if (enIyi != null) {
                tts.setVoice(enIyi);
                ttsSesAdi = enIyi.getName() + " (kalite " + enIyi.getQuality() + ")";
            }
        } catch (Exception e) {
            /* ses seçilemezse varsayılanla devam — okuma yine çalışır */
        }
    }

    /** Sistem motorunu ana iş parçacığında, her çağrıda benzersiz bir kimlikle
     *  başlatır. Bu yol hazırlanmış sistem motorunda tekrar düğmesine anında
     *  yanıt verir; sabit utterance kimliği kullanan motor önbellekleri de
     *  ikinci çağrıyı yutamaz. */
    private void sistemSesiniOku(final String metin, final int istekNesli) {
        runOnUiThread(() -> {
            if (istekNesli != sesNesli.get()) return;
            if (!ttsReady || tts == null) {
                ttsPendingNesli = istekNesli;
                ttsPending = metin;
                return;
            }
            if (kayit != null) kayit.durdur();
            if (piper != null) piper.durdur();
            tts.stop();
            Bundle ayarlar = new Bundle();
            ayarlar.putFloat(TextToSpeech.Engine.KEY_PARAM_VOLUME, sesSeviyesi);
            int sonuc = tts.speak(metin, TextToSpeech.QUEUE_FLUSH, ayarlar,
                    "macera-" + System.nanoTime());
            if (sonuc == TextToSpeech.ERROR) {
                ttsReady = false;
                ttsStatus = "failed";
                ttsPendingNesli = istekNesli;
                ttsPending = metin;
                piperBaslat();
            }
        });
    }

    /** Piper pahalı model kopyalama/ısınmasını yalnız sistem TTS gerçekten
     *  kullanılamadığında yapar. Hazır olduğunda en son bekleyen yönergeyi
     *  okur; eski oyunlardan kalan metinler stop() tarafından temizlenir. */
    private synchronized void piperBaslat() {
        if (piperBaslatildi || piper == null) return;
        piperBaslatildi = true;
        piper.kur(this, () -> {
            String bekleyen = ttsPending;
            int n = ttsPendingNesli;
            if (bekleyen == null || n != sesNesli.get()
                    || piper == null || !piper.hazirMi()) return;
            ttsPending = null;
            piper.oku(bekleyen);
        });
    }

    /** HTML tarafına açılan tek arayüz. Sadece @JavascriptInterface işaretli
     *  metotlar erişilebilir; sayfa uygulamanın kendi assets klasöründen yüklenir. */
    private class TtsBridge {
        @JavascriptInterface
        public void speak(String text) {
            if (text == null || text.trim().isEmpty()) return;
            final int istekNesli = sesNesli.incrementAndGet();
            /* SIRA: 1) hazır kayıt (varsa sıfır üretim)
                      2) yerel sistem TTS (anlık ve tekrar çağrılabilir)
                      3) Piper (sistem Türkçe sesi yoksa çevrimdışı yedek) */
            if (kayit != null && kayit.oku(MainActivity.this, text)) {
                if (piper != null) piper.durdur();
                if (tts != null) tts.stop();
                return;
            }
            if (ttsReady && tts != null) {
                sistemSesiniOku(text, istekNesli);
                return;
            }
            if (piper != null && piper.hazirMi()) {
                if (tts != null) tts.stop();
                piper.oku(text);
                return;
            }
            ttsPendingNesli = istekNesli;
            ttsPending = text;       /* motor hazır olunca yalnız son istek okunur */
            if (!"notready".equals(ttsStatus)) piperBaslat();
        }

        @JavascriptInterface
        public void setVolume(double level) {
            sesSeviyesi = (float) Math.max(0.0, Math.min(1.0, level));
            if (kayit != null) kayit.sesSeviyesi(sesSeviyesi);
            if (piper != null) piper.sesSeviyesi(sesSeviyesi);
        }

        @JavascriptInterface
        public void stop() {
            final int durdurmaNesli = sesNesli.incrementAndGet();
            ttsPending = null;
            if (kayit != null) kayit.durdur();
            if (piper != null) piper.durdur();
            runOnUiThread(() -> {
                if (durdurmaNesli == sesNesli.get() && tts != null) tts.stop();
            });
        }

        @JavascriptInterface
        public String status() {
            if (ttsReady) return "ok";
            if (piper != null && piper.hazirMi()) return "ok";
            return ttsStatus;
        }

        /** Hangi sesin seçildiğini görmek için (tanılama ekranı). */
        @JavascriptInterface
        public String voice() {
            if (kayit != null && !kayit.bosMu()) return "Chatterbox hazır kayıtlar";
            if (ttsReady)
                return ttsSesAdi.isEmpty() ? "yerel sistem sesi" : ttsSesAdi;
            if (piper != null && piper.hazirMi()) return "Piper tr_TR-fahrettin (uygulama içi)";
            return ttsSesAdi.isEmpty() ? ("sistem sesi · " + ttsStatus) : ttsSesAdi;
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        sesNesli.incrementAndGet();
        ttsPending = null;
        if (kayit != null) kayit.durdur();
        if (piper != null) piper.durdur();
        if (tts != null) tts.stop();
        if (web != null) web.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (web != null) web.onResume();
    }

    @Override
    protected void onDestroy() {
        if (piper != null) { piper.kapat(); piper = null; }
        if (tts != null) {
            tts.stop();
            tts.shutdown();
            tts = null;
        }
        if (web != null) {
            web.loadUrl("about:blank");
            web.destroy();
            web = null;
        }
        super.onDestroy();
    }
}
