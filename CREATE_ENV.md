# 🔧 Créer votre fichier `.env`

## ⚡ Copier-coller rapide

Exécutez cette commande à la racine du projet pour créer votre fichier `.env` :

```bash
cat > .env << 'EOF'
PORT=3000
DATABASE_URL=postgresql://user:password@localhost:5432/mathia
JWT_SECRET=super_secret_jwt_key
OPENAI_API_KEY=sk-xxxxxx
EOF
```

Puis **éditez le fichier** avec vos vraies valeurs :

```bash
nano .env
# ou
code .env
# ou
vim .env
```

---

## 📋 Contenu du fichier `.env`

Créez un fichier nommé **`.env`** à la racine du projet avec ce contenu :

```env
PORT=3000
DATABASE_URL=postgresql://user:password@localhost:5432/mathia
JWT_SECRET=super_secret_jwt_key
OPENAI_API_KEY=sk-xxxxxx
```

---

## 🔑 Remplacer les valeurs

### 1. `PORT` (optionnel)
Gardez `3000` ou changez selon vos besoins.

### 2. `DATABASE_URL` (requis)
Remplacez `user`, `password`, et `mathia` par vos vraies informations PostgreSQL :

```env
DATABASE_URL=postgresql://postgres:monmotdepasse@localhost:5432/mathia
```

**Format :** `postgresql://username:password@host:port/database_name`

### 3. `JWT_SECRET` (requis)
**⚠️ IMPORTANT** : Utilisez une clé aléatoire longue (minimum 32 caractères).

**Générer une clé sécurisée :**
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

Exemple de résultat :
```env
JWT_SECRET=a3f5e8d9c2b4a1f7e6d8c9b5a3f2e1d9c8b7a6f5e4d3c2b1a9f8e7d6c5b4a3f2
```

### 4. `OPENAI_API_KEY` (optionnel)
Si vous utilisez la génération d'exercices avec OpenAI :

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Obtenez votre clé sur : https://platform.openai.com/api-keys

---

## ✅ Exemple complet pour développement

```env
PORT=3000
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mathia
JWT_SECRET=dev_secret_key_for_local_testing_only
OPENAI_API_KEY=sk-proj-your-key-here-if-you-have-one
```

---

## 🚀 Vérifier que ça fonctionne

```bash
# Vérifier que les variables sont chargées
node -e "require('dotenv').config(); console.log('PORT:', process.env.PORT, '\nDATABASE_URL:', process.env.DATABASE_URL ? '✓ Défini' : '✗ Non défini')"

# Démarrer le serveur
npm run dev
```

Si tout fonctionne, vous verrez :
```
✅ Connexion à PostgreSQL établie avec succès
✅ Modèles synchronisés avec la base de données
🚀 ========================================
🎓 Serveur Mathia démarré avec succès
📍 URL: http://localhost:3000
...
```

---

## 📚 Plus d'informations

Consultez `ENV_SETUP.md` pour une documentation complète des variables d'environnement.









