# -*- coding: utf-8 -*-
"""
Uygulamanın okuduğu bütün cümleleri çıkarır ve her birine kimlik verir.

Kimlik = temizlenmiş metnin SHA-1'inin ilk 16 hanesi. Uygulama çalışma anında
AYNI temizleyiciden geçirip AYNI kimliği hesaplıyor; ses dosyası adı da bu
kimlik. İkisi birebir aynı olmazsa kayıt bulunamaz, o yüzden aşağıdaki
temizleyici macera-akademi'deki speechClean ile satır satır eşleştirildi.
"""
import hashlib, io, json, re, sys

KAYNAK = '/Users/ceyda/Downloads/macera-akademi-firebase-11.html'

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿←-⇿⌀-⏿"
    "■-◿⬀-⯿\U0001F1E6-\U0001F1FF️‍⃣]")

def temizle(metin):
    t = metin if metin is not None else ''
    t = re.sub(r'<br\s*/?>', '. ', t, flags=re.I)
    t = re.sub(r'</(p|div|li|h\d)>', '. ', t, flags=re.I)
    t = re.sub(r'<[^>]*>', ' ', t)
    t = t.replace('&nbsp;', ' ').replace('&amp;', ' ve ')
    t = re.sub(r'&[a-z]+;', ' ', t, flags=re.I)
    t = EMOJI.sub(' ', t)
    t = re.sub(r'(\d)\s*[×x]\s*(\d)', r'\1 çarpı \2', t, flags=re.I)
    t = re.sub(r'(\d)\s*÷\s*(\d)', r'\1 bölü \2', t)
    t = re.sub(r'(\d)\s*/\s*(\d)', r'\1 bölü \2', t)
    t = re.sub(r'(\d)\s*\+\s*(\d)', r'\1 artı \2', t)
    t = re.sub(r'(\d)\s*[−–]\s*(\d)', r'\1 eksi \2', t)
    t = re.sub(r'=\s*\?', ' kaç eder?', t)
    t = re.sub(r'\s=\s', ' eşittir ', t)
    t = t.replace('%', ' yüzde ')
    t = re.sub(r'[·•]', ', ', t)
    t = re.sub(r'\s[—–]\s', ', ', t)
    t = re.sub(r'[“”„»«]', '', t)
    t = re.sub(r'\.{3,}', ', ', t)
    t = t.replace('…', ', ')
    t = re.sub(r'\s+([,.!?])', r'\1', t)
    t = re.sub(r'([,.!?])\1+', r'\1', t)
    t = re.sub(r',\s*([.!?])', r'\1', t)
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'[,\s]+$', '', t)
    t = t.strip()
    if t and not re.search(r'[.!?]$', t):
        t += '.'
    return t

def kimlik(temiz):
    return hashlib.sha1(temiz.encode('utf-8')).hexdigest()[:16]

ALANLAR = ['speak', 'say', 'orderSay', 'okSay', 'revealSay']

def cikar():
    s = io.open(KAYNAK, encoding='utf-8').read()
    bulunan = []
    for alan in ALANLAR:
        for m in re.finditer(r"\b" + alan + r"\s*:\s*'((?:[^'\\]|\\.)*)'", s):
            ham = m.group(1)
            ham = ham.replace("\\'", "'").replace('\\"', '"').replace('\\n', ' ')
            ham = re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), ham)
            bulunan.append((alan, ham))
    kayitlar, gorulen = [], set()
    for alan, ham in bulunan:
        t = temizle(ham)
        if len(t) < 2 or t in gorulen:
            continue
        gorulen.add(t)
        kayitlar.append({'id': kimlik(t), 'metin': t, 'alan': alan})
    return kayitlar

if __name__ == '__main__':
    k = cikar()
    io.open('/Users/ceyda/Downloads/ses_uretim/manifest.json', 'w', encoding='utf-8').write(
        json.dumps(k, ensure_ascii=False, indent=1))
    uz = [len(x['metin']) for x in k]
    print('kayıt:', len(k))
    print('karakter: toplam', sum(uz), '· ortalama', round(sum(uz)/len(uz)), '· en uzun', max(uz))
    print('tahmini ses:', round(sum(uz)/14/60), 'dakika')
    print('örnek:', json.dumps(k[0], ensure_ascii=False))
