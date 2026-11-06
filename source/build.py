import json, os, re
B = '/home/claude/julies'
items = json.load(open(f'{B}/data/menu.json'))
for i in items: i.pop('src', None); i.pop('cats_old', None)
market = json.load(open(f'{B}/data/market_items.json'))
# Only show café items whose photo was downloaded
market = [m for m in market if not m[2] or os.path.exists(f'{B}/site/img/m-{m[2]}.webp')]
j = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
src = open(f'{B}/site/src.html').read()
SITE = 'https://vexoradigitalweb-png.github.io/julies-market-cafe-demo./'   # change to Julie's domain at launch
LD = {"@context": "https://schema.org", "@type": "CafeOrCoffeeShop", "@id": SITE + "#business",
  "name": "Julie's Market & Café", "alternateName": "Julie's Kitchen",
  "description": "Kosher dairy market and café under the Vaad Hakashrus of Flatbush, with glatt meat and Chalav Yisrael dairy catering.",
  "url": SITE, "image": SITE + "img/og.jpg", "logo": SITE + "img/icon-512.png",
  "telephone": "+1-718-573-9453", "email": "julie@jebani.com",
  "address": {"@type": "PostalAddress", "streetAddress": "514 Kings Hwy", "addressLocality": "Brooklyn", "addressRegion": "NY", "postalCode": "11223", "addressCountry": "US"},
  "openingHoursSpecification": [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "08:00", "closes": "17:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "08:00", "closes": "14:00"}],
  "servesCuisine": ["Kosher", "Café", "Salads"], "hasMenu": SITE + "market/",
  "sameAs": ["https://www.instagram.com/julieebani/", "https://www.ubereats.com/store/julies-market-cafe/qobyJZ7BVXCvS2kCOyTnuw"],
  "makesOffer": {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Kosher catering", "url": SITE + "catering/",
    "description": "Glatt meat and Chalav Yisrael dairy catering menus, never mixed: appetizers, platters, salads, mains, brunch and Shabbat."}}}
src = src.replace('__SITE__', SITE).replace('__LDJSON__', json.dumps(LD, ensure_ascii=False).replace('</', '<\\/'))
assert src.count('__MENU__') == 1 and src.count('__MARKET__') == 1
open(f'{B}/site/index.html', 'w').write(src.replace('__MENU__', j(items)).replace('__MARKET__', j(market)))
open('/tmp/claude-0/-home-claude/fa604d9b-382c-5e67-8bce-e7208c888dbc/scratchpad/check.js', 'w').write(max(re.findall(r'<script>(.*?)</script>', src, re.S), key=len))
print('market items with photos:', len(market))
