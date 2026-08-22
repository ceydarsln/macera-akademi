# -*- coding: utf-8 -*-
"""
Chatterbox Multilingual V3 ile Türkçe ses dosyalarını üretir.

Kullanım:
    .venv/bin/python uret.py [--limit N] [--ref referans.wav] [--baslangic N]

Her cümle için  ses/<kimlik>.wav  üretir; var olan dosyayı atlar, böylece
yarıda kesilse kaldığı yerden devam eder. Sonra ogg_yap.sh ile Opus'a
çevrilip uygulamaya konur.
"""
import argparse, io, json, os, sys, time
os.environ.setdefault('TQDM_DISABLE', '1')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import torch
import torchaudio as ta
try:
    import soundfile as sf
except ImportError:
    sys.exit('soundfile gerekli:  .venv/bin/python -m pip install soundfile')
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

KOK = os.path.dirname(os.path.abspath(__file__))
CIKTI = os.path.join(KOK, 'ses')
HEDEF_HZ = 16000

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0, help='kaç cümle üretilecek (0 = hepsi)')
    ap.add_argument('--baslangic', type=int, default=0)
    ap.add_argument('--ref', default='', help='ses klonlama için referans kayıt (wav)')
    ap.add_argument('--parca', type=int, default=0, help='bu işçinin numarası')
    ap.add_argument('--toplam', type=int, default=1, help='kaç işçi paralel çalışıyor')
    ap.add_argument('--exaggeration', type=float, default=0.45)
    ap.add_argument('--cfg', type=float, default=0.5)
    a = ap.parse_args()

    os.makedirs(CIKTI, exist_ok=True)
    kayitlar = json.load(io.open(os.path.join(KOK, 'manifest.json'), encoding='utf-8'))
    if a.baslangic: kayitlar = kayitlar[a.baslangic:]
    if a.limit:     kayitlar = kayitlar[:a.limit]
    # İş paralel işçilere bölünüyor: her işçi kendi payını üretiyor, ortak
    # klasöre yazıyorlar. Dosya adı içerikten türediği için çakışma olmuyor.
    if a.toplam > 1:
        kayitlar = [k for i, k in enumerate(kayitlar) if i % a.toplam == a.parca]
        print(f'işçi {a.parca+1}/{a.toplam} · payı {len(kayitlar)} cümle')

    aygit = 'mps' if torch.backends.mps.is_available() else 'cpu'
    print('Aygıt:', aygit, '· torch', torch.__version__)
    print('Model yükleniyor (ilk çalıştırmada indirilir)…')
    model = ChatterboxMultilingualTTS.from_pretrained(device=aygit, t3_model='v3')
    print('Model hazır · örnek hızı', model.sr)

    ek = {}
    if a.ref:
        ek['audio_prompt_path'] = a.ref
        print('Referans ses:', a.ref)

    t0 = time.time()
    uretilen = atlanan = 0
    toplam_ses = 0.0
    for i, k in enumerate(kayitlar, 1):
        hedef = os.path.join(CIKTI, k['id'] + '.ogg')
        if os.path.exists(hedef) and os.path.getsize(hedef) > 2000:
            atlanan += 1
            continue
        try:
            wav = model.generate(k['metin'], language_id='tr',
                                 exaggeration=a.exaggeration, cfg_weight=a.cfg, **ek)
            ses = wav.cpu()
            if ses.dim() > 1:
                ses = ses.mean(dim=0, keepdim=True)      # tek kanala indir
            toplam_ses += ses.shape[-1] / model.sr
            # Konuşma için 16 kHz yeterli; dosya boyutunu yarıya indiriyor.
            # ffmpeg olmadığı için OGG/Vorbis doğrudan soundfile ile yazılıyor;
            # Android Vorbis'i yerel olarak çalıyor.
            if model.sr != HEDEF_HZ:
                ses = ta.functional.resample(ses, model.sr, HEDEF_HZ)
            sf.write(hedef, ses.squeeze(0).numpy(), HEDEF_HZ,
                     format='OGG', subtype='VORBIS')
            uretilen += 1
        except Exception as e:
            print('  ✗', k['id'], repr(e)[:120])
            continue
        if uretilen % 10 == 0:
            gecen = time.time() - t0
            hiz = toplam_ses / gecen if gecen else 0
            kalan = len(kayitlar) - i
            print(f'  {i}/{len(kayitlar)} · üretilen {uretilen} · '
                  f'{toplam_ses/60:.1f} dk ses · {hiz:.2f}x gerçek zaman · '
                  f'kalan tahmini {kalan*(gecen/max(1,uretilen))/60:.0f} dk')
    print(f'BİTTİ · üretilen {uretilen} · atlanan {atlanan} · '
          f'{toplam_ses/60:.1f} dakika ses · {(time.time()-t0)/60:.1f} dakika sürdü')

if __name__ == '__main__':
    main()
