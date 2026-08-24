package com.maceraakademi.app;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
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
    /* Piper sesi (uygulamanın içinde gelen doğal Türkçe model). Hazırsa
       okuma ondan yapılır; kurulamazsa telefonun kendi motoruna düşülür. */
    private PiperSes piper;
    /* Chatterbox ile önceden üretilmiş kayıtlar — varsa ilk tercih. */
    private KayitliSes kayit;

    private TextToSpeech tts;
    private boolean ttsReady = false;
    private String ttsStatus = "notready";   // ok | missing | failed | notready
    private String ttsPending = null;        // motor hazır olmadan istenen metin
    private String ttsSesAdi = "";           // seçilen sesin adı (tanılama için)

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

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            WebView.setWebContentsDebuggingEnabled(false);
        }

        kayit = new KayitliSes();
        kayit.kur(this);
        piper = new PiperSes();
        piper.kur(this);
        setupTts();                      /* yedek: telefonun kendi motoru */
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
                    "  if(typeof state==='undefined') return 'exit';" +
                    "  if(state.purchaseConfirm){ closeBuyConfirm(); return 'handled'; }" +
                    "  if(state.confirmDelete){ state.confirmDelete=false; renderAll(); return 'handled'; }" +
                    "  if(state.friendModal){ closeFriendModal(); return 'handled'; }" +
                    "  if(state.screen==='gamePlayer'){ go('subjectList'); return 'handled'; }" +
                    "  if(state.screen==='messages'){ openFriends(); return 'handled'; }" +
                    "  if(state.screen==='subjectList'||state.screen==='soon'){ go('home'); return 'handled'; }" +
                    "  if(state.screen==='changePass'||state.screen==='diag'){ go('home'); return 'handled'; }" +
                    "  if(state.screen==='account'||state.screen==='settings'||state.screen==='friends'){ go('home'); return 'handled'; }" +
                    "  if(state.screen==='login'||state.screen==='register'||state.screen==='guestGrade'){ go('welcome'); return 'handled'; }" +
                    "  return 'exit';" +
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
                    return;
                }
                int res = tts.setLanguage(new Locale("tr", "TR"));
                if (res == TextToSpeech.LANG_MISSING_DATA || res == TextToSpeech.LANG_NOT_SUPPORTED) {
                    /* Türkçe ses paketi kurulu değil: uygulama çalışmaya devam eder,
                       kullanıcıya HTML tarafında bilgi verilir. */
                    ttsStatus = "missing";
                    return;
                }
                enIyiSesiSec();
                /* Robotik tonu yumuşatan ayarlar: hafif yavaş konuşma, doğal perde.
                   1.05 perde çocuk sesine benzetip mekanikleştiriyordu. */
                tts.setSpeechRate(0.92f);
                tts.setPitch(1.0f);
                ttsReady = true;
                ttsStatus = "ok";
                if (ttsPending != null) {
                    String t = ttsPending;
                    ttsPending = null;
                    tts.speak(t, TextToSpeech.QUEUE_FLUSH, null, "macera");
                }
            }
        });
    }

    /**
     * Cihazda birden çok Türkçe ses bulunur; varsayılan genelde en düşük
     * kaliteli sıkıştırılmış ses olur ve robotik duyulur. Kurulu Türkçe
     * sesleri kaliteye göre sıralayıp en iyisini seçiyoruz. Ağ sesleri
     * (Google'ın doğal sesleri) belirgin biçimde daha insana yakın, bu
     * yüzden eşit kalitede onlara öncelik veriyoruz — çevrimdışıyken
     * sistem kendiliğinden yerel sese düşüyor.
     */
    private void enIyiSesiSec() {
        try {
            if (Build.VERSION.SDK_INT < Build.VERSION_CODES.LOLLIPOP) return;
            Set<Voice> sesler = tts.getVoices();
            if (sesler == null || sesler.isEmpty()) return;

            Voice enIyi = null;
            int enIyiPuan = Integer.MIN_VALUE;
            for (Voice v : sesler) {
                if (v == null || v.getLocale() == null) continue;
                String dil = v.getLocale().getLanguage();
                if (!"tr".equalsIgnoreCase(dil)) continue;
                if (v.getFeatures() != null
                        && v.getFeatures().contains(TextToSpeech.Engine.KEY_FEATURE_NOT_INSTALLED)) continue;

                /* kalite baskın ölçüt; ağ sesi küçük bir artı */
                int puan = v.getQuality() * 10;
                if (v.isNetworkConnectionRequired()) puan += 3;
                /* "x-low" gibi düşük kaliteli varyantları geriye it */
                if (v.getName() != null && v.getName().contains("-low")) puan -= 50;

                if (puan > enIyiPuan) { enIyiPuan = puan; enIyi = v; }
            }
            if (enIyi != null) {
                tts.setVoice(enIyi);
                ttsSesAdi = enIyi.getName() + " (kalite " + enIyi.getQuality() + ")";
            }
        } catch (Exception e) {
            /* ses seçilemezse varsayılanla devam — okuma yine çalışır */
        }
    }

    /** HTML tarafına açılan tek arayüz. Sadece @JavascriptInterface işaretli
     *  metotlar erişilebilir; sayfa uygulamanın kendi assets klasöründen yüklenir. */
    private class TtsBridge {
        @JavascriptInterface
        public void speak(String text) {
            if (text == null || text.trim().isEmpty()) return;
            /* SIRA: 1) hazır kayıt (Chatterbox, en iyi kalite, sıfır işlem)
                      2) Piper (kayıt yoksa, cihazda üretir)
                      3) telefonun kendi sesi (Piper hazır değilse) */
            if (kayit != null && kayit.oku(MainActivity.this, text)) {
                if (piper != null) piper.durdur();
                if (tts != null) tts.stop();
                return;
            }
            if (piper != null && piper.hazirMi()) {
                if (tts != null) tts.stop();
                piper.oku(text);
                return;
            }
            if (!ttsReady || tts == null) {
                ttsPending = text;   /* motor henüz hazır değil: hazır olunca okunacak */
                return;
            }
            tts.stop();
            tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "macera");
        }

        @JavascriptInterface
        public void stop() {
            if (kayit != null) kayit.durdur();
            if (piper != null) piper.durdur();
            if (tts != null) tts.stop();
        }

        @JavascriptInterface
        public String status() {
            /* Piper hazırsa Türkçe ses her hâlükârda var. */
            if (piper != null && piper.hazirMi()) return "ok";
            return ttsStatus;
        }

        /** Hangi sesin seçildiğini görmek için (tanılama ekranı). */
        @JavascriptInterface
        public String voice() {
            if (kayit != null && !kayit.bosMu()) return "Chatterbox hazır kayıtlar";
            if (piper != null && piper.hazirMi()) return "Piper tr_TR-fahrettin (uygulama içi)";
            return ttsSesAdi.isEmpty() ? ("sistem sesi · " + ttsStatus) : ttsSesAdi;
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
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
