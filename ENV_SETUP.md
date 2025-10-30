# 🔐 Configuration des variables d'environnement

## 📝 Fichier `.env` requis

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```env
PORT=3000
DATABASE_URL=postgresql://user:password@localhost:5432/mathia
JWT_SECRET=super_secret_jwt_key
OPENAI_API_KEY=sk-xxxxxx
```

## 📋 Description des variables

### `PORT`
- **Description** : Port sur lequel le serveur Express écoute
- **Valeur par défaut** : `3000`
- **Exemple** : `PORT=3000`

### `DATABASE_URL`
- **Description** : URL de connexion complète à PostgreSQL
- **Format** : `postgresql://username:password@host:port/database`
- **Exemple** : `DATABASE_URL=postgresql://postgres:monmotdepasse@localhost:5432/mathia`
- **Note** : Si cette variable est définie, elle est prioritaire sur les variables DB_* séparées

### `JWT_SECRET`
- **Description** : Clé secrète pour signer les tokens JWT
- **Important** : ⚠️ Utilisez une clé longue et aléatoire en production
- **Exemple** : `JWT_SECRET=super_secret_jwt_key`
- **Génération sécurisée** :
  ```bash
  node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
  ```

### `OPENAI_API_KEY`
- **Description** : Clé API OpenAI pour la génération d'exercices
- **Format** : `sk-xxxxxxxxxxxxxxxxxxxxxx`
- **Exemple** : `OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx`
- **Obtenir une clé** : https://platform.openai.com/api-keys

## 🔄 Variables optionnelles

Si vous préférez utiliser des variables séparées pour la base de données au lieu de `DATABASE_URL` :

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mathia_db
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe

JWT_EXPIRES_IN=7d
NODE_ENV=development
```

## ⚙️ Comment le projet charge dotenv

### 1. Dans `server.js` (point d'entrée)
```javascript
require('dotenv').config();
```

### 2. Dans `src/config/db.js` (configuration database)
```javascript
require('dotenv').config();

// Utilise DATABASE_URL si disponible
const sequelize = process.env.DATABASE_URL
  ? new Sequelize(process.env.DATABASE_URL, { ... })
  : new Sequelize(DB_NAME, DB_USER, DB_PASSWORD, { ... });
```

### 3. Dans tous les autres fichiers
Les variables sont accessibles via `process.env.VARIABLE_NAME`

## 📦 Dépendance dotenv

Le package `dotenv` est déjà inclus dans `package.json` :

```json
{
  "dependencies": {
    "dotenv": "^16.3.1"
  }
}
```

## 🚀 Démarrage rapide

```bash
# 1. Copier l'exemple et créer votre fichier .env
cat > .env << 'EOF'
PORT=3000
DATABASE_URL=postgresql://postgres:password@localhost:5432/mathia
JWT_SECRET=super_secret_jwt_key
OPENAI_API_KEY=sk-xxxxxx
EOF

# 2. Éditer .env avec vos vraies valeurs
nano .env

# 3. Démarrer le serveur
npm run dev
```

## ✅ Vérification

Pour vérifier que les variables sont bien chargées :

```bash
node -e "require('dotenv').config(); console.log('PORT:', process.env.PORT); console.log('DATABASE_URL:', process.env.DATABASE_URL ? 'Défini' : 'Non défini');"
```

## 🔒 Sécurité

- ✅ Le fichier `.env` est dans `.gitignore` (ne pas commiter)
- ✅ Utilisez des valeurs différentes en développement et production
- ✅ Générez un `JWT_SECRET` aléatoire et long (minimum 32 caractères)
- ✅ Ne partagez jamais vos clés API ou secrets

## 📝 Exemple complet `.env` pour développement

```env
# Server
PORT=3000
NODE_ENV=development

# Database (option 1 : URL complète)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mathia_dev

# JWT
JWT_SECRET=dev_secret_key_change_in_production_with_long_random_string
JWT_EXPIRES_IN=7d

# OpenAI (optionnel si vous n'utilisez pas la génération IA)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# CORS
CORS_ORIGIN=http://localhost:3000
```

## 📝 Exemple complet `.env` pour production

```env
# Server
PORT=3000
NODE_ENV=production

# Database (Utilisez l'URL fournie par votre hébergeur)
DATABASE_URL=postgresql://user:password@production-host.com:5432/mathia_prod

# JWT (IMPORTANT : Générez une nouvelle clé aléatoire)
JWT_SECRET=production_random_32_chars_min_here_use_crypto_randomBytes
JWT_EXPIRES_IN=7d

# OpenAI
OPENAI_API_KEY=sk-proj-your-production-key-here

# CORS (URL de votre app iOS ou frontend)
CORS_ORIGIN=https://your-app.com
```

## 🎯 Priorité des variables

Le code vérifie les variables dans cet ordre :

1. **`DATABASE_URL`** (si définie) → Connexion directe
2. Sinon → `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`

Vous pouvez donc choisir l'une ou l'autre méthode.

## 🐛 Dépannage

### Erreur : "Cannot find module 'dotenv'"
```bash
npm install dotenv
```

### Erreur : "Database connection failed"
Vérifiez que :
- PostgreSQL est démarré : `pg_ctl status` ou `sudo service postgresql status`
- Les credentials dans `DATABASE_URL` sont corrects
- La base de données existe : `createdb mathia`

### Variables non chargées
- Le fichier `.env` doit être à la racine du projet (même niveau que `package.json`)
- Le fichier doit s'appeler exactement `.env` (pas `.env.txt`)
- Redémarrez le serveur après modification du `.env`









