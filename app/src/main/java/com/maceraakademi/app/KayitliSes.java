package com.maceraakademi.app;

import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.media.AudioAttributes;
import android.media.MediaPlayer;
import android.util.Log;

import java.io.IOException;
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Set;

/**
 * Önceden üretilmiş konuşma kayıtlarını çalar.
 *
 * NEDEN: Telefonda çalışan sesletme motorları (sistem TTS, Piper) ya cihaza
 * göre değişiyor ya da robotik duyuluyor. Uygulamanın okuduğu cümleler ise
 * SABİT — müfredat metinleri. Bu yüzden hepsi Chatterbox ile bilgisayarda bir
 * kez üretilip uygulamaya konuyor: her telefonda aynı, en iyi kalitede ses,
 * hiç işlem yükü ve internet gerekmeden.
 *
 * NASIL: Dosya adı, okunacak metnin (uygulamadaki speechClean'den geçmiş
 * hâlinin) SHA-1 özetinin ilk 16 hanesi. Aynı hesap ses üretilirken de
 * yapıldığı için metinle kayıt birebir eşleşiyor. Kayıt bulunamazsa çağıran
 * taraf Piper'a düşüyor.
 */
class KayitliSes {

    private static final String ETIKET = "KayitliSes";
    private static final String KLASOR = "ses";

    private final Set<String> mevcut = new HashSet<>();
    private MediaPlayer calar;
    private volatile float ses = 1.0f;

    /** assets/ses içindeki kayıtların listesini bir kez okur. */
    void kur(Context baglam){
        try {
            String[] dosyalar = baglam.getAssets().list(KLASOR);
            if (dosyalar != null){
                for (String d : dosyalar){
                    if (d.endsWith(".ogg")) mevcut.add(d.substring(0, d.length() - 4));
                }
            }
            Log.i(ETIKET, mevcut.size() + " hazır kayıt bulundu");
        } catch (IOException e){
            Log.w(ETIKET, "kayıt listesi okunamadı: " + e);
        }
    }

    boolean bosMu(){ return mevcut.isEmpty(); }

    /** Metnin kaydı varsa çalar ve true döner; yoksa false (çağıran Piper'a düşer). */
    boolean oku(Context baglam, String metin){
        String id = kimlik(metin);
        if (id == null || !mevcut.contains(id)) return false;
        try {
            durdur();
            AssetFileDescriptor fd = baglam.getAssets().openFd(KLASOR + "/" + id + ".ogg");
            MediaPlayer mp = new MediaPlayer();
            mp.setAudioAttributes(new AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build());
            mp.setDataSource(fd.getFileDescriptor(), fd.getStartOffset(), fd.getLength());
            fd.close();
            mp.setOnCompletionListener(p -> { p.release(); if (calar == p) calar = null; });
            mp.prepare();
            mp.setVolume(ses, ses);
            mp.start();
            calar = mp;
            return true;
        } catch (Throwable t){
            Log.w(ETIKET, "kayıt çalınamadı (" + id + "): " + t);
            return false;
        }
    }

    void sesSeviyesi(float seviye){
        ses = Math.max(0f, Math.min(1f, seviye));
        MediaPlayer mp = calar;
        if (mp != null) try { mp.setVolume(ses, ses); } catch (Throwable ignored){}
    }

    void durdur(){
        MediaPlayer mp = calar;
        calar = null;
        if (mp == null) return;
        try { if (mp.isPlaying()) mp.stop(); } catch (Throwable ignored){}
        try { mp.release(); } catch (Throwable ignored){}
    }

    /** speechClean'den geçmiş metnin SHA-1 özetinin ilk 16 hanesi. */
    static String kimlik(String metin){
        if (metin == null) return null;
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-1");
            byte[] o = md.digest(metin.getBytes("UTF-8"));
            StringBuilder sb = new StringBuilder();
            for (byte b : o) sb.append(String.format("%02x", b));
            return sb.substring(0, 16);
        } catch (Exception e){
            return null;
        }
    }
}
