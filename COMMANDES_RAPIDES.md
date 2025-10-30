# ⚡ Commandes rapides - Mathia

Toutes les commandes utiles en un seul endroit.

## 🖥️ Backend

### Installation et configuration

```bash
# Installation
npm install
pip install -r requirements.txt

# Configuration
cp example.env .env
nano .env  # Éditer avec vos valeurs

# Base de données
createdb mathia
npm run db:sync
```

### Démarrage

```bash
# Mode développement (auto-reload)
npm run dev

# Mode production
npm start

# Synchroniser la base
npm run db:sync
```

### Tests

```bash
# Tests automatisés
npm run test:api

# Tests bash
npm run test:api:bash

# Health check
curl http://localhost:3000/api/health
```

### Génération IA

```bash
# Générer 10 exercices
npm run generate:exercises

# Ou avec paramètres personnalisés
python scripts/ai_generate_exercises.py \
  --chapter "Les fractions" \
  --grade "6ème" \
  --difficulty "facile" \
  --type "qcm" \
  --count 10

# Importer en base
npm run import:exercises
```

## 📊 Base de données

### Commandes PostgreSQL

```bash
# Se connecter
psql -U postgres -d mathia

# Lister les tables
\dt

# Voir les utilisateurs
SELECT id, name, email FROM users;

# Voir les cours
SELECT id, title, grade, chapter FROM courses;

# Voir les exercices
SELECT id, "courseId", type, body, difficulty FROM exercises;

# Voir les tentatives
SELECT u.name, e.body, a."userAnswer", a."isCorrect"
FROM attempts a
JOIN users u ON a."userId" = u.id
JOIN exercises e ON a."exerciseId" = e.id
ORDER BY a."createdAt" DESC;

# Quitter
\q
```

### Créer des cours de test

```sql
INSERT INTO courses (title, grade, chapter, description, "createdAt", "updatedAt")
VALUES 
  ('Les fractions', '6ème', 'Arithmétique', 'Apprendre les fractions', NOW(), NOW()),
  ('Géométrie', '6ème', 'Géométrie', 'Les formes', NOW(), NOW()),
  ('Les équations', '3ème', 'Algèbre', 'Résoudre des équations', NOW(), NOW());
```

### Nettoyer les données de test

```sql
DELETE FROM users WHERE email LIKE '%test%';
DELETE FROM attempts WHERE "userId" IN (SELECT id FROM users WHERE email LIKE '%test%');
```

## 🌐 API (curl)

### Authentification

```bash
# Signup
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"User","email":"user@test.com","password":"test123"}'

# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"test123"}'

# Sauvegarder le token
export TOKEN="votre_token_ici"
```

### Cours et exercices

```bash
# Tous les cours
curl http://localhost:3000/api/courses \
  -H "Authorization: Bearer $TOKEN"

# Un cours par ID
curl http://localhost:3000/api/courses/1 \
  -H "Authorization: Bearer $TOKEN"

# Tous les exercices
curl http://localhost:3000/api/exercises \
  -H "Authorization: Bearer $TOKEN"

# Exercices filtrés
curl "http://localhost:3000/api/exercises?courseId=1&difficulty=facile" \
  -H "Authorization: Bearer $TOKEN"
```

### Créer et répondre

```bash
# Créer un exercice
curl -X POST http://localhost:3000/api/admin/exercises \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "courseId": 1,
    "type": "qcm",
    "body": "Question?",
    "options": {"A": "1", "B": "2", "C": "3"},
    "answer": "B",
    "difficulty": "facile"
  }'

# Soumettre une réponse
curl -X POST http://localhost:3000/api/attempts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"exerciseId": 1, "userAnswer": "B"}'
```

## 📱 iOS

### Xcode

```bash
# Ouvrir le projet
cd mobile/MathiaApp
open MathiaApp.xcodeproj

# Ou créer un nouveau projet (voir mobile/SETUP_GUIDE.md)
```

### Commandes Xcode

- **Build** : ⌘+B
- **Run** : ⌘+R
- **Clean** : ⌘+Shift+K
- **Stop** : ⌘+.

### Configuration réseau

Trouver l'IP du Mac (pour iPhone physique) :
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

## 🔍 Debugging

### Logs backend

```bash
# Voir les requêtes en temps réel
npm run dev
# Les logs s'affichent automatiquement
```

### Logs PostgreSQL

```bash
# Activer les logs SQL
# Dans .env, ajouter ou modifier :
NODE_ENV=development
```

### Logs iOS

Dans Xcode :
- View → Debug Area → Activate Console (⌘+Shift+C)
- Chercher les logs qui commencent par 📥 (réponses API)

## 🛠️ Utilitaires

### Vérifier les ports

```bash
# Voir qui utilise le port 3000
lsof -i :3000

# Tuer le process sur le port 3000
kill -9 $(lsof -t -i:3000)
```

### Générer un JWT_SECRET sécurisé

```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### Vérifier les dépendances

```bash
# Node.js
npm list --depth=0

# Python
pip list | grep -E "openai|psycopg2|dotenv"
```

## 📚 Documentation

### Ouvrir la documentation

```bash
# Swagger UI
open http://localhost:3000/api-docs

# Documentation locale (Markdown)
code .  # Ouvrir dans VS Code
```

### Générer une doc PDF (optionnel)

```bash
# Installer pandoc
brew install pandoc

# Convertir README en PDF
pandoc README.md -o README.pdf
```

## 🔄 Workflow de développement

### Développement backend

```bash
# Terminal 1 : Serveur
npm run dev

# Terminal 2 : Logs PostgreSQL
tail -f /usr/local/var/log/postgres.log  # Mac
# ou
sudo tail -f /var/log/postgresql/postgresql-*.log  # Linux

# Terminal 3 : Tests
npm run test:api
```

### Développement mobile

```bash
# Terminal 1 : Backend
npm run dev

# Xcode : Run l'app iOS
# ⌘+R
```

## 🚀 Déploiement

### Backend → Heroku

```bash
heroku create mathia-api
heroku addons:create heroku-postgresql
heroku config:set JWT_SECRET=$(node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")
git push heroku main
```

### Backend → Render

```bash
# Via dashboard Render
# 1. Connect repository
# 2. Set environment variables
# 3. Deploy
```

### iOS → TestFlight

```bash
# Dans Xcode
# 1. Product → Archive
# 2. Distribute App → TestFlight
# 3. Upload
```

## 📖 Aide rapide

```bash
# Backend
npm run dev              # Démarrer
npm run test:api         # Tester
npm run db:sync          # Sync DB
npm run generate:exercises  # Générer exercices IA

# Tests
curl http://localhost:3000/api/health  # Health check
psql -U postgres -d mathia             # DB console

# Documentation
open http://localhost:3000/api-docs    # Swagger
cat INDEX.md                           # Index complet
```

---

💡 **Astuce** : Ajoutez ce fichier à vos favoris pour un accès rapide aux commandes !





