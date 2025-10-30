# 🧪 Guide de Test de l'API Mathia

Ce guide explique comment tester tous les endpoints de l'API.

## 📋 Avant de commencer

### 1. Démarrer le serveur

```bash
npm run dev
```

Le serveur doit être accessible sur `http://localhost:3000`

### 2. Vérifier que la base de données est connectée

Vous devriez voir dans les logs :
```
✅ Connexion à PostgreSQL établie avec succès
✅ Modèles synchronisés avec la base de données
🚀 Serveur Mathia démarré avec succès
📍 URL: http://localhost:3000
```

## 🚀 Lancer les tests automatisés

### Option 1 : Script Node.js (recommandé)

```bash
npm run test:api
```

Ou directement :
```bash
node tests/test_api.js
```

### Option 2 : Script Bash (Linux/Mac)

```bash
npm run test:api:bash
```

Ou directement :
```bash
bash tests/test_api.sh
```

## 📊 Tests effectués

Les scripts testent automatiquement :

### ✅ 1. POST /auth/signup - Créer un compte

**Requête :**
```json
{
  "name": "Test User",
  "email": "test_1234567890@example.com",
  "password": "test123456"
}
```

**Réponse attendue (201 Created) :**
```json
{
  "success": true,
  "message": "Inscription réussie",
  "data": {
    "user": {
      "id": 1,
      "name": "Test User",
      "email": "test_1234567890@example.com",
      "createdAt": "2025-01-15T14:30:00.000Z",
      "updatedAt": "2025-01-15T14:30:00.000Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Vérifications :**
- ✅ Code HTTP 201
- ✅ Token JWT retourné
- ✅ password_hash non visible dans la réponse
- ✅ Email unique (409 si déjà utilisé)

---

### ✅ 2. POST /auth/login - Obtenir un JWT

**Requête :**
```json
{
  "email": "test_1234567890@example.com",
  "password": "test123456"
}
```

**Réponse attendue (200 OK) :**
```json
{
  "success": true,
  "message": "Connexion réussie",
  "data": {
    "user": {
      "id": 1,
      "name": "Test User",
      "email": "test_1234567890@example.com",
      "createdAt": "2025-01-15T14:30:00.000Z",
      "updatedAt": "2025-01-15T14:30:00.000Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Vérifications :**
- ✅ Code HTTP 200
- ✅ Token JWT retourné
- ✅ Infos utilisateur correctes
- ✅ Mot de passe incorrect → 401

---

### ✅ 3. GET /courses - Récupérer les cours

**Requête :**
```
GET /api/courses
Headers: Authorization: Bearer {token}
```

**Réponse attendue (200 OK) :**
```json
{
  "success": true,
  "data": {
    "courses": [
      {
        "id": 1,
        "title": "Les fractions",
        "grade": "6ème",
        "chapter": "Arithmétique",
        "description": "Apprendre les fractions simples",
        "createdAt": "2025-01-15T10:00:00.000Z",
        "updatedAt": "2025-01-15T10:00:00.000Z",
        "exercises": [
          {
            "id": 1,
            "type": "qcm",
            "difficulty": "facile"
          }
        ]
      }
    ]
  }
}
```

**Vérifications :**
- ✅ Code HTTP 200
- ✅ Liste de cours avec exercices
- ✅ Sans token → 401
- ✅ Ordre décroissant (plus récents d'abord)

---

### ✅ 4. GET /exercises - Lister tous les exercices

**Requête :**
```
GET /api/exercises
Headers: Authorization: Bearer {token}
```

**Réponse attendue (200 OK) :**
```json
{
  "success": true,
  "data": {
    "exercises": [
      {
        "id": 1,
        "courseId": 1,
        "type": "qcm",
        "body": "Quelle est la moitié de 10?",
        "options": {
          "A": "3",
          "B": "5",
          "C": "7",
          "D": "10"
        },
        "answer": "B",
        "explanation": "10 divisé par 2 égale 5",
        "difficulty": "facile",
        "tags": ["fractions", "division"],
        "createdAt": "2025-01-15T10:15:00.000Z",
        "updatedAt": "2025-01-15T10:15:00.000Z",
        "course": {
          "id": 1,
          "title": "Les fractions",
          "grade": "6ème",
          "chapter": "Arithmétique"
        }
      }
    ]
  }
}
```

**Vérifications :**
- ✅ Code HTTP 200
- ✅ Exercices avec infos du cours
- ✅ Tous les champs présents
- ✅ Sans token → 401

---

### ✅ 5. GET /exercises?courseId=1&difficulty=facile - Filtrer

**Requête :**
```
GET /api/exercises?courseId=1&difficulty=facile
Headers: Authorization: Bearer {token}
```

**Réponse attendue (200 OK) :**
```json
{
  "success": true,
  "data": {
    "exercises": [
      {
        "id": 1,
        "courseId": 1,
        "difficulty": "facile",
        ...
      }
    ]
  }
}
```

**Vérifications :**
- ✅ Filtrage par courseId fonctionne
- ✅ Filtrage par difficulty fonctionne
- ✅ Les deux filtres peuvent être combinés
- ✅ Retourne un tableau vide si aucun résultat

---

### ✅ 6. POST /attempts - Enregistrer une réponse

**Requête :**
```json
{
  "exerciseId": 1,
  "userAnswer": "B"
}
```

**Réponse attendue - Correcte (201 Created) :**
```json
{
  "success": true,
  "data": {
    "attempt": {
      "id": 1,
      "exerciseId": 1,
      "userAnswer": "B",
      "isCorrect": true,
      "createdAt": "2025-01-15T12:30:00.000Z"
    },
    "isCorrect": true,
    "explanation": "10 divisé par 2 égale 5",
    "correctAnswer": "B"
  }
}
```

**Réponse attendue - Incorrecte (201 Created) :**
```json
{
  "success": true,
  "data": {
    "attempt": {
      "id": 2,
      "exerciseId": 1,
      "userAnswer": "A",
      "isCorrect": false,
      "createdAt": "2025-01-15T12:31:00.000Z"
    },
    "isCorrect": false
  }
}
```

**Vérifications :**
- ✅ Code HTTP 201
- ✅ isCorrect calculé correctement
- ✅ Explication retournée si correct
- ✅ Explication cachée si incorrect
- ✅ Enregistrement en base de données
- ✅ Exercice inexistant → 404

---

### ✅ 7. Test sans authentification

**Requête :**
```
GET /api/courses
(sans header Authorization)
```

**Réponse attendue (401 Unauthorized) :**
```json
{
  "success": false,
  "message": "Accès non autorisé. Token manquant."
}
```

**Vérifications :**
- ✅ Code HTTP 401
- ✅ Protection JWT active
- ✅ Routes /auth accessibles sans token
- ✅ Autres routes bloquées sans token

---

## 🎯 Tests manuels avec curl

Si le serveur est démarré, testez manuellement :

### 1. Créer un compte

```bash
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Marie Dupont",
    "email": "marie@example.com",
    "password": "password123"
  }'
```

### 2. Se connecter

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "marie@example.com",
    "password": "password123"
  }'
```

**→ Copier le token de la réponse**

### 3. Exporter le token

```bash
# Linux/Mac
export TOKEN="votre_token_ici"

# Windows PowerShell
$TOKEN = "votre_token_ici"
```

### 4. Récupérer les cours

```bash
# Linux/Mac
curl http://localhost:3000/api/courses \
  -H "Authorization: Bearer $TOKEN"

# Windows PowerShell
curl http://localhost:3000/api/courses -Headers @{"Authorization"="Bearer $TOKEN"}
```

### 5. Filtrer les exercices

```bash
curl "http://localhost:3000/api/exercises?courseId=1&difficulty=facile" \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Soumettre une réponse

```bash
curl -X POST http://localhost:3000/api/attempts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exerciseId": 1,
    "userAnswer": "B"
  }'
```

---

## 🔍 Vérifier les données en base

```sql
-- Voir tous les utilisateurs
SELECT id, name, email, "createdAt" FROM users;

-- Voir toutes les tentatives
SELECT 
  u.name AS utilisateur,
  e.body AS question,
  a."userAnswer" AS reponse,
  a."isCorrect" AS correct,
  a."createdAt" AS date
FROM attempts a
JOIN users u ON a."userId" = u.id
JOIN exercises e ON a."exerciseId" = e.id
ORDER BY a."createdAt" DESC;

-- Compter les tentatives par utilisateur
SELECT 
  u.name,
  COUNT(*) AS total_tentatives,
  SUM(CASE WHEN a."isCorrect" THEN 1 ELSE 0 END) AS bonnes_reponses
FROM attempts a
JOIN users u ON a."userId" = u.id
GROUP BY u.name;
```

---

## 🐛 Dépannage

### ❌ "Connection refused" ou "ECONNREFUSED"

**Problème** : Le serveur n'est pas démarré

**Solution** :
```bash
npm run dev
```

Attendez de voir :
```
🚀 Serveur Mathia démarré avec succès
📍 URL: http://localhost:3000
```

---

### ❌ "Database connection failed"

**Problème** : PostgreSQL n'est pas démarré ou mal configuré

**Solution** :
1. Vérifier que PostgreSQL est démarré
2. Vérifier le fichier `.env` :
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/mathia
   ```
3. Créer la base si nécessaire :
   ```bash
   createdb mathia
   ```

---

### ❌ 404 sur POST /attempts

**Problème** : Aucun exercice en base de données

**Solution** : Créer un exercice via l'API :
```bash
curl -X POST http://localhost:3000/api/admin/exercises \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "courseId": 1,
    "type": "qcm",
    "body": "Quelle est la moitié de 10?",
    "options": {"A": "3", "B": "5", "C": "7", "D": "10"},
    "answer": "B",
    "explanation": "10 ÷ 2 = 5",
    "difficulty": "facile",
    "tags": ["fractions"]
  }'
```

---

### ❌ 401 Unauthorized

**Problème** : Token manquant, invalide ou expiré

**Solutions** :
1. Vérifier que vous incluez le header :
   ```
   Authorization: Bearer {token}
   ```
2. Générer un nouveau token :
   ```bash
   curl -X POST http://localhost:3000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"marie@example.com","password":"password123"}'
   ```
3. Vérifier JWT_SECRET dans `.env`

---

## 📊 Résultat attendu du script de test

```
======================================================================
🧪 TEST DE L'API MATHIA
======================================================================

📍 URL de base: http://localhost:3000/api
📧 Email de test: test_1705330000@example.com

✅ Inscription réussie
🔑 Token récupéré (152 caractères)
👤 User ID: 5

✅ Connexion réussie
🔑 Nouveau token récupéré

✅ Récupération des cours réussie
📚 Nombre de cours: 2

✅ Récupération des exercices réussie
📝 Nombre d'exercices: 5
🎯 Premier exercice ID: 1

✅ Filtrage des exercices réussi
📝 Exercices faciles du cours 1: 3

✅ Enregistrement de la réponse réussi
✓ Réponse enregistrée (Correcte: true)

✅ Protection JWT fonctionne correctement

======================================================================
📊 RÉSUMÉ DES TESTS
======================================================================

✅ Tests terminés
```

---

## 🎉 Checklist complète

Avant de dire que tout fonctionne :

- [ ] Serveur démarré (`npm run dev`)
- [ ] Base de données connectée
- [ ] POST /auth/signup → 201 Created
- [ ] POST /auth/login → 200 OK avec token
- [ ] GET /courses → 200 OK (avec token)
- [ ] GET /exercises → 200 OK (avec token)
- [ ] GET /exercises?courseId=1&difficulty=facile → 200 OK
- [ ] POST /attempts → 201 Created (avec token)
- [ ] GET /courses (sans token) → 401 Unauthorized
- [ ] Validation Joi fonctionne (email invalide → 400)
- [ ] Password hashé (pas visible en base)

---

✅ **Tous les endpoints testés et fonctionnels !**









