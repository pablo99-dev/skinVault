import psycopg2
import csv
import os

# =========================
# Connexion PostgreSQL
# =========================
conn = psycopg2.connect(
    dbname="database_name",  # à remplacer
    user="username",         # à remplacer
    password="password",       # à remplacer
    host="localhost"
)
cur = conn.cursor()

# =========================
# Création des tables si elles n'existent pas
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS weapon_category (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS weapon (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    category_id INTEGER NOT NULL
        REFERENCES weapon_category(id)
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS skin (
    id SERIAL PRIMARY KEY,
    weapon_id INTEGER NOT NULL
        REFERENCES weapon(id),
    name TEXT NOT NULL,
    max_price REAL,
    image_url TEXT,
    UNIQUE (weapon_id, name)
);
""")
cur.execute("""
CREATE TABLE user_favorite (
    user_id INTEGER NOT NULL,
    skin_id INTEGER NOT NULL REFERENCES skin(id),
    PRIMARY KEY (user_id, skin_id)
);
""")

print("✅ Tables créées ou déjà existantes")

# =========================
# Catégories
# =========================
categories = [
    'Knife',
    'Rifle',
    'SMG',
    'Sniper',
    'Pistol',
    'Shotgun',
    'Machine Gun',
    'Agent',
    'Sticker'
]

for category_name in categories:
    cur.execute("""
        INSERT INTO weapon_category (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (category_name,))

print("✅ Catégories insérées")

# =========================
# Armes → Catégories
# =========================
WEAPONS = {
    'Karambit': 'Knife',
    'Butterfly': 'Knife',
    'M9 Bayonet': 'Knife',
    'Gut': 'Knife',
    'Flip': 'Knife',
    'Huntsman': 'Knife',

    'AK-47': 'Rifle',
    'M4A4': 'Rifle',
    'M4A1-S': 'Rifle',
    'AUG': 'Rifle',
    'SG 553': 'Rifle',
    'FAMAS': 'Rifle',

    'MP9': 'SMG',
    'UMP-45': 'SMG',
    'MP7': 'SMG',
    'P90': 'SMG',
    'MAC-10': 'SMG',

    'AWP': 'Sniper',
    'SSG 08': 'Sniper',
    'SCAR-20': 'Sniper',
    'G3SG1': 'Sniper',

    'Glock': 'Pistol',
    'USP-S': 'Pistol',
    'Desert Eagle': 'Pistol',
    'P250': 'Pistol',
    'Five-SeveN': 'Pistol',
    'CZ75': 'Pistol',

    'Nova': 'Shotgun',
    'XM1014': 'Shotgun',
    'MAG-7': 'Shotgun',
    'Sawed-Off': 'Shotgun',

    'M249': 'Machine Gun',
    'Negev': 'Machine Gun',

    'Agents': 'Agent',
    'All Stickers': 'Sticker'
}

for weapon_name, category_name in WEAPONS.items():
    cur.execute("""
        INSERT INTO weapon (name, category_id)
        SELECT %s, id
        FROM weapon_category
        WHERE name = %s
        ON CONFLICT (name) DO NOTHING
    """, (weapon_name, category_name))

print("✅ Armes insérées")

# =========================
# Import des skins depuis CSV
# =========================
csv_folder = "../filesdb"  # le dossier qui contient les fichiers csv
csv_files = [f for f in os.listdir(csv_folder) if f.endswith(".csv")]

CSV_TO_WEAPON = {
    "karambit": "Karambit",
    "butterfly": "Butterfly",
    "m9bayonet": "M9 Bayonet",
    "gut": "Gut",
    "flip": "Flip",
    "huntsman": "Huntsman",

    "ak_47": "AK-47",
    "m4a4": "M4A4",
    "m4a1": "M4A1-S",
    "m4a1_s": "M4A1-S",
    "aug": "AUG",
    "sg553": "SG 553",
    "famax": "FAMAS",
    "g3sg1": "G3SG1",
    "scar20": "SCAR-20",
    "awp": "AWP",
    "ssg08": "SSG 08",

    "mp9": "MP9",
    "ump_45": "UMP-45",
    "mp7": "MP7",
    "p90": "P90",
    "mac10": "MAC-10",

    "glock": "Glock",
    "usps": "USP-S",
    "p250": "P250",
    "fivesevn": "Five-SeveN",
    "cz75": "CZ75",
    "desert_eagel": "Desert Eagle",

    "nova": "Nova",
    "xm1014": "XM1014",
    "mag7": "MAG-7",
    "sawedoff": "Sawed-Off",

    "m249": "M249",
    "negev": "Negev",

    "stickers": "All Stickers",
    "agents": "Agents",
}

# remplissage table skin
for file in csv_files:
    file_key = file.replace(".csv", "").lower()
    weapon_name = CSV_TO_WEAPON.get(file_key)

    if not weapon_name:
        print(f"❌ Pas de mapping pour {file}")
        continue

    # Récupérer weapon_id
    cur.execute("SELECT id FROM weapon WHERE name=%s;", (weapon_name,))
    result = cur.fetchone() # une seule ligne 
    if not result:
        print(f"❌ Weapon '{weapon_name}' non trouvé en base")
        continue
    weapon_id = result[0]

    # Lire le CSV
    with open(os.path.join(csv_folder, file), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            skin_name = row["name"]
            image_url = row["image _url"]  # attention à l'espace (c'est comme ca que c'est importe depuis les csv )
            max_price_raw = row["max_price"]

            # =========================
            # Nettoyer le prix 
            # =========================
            max_price = None
            if max_price_raw:
                cleaned = max_price_raw.strip().replace(",", "").replace("$", "")
                try:
                    max_price = float(cleaned)
                except ValueError: # si le prix n'est pas un flot 
                    print(f"⚠️ Prix invalide pour {skin_name}: {max_price_raw}")
                    max_price = None

            # Insertion skin
            cur.execute("""
                INSERT INTO skin (weapon_id, name, max_price, image_url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (weapon_id, name) DO NOTHING;
            """, (weapon_id, skin_name, max_price, image_url))

print("✅ Skins importés depuis les CSV")

# =========================
# Commit & fermeture
# =========================
conn.commit()
cur.close()
conn.close()

print("🎉 Base complète prête : catégories, armes et skins")

