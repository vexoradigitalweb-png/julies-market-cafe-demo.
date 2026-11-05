import json, re, csv, hashlib

raw = json.load(open('/home/claude/julies/data/catalog_raw.json'))

# Draft kosher labels (M = meat, D = dairy, P = parve, PM = vegetable version parve / chicken version meat)
M = {5,6,13,28,29,33,37,38,39,40,42,43,44,53,59,64,70,71,72,73,74,75,76,77,78,79,80,81,82,84,85,
     106,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,166,167,173,183,193}
D = {1,3,7,20,21,41,49,56,89,98,99,101,102,103,113,139,140,141,142,143,145,146,147,148,149,
     150,151,156,157,160,172,177,178,179,180,184,185,186,191,192}
PM = {168,169}
GUESS = {2,3,7,21,35,41,45,54,55,58,65,69,116,138,139,143,144,150,152,163,172,181,188,189,192}
# Per-size overrides where one listing mixes kitchens
VARIANT = {36: {"Spicy Rig Sauce": "D", "Bolognese Sauce": "M", "Pesto Sauce": "D"}}

CAT = {"SUKKOT MENU": "Sukkot", "Weekly Menu": "Weekly Menu", "Pick Ups": "Pick Ups",
       "Shabbat/Holiday": "Shabbat & Holiday", "Sides": "Sides", "Pasta/Rice": "Pasta & Rice",
       "Fish": "Fish", "Meats": "Meats", "Chicken": "Chicken", "Mains": "Mains", "Brunch": "Brunch",
       "Salads": "Salads", "Appetizers": "Appetizers", "Platters/Boards": "Platters & Boards",
       "65ad60ee7fe29939972e4592": "More"}

items = []
for n, t, cats, desc, variants, imgs in raw:
    if n == 19:
        k = "BOOK"
    elif n in VARIANT:
        k = "MIX"
    elif n in M: k = "M"
    elif n in D: k = "D"
    elif n in PM: k = "PM"
    else: k = "P"
    photos = [] if imgs[0].startswith("S/") else imgs
    items.append({
        "id": n, "name": t, "cats": [CAT[c] for c in cats], "desc": desc,
        "sizes": [{"label": o, "price": float(p), "k": VARIANT.get(n, {}).get(o)} for o, p in variants],
        "k": k, "guess": n in GUESS,
        # local file names; filled once the photos are downloaded
        "img": [f"img/{n}-{i+1}.webp" for i in range(len(photos))],
        "src": ["https://images.squarespace-cdn.com/content/v1/65ad501f1776560c568f1d4c/" + p[2:] for p in photos],
    })

# Safety: prices in site data must equal the verified catalog exactly
for it, r in zip(items, raw):
    assert [f"{s['price']:.2f}" for s in it["sizes"]] == [p for _, p in r[4]], it["id"]
    assert [s["label"] for s in it["sizes"]] == [o for o, _ in r[4]], it["id"]

json.dump(items, open('/home/claude/julies/data/menu.json', 'w'), ensure_ascii=False)

names = {"M": "Meat", "D": "Dairy", "P": "Parve", "PM": "Veg: Parve / Chicken: Meat", "MIX": "Depends on sauce", "BOOK": "Book"}
with open('/home/claude/julies/data/kosher_labels_for_julie.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(["#", "Dish", "Draft label", "Confidence", "Julie's correction"])
    for it in items:
        w.writerow([it["id"], it["name"], names[it["k"]], "Guess - please check" if it["guess"] else "Likely", ""])

from collections import Counter
print(Counter(i["k"] for i in items), "photos", sum(len(i["img"]) for i in items), "no photo", sum(1 for i in items if not i["img"]))
