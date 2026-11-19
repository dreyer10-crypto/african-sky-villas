#!/usr/bin/env python3
"""Build a branded African Sky Villas photo page for one guest's safari.

Usage:
  python3 make_gallery.py --guest "Liana Flores" --date 2026-11-19 \
      --safari "Full-Day Kruger Safari" --photos ./in/liana --out ./out \
      [--donate-url https://...] [--supplier "Africa Kruger Safari"]

Produces  out/<guest-slug>-<random>/  with index.html, photos/, thumbs/,
<slug>-photos.zip and message.txt (WhatsApp + email text ready to paste).
The random part of the folder name makes the link hard to guess; the page is noindex.
"""
import argparse, datetime, html, io, os, re, secrets, shutil
from PIL import Image, ImageOps
import sys as _sys; _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texts import TEXT, PT_MONTHS

LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'images', 'logo-transparent.png')
SITE = 'https://africansky.travel'
TOURS = SITE + '/african-sky-villas-tours-and-activities.html'
WA = '27762095334'

def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def save(im, path, edge, q):
    im = im.copy(); im.thumbnail((edge, edge), Image.LANCZOS)
    im.save(path, 'JPEG', quality=q, optimize=True, progressive=True)  # no EXIF carried over
    return im.size

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--guest', required=True); ap.add_argument('--date', required=True)
    ap.add_argument('--safari', required=True); ap.add_argument('--photos', required=True)
    ap.add_argument('--out', default='out'); ap.add_argument('--donate-url', default='')
    ap.add_argument('--supplier', default='Africa Kruger Safari')
    ap.add_argument('--base-url', default=SITE + '/photos')
    ap.add_argument('--lang', default='en', choices=sorted(TEXT))
    ap.add_argument('--phone', default='', help='guest WhatsApp number, digits only, with country code')
    a = ap.parse_args()

    files = sorted(f for f in os.listdir(a.photos) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')))
    if not files: raise SystemExit('no photos found in ' + a.photos)
    folder = f"{slug(a.guest)}-{secrets.token_hex(4)}"
    out = os.path.join(a.out, folder); os.makedirs(out + '/photos'); os.makedirs(out + '/thumbs')
    shutil.copy(LOGO, out + '/logo.png')
    d = datetime.date.fromisoformat(a.date)
    when = f"{d.day} de {PT_MONTHS[d.month-1]} de {d.year}" if a.lang == 'pt' else d.strftime('%-d %B %Y')
    T = TEXT[a.lang]
    first = a.guest.split()[0]

    items = []
    for i, f in enumerate(files, 1):
        im = ImageOps.exif_transpose(Image.open(os.path.join(a.photos, f))).convert('RGB')
        name = f'{i:02d}.jpg'
        w, h = save(im, f'{out}/photos/{name}', 2000, 85)
        save(im, f'{out}/thumbs/{name}', 720, 78)
        items.append((name, w, h))
    zipname = f'{slug(a.guest)}-safari-photos.zip'

    import urllib.parse as _u
    donate = a.donate_url or ('https://wa.me/' + WA + '?text=' + _u.quote(T['gwa'].format(first=first)))
    gb, gs = (T['gb'], T['gs']) if a.donate_url else (T['gb2'], T['gs2'])
    e = html.escape
    tiles = '\n'.join(
        f'<figure class="tile{" wide" if w/h > 1.6 and k % 5 == 0 else ""}"><button data-i="{k}" aria-label="Open photo {k+1}">'
        f'<img src="thumbs/{n}" loading="lazy" width="{w}" height="{h}" alt="Safari photo {k+1}"></button>'
        f'<a class="dl" href="photos/{n}" download="{slug(a.safari)}-{k+1:02d}.jpg" aria-label="Download photo {k+1}">↓</a></figure>'
        for k, (n, w, h) in enumerate(items))

    page = f'''<!doctype html><html lang="{T['lang']}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>{T['title']}</title>
<meta property="og:title" content="{e(T['og'].format(first=first))}">
<meta property="og:description" content="{e(a.safari)} · {when} · African Sky Villas">
<meta property="og:image" content="{a.base_url}/{folder}/photos/01.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--cream:#FBF6EE;--deep:#F2E9D8;--esp:#1A1006;--char:#2C1F12;--terra:#C44D2C;--amber:#D89B3A;--soft:#E8BF6B;--taupe:#8B6F47}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--cream);color:var(--char);font:400 16px/1.65 Manrope,system-ui,sans-serif}}
a{{color:inherit}}
.top{{position:absolute;inset:0 0 auto;z-index:3;display:flex;align-items:center;gap:10px;padding:18px 20px;color:#fff}}
.top img{{width:42px;height:42px;border-radius:50%;background:#FBF6EE;padding:3px;box-shadow:0 2px 10px rgba(0,0,0,.3)}}
.top b{{font:500 19px Fraunces,serif}}.top b i{{font-style:normal;color:var(--soft)}}
.hero{{position:relative;min-height:88svh;display:flex;align-items:flex-end;color:#fff;overflow:hidden;background:var(--esp)}}
.hero>img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;animation:kb 18s ease-out both}}
@keyframes kb{{from{{transform:scale(1.12)}}to{{transform:scale(1)}}}}
@media (prefers-reduced-motion:reduce){{.hero>img{{animation:none}}}}
.hero:after{{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(26,16,6,.88),rgba(26,16,6,.1) 55%,rgba(26,16,6,.35))}}
.hero .t{{position:relative;z-index:2;padding:0 20px 44px;max-width:900px;margin:0 auto;width:100%}}
.eb{{font:700 11px Manrope;letter-spacing:.28em;text-transform:uppercase;color:var(--soft)}}
h1{{font:400 clamp(38px,8vw,72px)/1.02 Fraunces,serif;margin:10px 0 12px}}h1 em{{color:var(--soft)}}
.meta{{font-size:15px;opacity:.9}}
.cta{{display:inline-flex;gap:8px;align-items:center;margin-top:22px;padding:13px 22px;border-radius:999px;background:var(--terra);color:#fff;text-decoration:none;font-weight:600}}
.wrap{{max-width:900px;margin:0 auto;padding:0 20px}}
.note{{padding:56px 0 8px}}.note p{{font:400 clamp(19px,2.6vw,23px)/1.55 Fraunces,serif;margin:0 0 14px}}
.sig{{font:italic 400 17px Fraunces,serif;color:var(--taupe)}}
.bar{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin:40px 0 16px;flex-wrap:wrap}}
.bar h2{{font:400 30px Fraunces,serif;margin:0}}.bar a{{font-weight:600;color:var(--terra);text-decoration:none}}
.grid{{columns:2 260px;column-gap:12px}}
.tile{{position:relative;margin:0 0 12px;break-inside:avoid;border-radius:10px;overflow:hidden;background:var(--deep)}}
.tile button{{all:unset;cursor:zoom-in;display:block}}.tile img{{display:block;width:100%;height:auto}}
.dl{{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);width:38px;height:38px;border-radius:50%;display:grid;place-items:center;background:rgba(26,16,6,.6);color:#fff;text-decoration:none;font-weight:700}}
.credit{{font-size:13px;color:var(--taupe);margin:6px 0 0}}
.give{{margin:64px 0 0;background:var(--esp);color:var(--cream);border-radius:16px;padding:36px 26px;position:relative;overflow:hidden}}
.give .eb{{color:var(--soft)}}.give h2{{font:400 clamp(28px,5vw,40px)/1.1 Fraunces,serif;margin:10px 0 12px}}.give h2 em{{color:var(--soft)}}
.give p{{margin:0 0 18px;color:#E9DFCF;max-width:560px}}
.give .cta{{background:var(--amber);color:var(--esp)}}.give small{{display:block;margin-top:14px;color:#B59B76;font-size:12.5px}}
.next{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:24px 0 0}}
.next a{{display:block;padding:20px;border:1px solid #E3D6BC;border-radius:12px;text-decoration:none;background:#FFFBF3}}
.next b{{display:block;font:500 19px Fraunces,serif;margin-bottom:4px}}.next span{{font-size:14px;color:var(--taupe)}}
footer{{margin-top:56px;padding:28px 20px 40px;text-align:center;font-size:13px;color:var(--taupe);border-top:1px solid #E3D6BC}}
.lb{{position:fixed;inset:0;z-index:9;background:rgba(15,9,3,.95);display:none;align-items:center;justify-content:center}}
.lb.on{{display:flex}}.lb img{{max-width:96vw;max-height:84vh;border-radius:6px}}
.lb button,.lb a{{position:absolute;color:#fff;background:none;border:0;font-size:34px;cursor:pointer;padding:14px;text-decoration:none}}
.lb .x{{top:8px;right:10px}}.lb .p{{left:4px;top:50%;transform:translateY(-50%)}}.lb .n{{right:4px;top:50%;transform:translateY(-50%)}}
.lb .d{{bottom:12px;left:50%;transform:translateX(-50%);font:600 15px Manrope;background:var(--terra);border-radius:999px;padding:11px 20px}}
</style></head><body>
<header class="top"><img src="logo.png" alt=""><b>African Sky <i>Villas</i></b></header>
<section class="hero"><img src="photos/{items[0][0]}" alt="">
<div class="t"><div class="eb">{e(a.safari)} · {when}</div>
<h1>{T['h1'].format(first=e(first))}</h1>
<div class="meta">{T['count'].format(n=len(items))}</div>
<a class="cta" href="#photos">{T['see']}</a></div></section>
<main class="wrap">
<section class="note"><p>{T['p1']}</p>
<p>{T['p2']}</p>
<div class="sig">{T['sig']}</div></section>
<div class="bar" id="photos"><h2>{T['yours']}</h2><a href="#" id="dlall">{T['all'].format(n=len(items))}</a></div>
<div class="grid">
{tiles}
</div>
<p class="credit">{T['credit'].format(sup=e(a.supplier))}</p>
<section class="give" id="give"><div class="eb">Tap2Protect</div>
<h2>{T['gh']}</h2>
<p>{T['gp']}</p>
<a class="cta" href="{e(donate)}" target="_blank" rel="noopener">{gb}</a>
<small>{gs}</small></section>
<div class="next">
<a href="{TOURS}"><b>{T['n1']}</b><span>{T['n1s']}</span></a>
<a href="https://wa.me/{WA}"><b>{T['n2']}</b><span>{T['n2s']}</span></a>
</div></main>
<footer>African Sky Villas · Marloth Park · South Africa · <a href="{SITE}">africansky.travel</a></footer>
<div class="lb" role="dialog" aria-modal="true"><img alt=""><button class="x" aria-label="Close">×</button>
<button class="p" aria-label="Previous">‹</button><button class="n" aria-label="Next">›</button><a class="d" download>{T['dl']}</a></div>
<script src="../jszip.min.js"></script>
<script>
document.getElementById('dlall').onclick=async ev=>{{ev.preventDefault();const b=ev.currentTarget,t=b.textContent;
try{{b.textContent='…';const z=new JSZip();
for(let i=0;i<P.length;i++){{b.textContent=(i+1)+' / '+P.length;const r=await fetch('photos/'+P[i]);z.file('{slug(a.safari)}-'+String(i+1).padStart(2,'0')+'.jpg',await r.blob())}}
const blob=await z.generateAsync({{type:'blob'}}),u=URL.createObjectURL(blob),l=document.createElement('a');l.href=u;l.download='{zipname}';document.body.appendChild(l);l.click();l.remove();setTimeout(()=>URL.revokeObjectURL(u),4000)}}
catch(err){{alert('{T['dlerr']}')}}finally{{b.textContent=t}}}};
const P={[n for n,_,_ in items]!r},lb=document.querySelector('.lb'),im=lb.querySelector('img'),d=lb.querySelector('.d');let c=0;
function show(i){{c=(i+P.length)%P.length;im.src='photos/'+P[c];d.href='photos/'+P[c];d.download='{slug(a.safari)}-'+String(c+1).padStart(2,'0')+'.jpg';lb.classList.add('on')}}
document.querySelectorAll('.tile button').forEach(b=>b.onclick=()=>show(+b.dataset.i));
lb.querySelector('.x').onclick=()=>lb.classList.remove('on');lb.querySelector('.p').onclick=()=>show(c-1);lb.querySelector('.n').onclick=()=>show(c+1);
lb.onclick=e=>{{if(e.target===lb)lb.classList.remove('on')}};
addEventListener('keydown',e=>{{if(!lb.classList.contains('on'))return;if(e.key==='Escape')lb.classList.remove('on');if(e.key==='ArrowLeft')show(c-1);if(e.key==='ArrowRight')show(c+1)}});
let x0=null;lb.addEventListener('touchstart',e=>x0=e.touches[0].clientX);lb.addEventListener('touchend',e=>{{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40)show(c+(dx<0?1:-1));x0=null}});
</script></body></html>'''
    open(out + '/index.html', 'w', encoding='utf-8').write(page)

    link = f'{a.base_url}/{folder}/'
    fmt = dict(first=first, safari=a.safari, n=len(items), link=link, when=when)
    wa = T['wa'].format(**fmt)
    msg = 'WHATSAPP\n' + wa + '\n\n'
    if a.phone:
        import urllib.parse
        msg += 'One-tap WhatsApp link (opens the chat with this message filled in):\nhttps://wa.me/' + a.phone + '?text=' + urllib.parse.quote(wa) + '\n\n'
    msg += 'EMAIL\nSubject: ' + T['subj'].format(**fmt) + '\n\n' + T['mail'].format(**fmt) + '\n'
    open(out + '/message.txt', 'w', encoding='utf-8').write(msg)
    print(out); print(link)

if __name__ == '__main__':
    main()
