import json, os
B = '/home/claude/julies'
items = json.load(open(f'{B}/data/menu.json'))
for i in items: i.pop('src', None); i.pop('cats_old', None)
market = json.load(open(f'{B}/data/market_items.json'))
# Only show café items whose photo was downloaded
market = [m for m in market if not m[2] or os.path.exists(f'{B}/site/img/m-{m[2]}.webp')]
j = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
src = open(f'{B}/site/src.html').read()
assert src.count('__MENU__') == 1 and src.count('__MARKET__') == 1
open(f'{B}/site/index.html', 'w').write(src.replace('__MENU__', j(items)).replace('__MARKET__', j(market)))
open('/tmp/claude-0/-home-claude/fa604d9b-382c-5e67-8bce-e7208c888dbc/scratchpad/check.js', 'w').write(src.split('<script>')[1].split('</script>')[0])
print('market items with photos:', len(market))
