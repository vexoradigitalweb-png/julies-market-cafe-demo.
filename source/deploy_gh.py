"""Copy the current build into the GitHub Pages repo as a full standalone page, plus source files."""
import os, shutil, glob
B = '/home/claude/julies'
R = '/home/claude/julies-market-cafe-demo.'
src = open(f'{B}/site/index.html').read()
cut = src.index('<header class="top wrap">')
head, body = src[:cut], src[cut:]
reset = '''<style>
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px system-ui,-apple-system,sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>'''
# ---- Site settings: change these two lines at launch on Julie's domain ----
SITE = 'https://vexoradigitalweb-png.github.io/julies-market-cafe-demo./'
BASE = '/julies-market-cafe-demo./'
NOINDEX = True   # demo stays hidden from Google; set False at launch
VIEWS = ['market', 'catering', 'about', 'contact']
TITLES = {'home': "Julie's Market & Café | Kosher Café, Market & Catering on Kings Highway, Brooklyn",
  'market': "The Market & Café: Menu & Prices | Julie's, Kings Highway",
  'catering': "Kosher Catering Menu & Online Quote | Julie's Market & Café",
  'about': "About Julie | Julie's Market & Café",
  'contact': "Contact, Hours & Directions | Julie's Market & Café"}
DESCS = {'home': "Kosher market &amp; café at 514 Kings Highway, Brooklyn, under the Vaad of Flatbush. Salads, coffee and grab &amp; go, plus glatt meat and dairy catering quotes online.",
  'market': "The full café and market menu with prices: coffee and matcha, smoothies, grab &amp; go salads and bowls, prepared food, a cheese counter and pantry goods. Kosher dairy, Chalav Yisrael.",
  'catering': "193 kosher catering dishes in glatt meat or Chalav Yisrael dairy, never mixed: appetizers, platters, salads, mains, Shabbat and more. Build your order and get a quote.",
  'about': "Meet Julie, the cook behind Julie's Market &amp; Café and Julie's Kitchen catering on Kings Highway, Brooklyn.",
  'contact': "Call (718) 573-9453, text Julie at 917-880-8999 or visit 514 Kings Highway, Brooklyn. Open Sun–Thu 8 AM–5 PM, Fri 8 AM–2 PM."}
import re
# crawlable links: each section link points at its own address
for v in VIEWS: body = body.replace(f'href="#{v}"', f'href="{BASE}{v}/"')
body = body.replace('href="#home"', f'href="{BASE}"')
def page(v):
    h = head.replace('__SITE__', SITE)
    url = SITE + ('' if v == 'home' else v + '/')
    h = re.sub(r'<title>.*?</title>', f'<title>{TITLES[v].replace("&", "&amp;")}</title>', h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESCS[v]}">', h, count=1)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', h, count=1)
    h = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', h, count=1)
    if v != 'home': h = re.sub(r'<link rel="preload" as="image"[^>]*>\n', '', h, count=1)   # the storefront photo is only on the home page
    b = body
    if v != 'home':
        b = b.replace('<section data-view="home">', '<section data-view="home" hidden>', 1).replace(f'<section data-view="{v}" hidden>', f'<section data-view="{v}">', 1)
    return ('<!doctype html>\n<html lang="en" data-base="' + BASE + '">\n<head>\n<meta charset="utf-8">\n<base href="' + BASE + '">\n'
       '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
       + ('<meta name="robots" content="noindex,nofollow">\n' if NOINDEX else '') + reset + '\n' + h + '\n</head>\n<body>\n' + b + '\n</body>\n</html>\n')
open(f'{R}/index.html', 'w').write(page('home'))
for v in VIEWS:
    os.makedirs(f'{R}/{v}', exist_ok=True); open(f'{R}/{v}/index.html', 'w').write(page(v))
from datetime import date
open(f'{R}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
  + ''.join(f'  <url><loc>{SITE}{"" if v == "home" else v + "/"}</loc><lastmod>{date.today()}</lastmod></url>\n' for v in ['home'] + VIEWS) + '</urlset>\n')
open(f'{R}/404.html', 'w').write(page('home'))
os.makedirs(f'{R}/img', exist_ok=True)
shutil.copytree(f'{B}/site/img', f'{R}/img', dirs_exist_ok=True)
os.makedirs(f'{R}/source/data', exist_ok=True); os.makedirs(f'{R}/source/backups', exist_ok=True)
shutil.copy2(f'{B}/site/src.html', f'{R}/source/src.html')
shutil.copy2(f'{B}/build.py', f'{R}/source/build.py')
shutil.copy2(f'{B}/deploy_gh.py', f'{R}/source/deploy_gh.py')
for f in ['catalog_raw.json', 'menu.json', 'market_items.json', 'kosher_labels_for_julie.csv', 'build_menu.py']:
    shutil.copy2(f'{B}/data/{f}', f'{R}/source/data/{f}')
for f in glob.glob(f'{B}/site/src_v*_backup.html') + [f'{B}/site/without-counters.html']:
    shutil.copy2(f, f'{R}/source/backups/' + os.path.basename(f))
print('deployed', os.path.getsize(f'{R}/index.html') // 1024, 'KB')
