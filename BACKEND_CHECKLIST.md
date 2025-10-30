# ✅ Checklist Backend Mathia - Fonctionnalité complète

Ce document vérifie que le backend est totalement fonctionnel et prêt pour l'app iOS.

## 🔧 Configuration

### ✅ Variables d'environnement

Vérifier que le fichier `.env` existe et contient :

```bash
cat .env
```

Doit contenir :
```env
PORT=3000
DATABASE_URL=postgresql://user:password@localhost:5432/mathia
JWT_SECRET=super_secret_jwt_key
OPENAI_API_KEY=sk-xxxxxx
```

**Test** :
```bash
node -e "require('dotenv').config(); console.log('✓ PORT:', process.env.PORT); console.log('✓ DATABASE_URL:', process.env.DATABASE_URL ? 'Défini' : 'Manquant'); console.log('✓ JWT_SECRET:', process.env.JWT_SECRET ? 'Défini' : 'Manquant')"
```

### ✅ Dépendances installées

```bash
npm install
```

Vérifier que `node_modules/` existe et contient :
- express
- sequelize
- pg
- jsonwebtoken
- bcryptjs
- dotenv
- cors
- helmet
- joi

### ✅ Base de données PostgreSQL

**Vérifier que PostgreSQL est démarré** :
```bash
# Mac
brew services list | grep postgresql

# Linux
sudo service postgresql status

# Windows
pg_ctl status
```

**Créer la base de données** :
```bash
createdb mathia

# Ou depuis psql
psql -U postgres -c "CREATE DATABASE mathia;"
```

**Synchroniser les modèles** :
```bash
npm run db:sync
```

Doit afficher :
```
✅ Connexion à PostgreSQL établie avec succès
✅ Modèles synchronisés avec la base de données
```

## 🚀 Démarrage du serveur

### ✅ Lancer le serveur

```bash
npm run dev
```

**Sortie attendue** :
```
✅ Connexion à PostgreSQL établie avec succès
✅ Modèles synchronisés avec la base de données

🚀 ========================================
🎓 Serveur Mathia démarré avec succès
📍 URL: http://localhost:3000
📚 Documentation: http://localhost:3000/api-docs
🌍 Environnement: development
🚀 ========================================
```

### ✅ Vérifier que le serveur répond

```bash
curl http://localhost:3000/api/health
```

**Réponse attendue** :
```json
{
  "success": true,
  "message": "API Mathia fonctionnelle",
  "timestamp": "2025-01-15T14:30:00.000Z"
}
```

## 🧪 Tests des endpoints

### ✅ 1. POST /auth/signup

```bash
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Backend",
    "email": "backend_test@example.com",
    "password": "test123456"
  }'
```

**Vérifications** :
- ✅ Status: 201 Created
- ✅ Retourne un objet `user` (sans password_hash)
- ✅ Retourne un `token` JWT
- ✅ Email dupliqué → 409 Conflict

### ✅ 2. POST /auth/login

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "backend_test@example.com",
    "password": "test123456"
  }'
```

**Vérifications** :
- ✅ Status: 200 OK
- ✅ Retourne un token JWT
- ✅ Mauvais password → 401 Unauthorized

**→ Sauvegarder le token** :
```bash
export TOKEN="votre_token_ici"
```

### ✅ 3. GET /courses (avec JWT)

```bash
curl http://localhost:3000/api/courses \
  -H "Authorization: Bearer $TOKEN"
```

**Vérifications** :
- ✅ Status: 200 OK
- ✅ Retourne un tableau de cours
- ✅ Chaque cours a : id, title, grade, chapter, description, exercises[]
- ✅ Sans token → 401 Unauthorized

### ✅ 4. GET /exercises (avec filtres)

**Sans filtre** :
```bash
curl http://localhost:3000/api/exercises \
  -H "Authorization: Bearer $TOKEN"
```

**Avec courseId** :
```bash
curl "http://localhost:3000/api/exercises?courseId=1" \
  -H "Authorization: Bearer $TOKEN"
```

**Avec difficulty** :
```bash
curl "http://localhost:3000/api/exercises?difficulty=facile" \
  -H "Authorization: Bearer $TOKEN"
```

**Les deux filtres** :
```bash
curl "http://localhost:3000/api/exercises?courseId=1&difficulty=facile" \
  -H "Authorization: Bearer $TOKEN"
```

**Vérifications** :
- ✅ Status: 200 OK
- ✅ Filtrage par courseId fonctionne
- ✅ Filtrage par difficulty fonctionne
- ✅ Les deux filtres peuvent être combinés
- ✅ Retourne un tableau d'exercices avec infos du cours

### ✅ 5. POST /admin/exercises

```bash
curl -X POST http://localhost:3000/api/admin/exercises \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "courseId": 1,
    "type": "qcm",
    "body": "Test: Quelle est la moitié de 10?",
    "options": {"A": "3", "B": "5", "C": "7", "D": "10"},
    "answer": "B",
    "explanation": "10 divisé par 2 égale 5",
    "difficulty": "facile",
    "tags": ["test"]
  }'
```

**Vérifications** :
- ✅ Status: 201 Created
- ✅ Exercice créé en base de données
- ✅ Retourne l'exercice avec son ID
- ✅ Course inexistant → 404 Not Found

### ✅ 6. POST /attempts

```bash
curl -X POST http://localhost:3000/api/attempts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exerciseId": 1,
    "userAnswer": "B"
  }'
```

**Vérifications** :
- ✅ Status: 201 Created
- ✅ Retourne `isCorrect: true` ou `false`
- ✅ Si correct → retourne `explanation` et `correctAnswer`
- ✅ Si incorrect → pas d'explication
- ✅ Tentative enregistrée en base

## 🗄️ Vérifications en base de données

### ✅ Tables créées

```sql
-- Vérifier que toutes les tables existent
\dt
```

Doit afficher :
```
 public | attempts  | table | postgres
 public | courses   | table | postgres
 public | exercises | table | postgres
 public | users     | table | postgres
```

### ✅ Structure des tables

```sql
-- User
\d users
-- Colonnes: id, name, email, password_hash, createdAt, updatedAt

-- Course
\d courses
-- Colonnes: id, title, grade, chapter, description, createdAt, updatedAt

-- Exercise
\d exercises
-- Colonnes: id, courseId, type, body, options, answer, explanation, difficulty, tags, createdAt, updatedAt

-- Attempt
\d attempts
-- Colonnes: id, userId, exerciseId, userAnswer, isCorrect, createdAt
```

### ✅ Données de test

**Utilisateurs** :
```sql
SELECT id, name, email FROM users;
```

**Cours** :
```sql
SELECT id, title, grade, chapter FROM courses;
```

**Exercices** :
```sql
SELECT id, "courseId", type, body, difficulty FROM exercises LIMIT 5;
```

**Tentatives** :
```sql
SELECT u.name, e.body, a."userAnswer", a."isCorrect" 
FROM attempts a
JOIN users u ON a."userId" = u.id
JOIN exercises e ON a."exerciseId" = e.id
LIMIT 5;
```

### ✅ Relations

```sql
-- Vérifier les foreign keys
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';
```

## 🔐 Sécurité

### ✅ Password hashé

```sql
SELECT email, password_hash FROM users LIMIT 1;
```

Le `password_hash` doit commencer par `$2a$` ou `$2b$` (bcrypt).

### ✅ JWT généré

Les tokens doivent avoir 3 parties séparées par des points :
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsImlhdCI6MTYxMDAwMDAwMH0.signature
```

### ✅ Protection des routes

```bash
# Sans token → doit retourner 401
curl http://localhost:3000/api/courses

# Avec mauvais token → doit retourner 401
curl http://localhost:3000/api/courses \
  -H "Authorization: Bearer invalid_token"

# Avec bon token → doit retourner 200
curl http://localhost:3000/api/courses \
  -H "Authorization: Bearer $TOKEN"
```

## 📚 Documentation

### ✅ Swagger accessible

Ouvrir dans le navigateur :
```
http://localhost:3000/api-docs
```

Doit afficher l'interface Swagger UI avec toutes les routes documentées.

### ✅ Fichiers de documentation présents

- [ ] `README.md` - Documentation principale
- [ ] `QUICK_START.md` - Guide de démarrage rapide
- [ ] `ROUTES.md` - Documentation des routes
- [ ] `TEST_API.md` - Guide de test
- [ ] `TESTING_GUIDE.md` - Guide complet des tests
- [ ] `ENV_SETUP.md` - Configuration environnement
- [ ] `CREATE_ENV.md` - Création du .env
- [ ] `AI_GENERATION_GUIDE.md` - Génération IA
- [ ] `docs/openapi.yaml` - Spécification OpenAPI
- [ ] `docs/SWAGGER_GUIDE.md` - Guide Swagger

## 🤖 Génération IA (optionnel)

### ✅ Script Python fonctionnel

```bash
python scripts/ai_generate_exercises.py \
  --chapter "Test" \
  --grade "6ème" \
  --difficulty "facile" \
  --type "qcm" \
  --count 1
```

Doit créer `backend/data/generated_exercises.json`.

## 📊 Résumé final

Si tous ces points sont validés, le backend est **totalement fonctionnel** :

### Configuration
- [x] Variables d'environnement (.env)
- [x] Dépendances Node.js installées
- [x] Dépendances Python installées (optionnel)
- [x] PostgreSQL démarré
- [x] Base de données créée

### Modèles
- [x] User (id, name, email, password_hash)
- [x] Course (id, title, grade, chapter, description)
- [x] Exercise (id, courseId, type, body, options, answer, explanation, difficulty, tags)
- [x] Attempt (id, userId, exerciseId, userAnswer, isCorrect, createdAt)

### Routes
- [x] POST /auth/signup (public)
- [x] POST /auth/login (public)
- [x] GET /courses (JWT requis)
- [x] GET /courses/:id (JWT requis)
- [x] GET /exercises (JWT requis, filtres: courseId, difficulty)
- [x] POST /attempts (JWT requis)
- [x] POST /admin/exercises (JWT requis)

### Sécurité
- [x] Password hashé avec bcrypt
- [x] JWT sur toutes les routes sauf /auth
- [x] Validation Joi sur tous les endpoints
- [x] CORS configuré
- [x] Helmet activé
- [x] Rate limiting actif

### Documentation
- [x] README complet
- [x] Swagger accessible
- [x] Guides de test
- [x] Documentation OpenAPI

### Tests
- [x] Scripts de test automatisés
- [x] Tous les endpoints testés
- [x] Protection JWT vérifiée

## 🎉 État du backend

Le backend Mathia est **100% fonctionnel** et prêt pour :

✅ Connexion avec l'app iOS SwiftUI  
✅ Utilisation en développement  
✅ Déploiement en production (après configuration HTTPS)  
✅ Génération d'exercices avec IA  
✅ Tests automatisés  

## 🔗 Prochaines étapes

1. **Lancer le backend** : `npm run dev`
2. **Ouvrir l'app iOS** dans Xcode
3. **Créer des cours et exercices** via l'API ou le script IA
4. **Tester le flux complet** depuis l'app iOS

---

🚀 **Le backend est prêt pour l'app iOS !**





