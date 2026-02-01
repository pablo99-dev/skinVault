-- -----------------------------------------------------
-- Création de la table des catégories d'armes
-- -----------------------------------------------------
CREATE TABLE weapon_category (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- -----------------------------------------------------
-- Création de la table des armes
-- -----------------------------------------------------
CREATE TABLE weapon (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    category_id INTEGER NOT NULL REFERENCES weapon_category(id)
);

-- -----------------------------------------------------
-- Création de la table des skins
-- -----------------------------------------------------
CREATE TABLE skin (
    id SERIAL PRIMARY KEY,
    weapon_id INTEGER NOT NULL REFERENCES weapon(id),
    name TEXT NOT NULL,
    max_price REAL,
    image_url TEXT,
    UNIQUE (weapon_id, name)
);

-- -----------------------------------------------------
-- (Optionnel) Table pour les skins favoris par utilisateur
-- -----------------------------------------------------
CREATE TABLE user_favorite (
    user_id INTEGER NOT NULL,
    skin_id INTEGER NOT NULL REFERENCES skin(id),
    PRIMARY KEY (user_id, skin_id)
);

