# 🧪 Test de l'API Mathia

Guide rapide pour tester toutes les routes de l'API.

## 🚀 Démarrage

```bash
# 1. Démarrer le serveur
npm run dev

# Le serveur est accessible sur http://localhost:3000
```

## 📝 Tests avec curl

### 1️⃣ Inscription (/auth/signup)

```bash
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Marie Dupont",
    "email": "marie@example.com",
    "password": "password123"
  }'
```

**Réponse attendue :**
```json
{
  "success": true,
  "message": "Inscription réussie",
  "data": {
    "user": {
      "id": 1,
      "name": "Marie Dupont",
      "email": "marie@example.com",
      "createdAt": "...",
      "updatedAt": "..."
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

✅ **Vérifications :**
- Le mot de passe est hashé automatiquement avec bcrypt
- Un JWT est généré et retourné
- Le password_hash n'apparaît pas dans la réponse

---

### 2️⃣ Connexion (/auth/login)

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "marie@example.com",
    "password": "password123"
  }'
```

**Réponse attendue :**
```json
{
  "success": true,
  "message": "Connexion réussie",
  "data": {
    "user": { ... },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

✅ **Vérifications :**
- Le JWT est retourné
- Mauvais mot de passe → 401 Unauthorized

**💡 Sauvegarder le token dans une variable :**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### 3️⃣ Créer des cours (pour les tests suivants)

**Note:** Cette route n'est pas dans les spécifications, mais pour tester, vous pouvez créer un cours directement en base :

```sql
-- Depuis psql
INSERT INTO courses (title, grade, chapter, description, "createdAt", "updatedAt")
VALUES 
  ('Les fractions', '6ème', 'Arithmétique', 'Apprendre les fractions simples', NOW(), NOW()),
  ('Les équations', '3ème', 'Algèbre', 'Résoudre des équations du premier degré', NOW(), NOW());
```

---

### 4️⃣ GET tous les cours (/courses)

```bash
curl -X GET http://localhost:3000/api/courses \
  -H "Authorization: Bearer $TOKEN"
```

**Réponse attendue :**
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
        "createdAt": "...",
        "updatedAt": "...",
        "exercises": []
      }
    ]
  }
}
```

✅ **Vérifications :**
- Sans token → 401 Unauthorized
- Avec token → Liste complète des cours avec leurs exercices

---

### 5️⃣ GET un cours par ID (/courses/:id)

```bash
curl -X GET http://localhost:3000/api/courses/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Réponse attendue :**
```json
{
  "success": true,
  "data": {
    "course": {
      "id": 1,
      "title": "Les fractions",
      "grade": "6ème",
      "chapter": "Arithmétique",
      "description": "Apprendre les fractions simples",
      "createdAt": "...",
      "updatedAt": "...",
      "exercises": [
        {
          "id": 1,
          "courseId": 1,
          "type": "qcm",
          "body": "Quelle est la moitié de 10?",
          ...
        }
      ]
    }
  }
}
```

✅ **Vérifications :**
- ID inexistant → 404 Not Found
- Retourne le cours avec tous ses exercices

---

### 6️⃣ POST ajouter un exercice (/admin/exercises)

```bash
curl -X POST http://localhost:3000/api/admin/exercises \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
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
    "tags": ["fractions", "division"]
  }'
```

**Réponse attendue :**
```json
{
  "success": true,
  "message": "Exercice créé avec succès",
  "data": {
    "exercise": {
      "id": 1,
      "courseId": 1,
      "type": "qcm",
      "body": "Quelle est la moitié de 10?",
      "options": { "A": "3", "B": "5", "C": "7", "D": "10" },
      "answer": "B",
      "explanation": "10 divisé par 2 égale 5",
      "difficulty": "facile",
      "tags": ["fractions", "division"],
      "createdAt": "...",
      "updatedAt": "..."
    }
  }
}
```

✅ **Vérifications :**
- L'exercice est créé avec tous les champs
- courseId inexistant → 404 Course Not Found

---

### 7️⃣ GET tous les exercices (/exercises)

**Sans filtre :**
```bash
curl -X GET http://localhost:3000/api/exercises \
  -H "Authorization: Bearer $TOKEN"
```

**Avec filtrage par courseId :**
```bash
curl -X GET "http://localhost:3000/api/exercises?courseId=1" \
  -H "Authorization: Bearer $TOKEN"
```

**Avec filtrage par difficulty :**
```bash
curl -X GET "http://localhost:3000/api/exercises?difficulty=facile" \
  -H "Authorization: Bearer $TOKEN"
```

**Avec les deux filtres :**
```bash
curl -X GET "http://localhost:3000/api/exercises?courseId=1&difficulty=facile" \
  -H "Authorization: Bearer $TOKEN"
```

**Réponse attendue :**
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
        "options": { ... },
        "answer": "B",
        "explanation": "10 divisé par 2 égale 5",
        "difficulty": "facile",
        "tags": ["fractions", "division"],
        "createdAt": "...",
        "updatedAt": "...",
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

✅ **Vérifications :**
- Le filtrage par courseId fonctionne
- Le filtrage par difficulty fonctionne
- Les deux filtres peuvent être combinés
- Chaque exercice inclut les infos du cours

---

### 8️⃣ POST soumettre une réponse (/attempts)

**Réponse correcte :**
```bash
curl -X POST http://localhost:3000/api/attempts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exerciseId": 1,
    "userAnswer": "B"
  }'
```

**Réponse attendue (correcte) :**
```json
{
  "success": true,
  "data": {
    "attempt": {
      "id": 1,
      "exerciseId": 1,
      "userAnswer": "B",
      "isCorrect": true,
      "createdAt": "2025-01-01T12:30:00Z"
    },
    "isCorrect": true,
    "explanation": "10 divisé par 2 égale 5",
    "correctAnswer": "B"
  }
}
```

**Réponse incorrecte :**
```bash
curl -X POST http://localhost:3000/api/attempts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exerciseId": 1,
    "userAnswer": "A"
  }'
```

**Réponse attendue (incorrecte) :**
```json
{
  "success": true,
  "data": {
    "attempt": {
      "id": 2,
      "exerciseId": 1,
      "userAnswer": "A",
      "isCorrect": false,
      "createdAt": "2025-01-01T12:31:00Z"
    },
    "isCorrect": false
  }
}
```

✅ **Vérifications :**
- La réponse est bien vérifiée (comparaison insensible à la casse)
- L'attempt est enregistré en base de données
- Si correct → l'explication et la bonne réponse sont retournées
- Si incorrect → seul le résultat est retourné (pas d'explication)

---

## 🔒 Test de la sécurité JWT

### Sans token (doit échouer) :
```bash
curl -X GET http://localhost:3000/api/courses
```

**Réponse attendue :**
```json
{
  "success": false,
  "message": "Accès non autorisé. Token manquant."
}
```

### Avec un mauvais token (doit échouer) :
```bash
curl -X GET http://localhost:3000/api/courses \
  -H "Authorization: Bearer invalid_token_here"
```

**Réponse attendue :**
```json
{
  "success": false,
  "message": "Token invalide."
}
```

✅ **Vérifications :**
- Routes /auth/* accessibles sans token
- Toutes les autres routes nécessitent un JWT valide
- Mauvais token → 401 Unauthorized

---

## 📊 Vérification en base de données

```sql
-- Voir les utilisateurs créés
SELECT id, name, email, "createdAt" FROM users;

-- Voir les tentatives d'un utilisateur
SELECT u.name, e.body, a."userAnswer", a."isCorrect", a."createdAt"
FROM attempts a
JOIN users u ON a."userId" = u.id
JOIN exercises e ON a."exerciseId" = e.id
ORDER BY a."createdAt" DESC;

-- Vérifier que le mot de passe est bien hashé
SELECT email, password_hash FROM users;
-- password_hash doit commencer par $2a$ ou $2b$ (bcrypt)
```

---

## ✅ Checklist complète

- [ ] POST /auth/signup → Inscription avec hash bcrypt + JWT
- [ ] POST /auth/login → Connexion avec retour JWT
- [ ] GET /courses → Liste tous les cours (JWT requis)
- [ ] GET /courses/:id → Détails d'un cours (JWT requis)
- [ ] GET /exercises → Liste avec filtres courseId et difficulty (JWT requis)
- [ ] POST /attempts → Enregistre et vérifie la réponse (JWT requis)
- [ ] POST /admin/exercises → Ajoute un exercice (JWT requis)
- [ ] Routes /auth accessibles sans JWT
- [ ] Toutes les autres routes bloquées sans JWT
- [ ] Validation Joi sur toutes les routes

---

## 🎯 Scénario complet

```bash
# 1. Créer un compte
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@test.com","password":"test123"}'

# 2. Récupérer le token et le sauvegarder
TOKEN="votre_token_ici"

# 3. Créer un exercice
curl -X POST http://localhost:3000/api/admin/exercises \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"courseId":1,"type":"libre","body":"Combien font 2+2?","answer":"4","difficulty":"facile"}'

# 4. Lister les exercices
curl -X GET http://localhost:3000/api/exercises \
  -H "Authorization: Bearer $TOKEN"

# 5. Répondre à l'exercice
curl -X POST http://localhost:3000/api/attempts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"exerciseId":1,"userAnswer":"4"}'
```

🎉 Toutes les routes fonctionnent !









