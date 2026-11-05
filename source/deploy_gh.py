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
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
       '<meta name="robots" content="noindex,nofollow">\n' + reset + '\n' + head + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
open(f'{R}/index.html', 'w').write(doc)
os.makedirs(f'{R}/img', exist_ok=True)
for f in os.listdir(f'{B}/site/img'):
    shutil.copy2(f'{B}/site/img/{f}', f'{R}/img/{f}')
os.makedirs(f'{R}/source/data', exist_ok=True); os.makedirs(f'{R}/source/backups', exist_ok=True)
shutil.copy2(f'{B}/site/src.html', f'{R}/source/src.html')
shutil.copy2(f'{B}/build.py', f'{R}/source/build.py')
shutil.copy2(f'{B}/deploy_gh.py', f'{R}/source/deploy_gh.py')
for f in ['catalog_raw.json', 'menu.json', 'market_items.json', 'kosher_labels_for_julie.csv', 'build_menu.py']:
    shutil.copy2(f'{B}/data/{f}', f'{R}/source/data/{f}')
for f in glob.glob(f'{B}/site/src_v*_backup.html') + [f'{B}/site/without-counters.html']:
    shutil.copy2(f, f'{R}/source/backups/' + os.path.basename(f))
print('deployed', os.path.getsize(f'{R}/index.html') // 1024, 'KB')
