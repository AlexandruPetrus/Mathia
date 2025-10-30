# 📍 Routes de l'API Mathia

Toutes les routes sont préfixées par `/api`.

## 🔓 Routes publiques (sans JWT)

### Authentification - `/api/auth`

| Méthode | Route | Description | Body |
|---------|-------|-------------|------|
| POST | `/auth/signup` | Inscription (hash password + JWT) | `{ name, email, password }` |
| POST | `/auth/login` | Connexion (retour JWT) | `{ email, password }` |

**Réponse d'authentification :**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "name": "Marie Dupont",
      "email": "marie@example.com",
      "createdAt": "2025-01-01T10:00:00Z",
      "updatedAt": "2025-01-01T10:00:00Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

## 🔒 Routes protégées (JWT requis)

**Header requis :** `Authorization: Bearer {token}`

### Cours - `/api/courses`

| Méthode | Route | Description | Query Params |
|---------|-------|-------------|--------------|
| GET | `/courses` | GET tous les cours | - |
| GET | `/courses/:id` | GET un cours par ID avec ses exercices | - |

**Exemple réponse GET /courses :**
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
        "createdAt": "2025-01-01T10:00:00Z",
        "updatedAt": "2025-01-01T10:00:00Z",
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

### Exercices - `/api/exercises`

| Méthode | Route | Description | Query Params |
|---------|-------|-------------|--------------|
| GET | `/exercises` | GET tous les exercices avec filtrage | `?courseId=1&difficulty=facile` |

**Filtres disponibles :**
- `courseId` : Filtrer par ID de cours (INTEGER)
- `difficulty` : Filtrer par difficulté ("facile", "moyen", "difficile")

**Exemple réponse GET /exercises?courseId=1&difficulty=facile :**
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
        "createdAt": "2025-01-01T10:00:00Z",
        "updatedAt": "2025-01-01T10:00:00Z",
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

### Tentatives - `/api/attempts`

| Méthode | Route | Description | Body |
|---------|-------|-------------|------|
| POST | `/attempts` | Enregistrer une réponse et vérifier si elle est correcte | `{ exerciseId, userAnswer }` |

**Body :**
```json
{
  "exerciseId": 1,
  "userAnswer": "B"
}
```

**Exemple réponse (correcte) :**
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

**Exemple réponse (incorrecte) :**
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

### Admin - `/api/admin`

| Méthode | Route | Description | Body |
|---------|-------|-------------|------|
| POST | `/admin/exercises` | Ajouter un exercice manuellement | `{ courseId, type, body, options, answer, explanation, difficulty, tags }` |

**Body exemple :**
```json
{
  "courseId": 1,
  "type": "qcm",
  "body": "Combien font 5 + 3?",
  "options": {
    "A": "6",
    "B": "7",
    "C": "8",
    "D": "9"
  },
  "answer": "C",
  "explanation": "5 plus 3 égale 8",
  "difficulty": "facile",
  "tags": ["addition", "base"]
}
```

**Réponse :**
```json
{
  "success": true,
  "message": "Exercice créé avec succès",
  "data": {
    "exercise": {
      "id": 2,
      "courseId": 1,
      "type": "qcm",
      "body": "Combien font 5 + 3?",
      "options": {
        "A": "6",
        "B": "7",
        "C": "8",
        "D": "9"
      },
      "answer": "C",
      "explanation": "5 plus 3 égale 8",
      "difficulty": "facile",
      "tags": ["addition", "base"],
      "createdAt": "2025-01-01T14:00:00Z",
      "updatedAt": "2025-01-01T14:00:00Z"
    }
  }
}
```

---

## 🔑 Authentification JWT

### Comment utiliser le JWT

1. **Obtenir le token** via `/auth/signup` ou `/auth/login`
2. **Inclure le token** dans toutes les requêtes protégées :
   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### Exemple avec curl

```bash
# 1. S'inscrire et récupérer le token
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Marie","email":"marie@test.com","password":"password123"}'

# Réponse : { "data": { "token": "eyJ..." } }

# 2. Utiliser le token pour accéder aux ressources
TOKEN="eyJ..."

curl -X GET http://localhost:3000/api/courses \
  -H "Authorization: Bearer $TOKEN"

curl -X GET "http://localhost:3000/api/exercises?courseId=1&difficulty=facile" \
  -H "Authorization: Bearer $TOKEN"

curl -X POST http://localhost:3000/api/attempts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"exerciseId":1,"userAnswer":"B"}'
```

---

## 🛡️ Sécurité

- ✅ **Mot de passe hashé** automatiquement avec bcrypt (10 rounds)
- ✅ **JWT valide 7 jours** par défaut (configurable via JWT_EXPIRES_IN)
- ✅ **Validation des données** avec Joi sur tous les endpoints
- ✅ **Protection JWT** sur toutes les routes sauf `/auth/*` et `/health`
- ✅ **Rate limiting** : 100 requêtes par 15 minutes
- ✅ **Helmet** pour sécuriser les headers HTTP
- ✅ **CORS** configuré

---

## 📊 Codes de réponse HTTP

| Code | Signification |
|------|---------------|
| 200 | Succès |
| 201 | Créé avec succès |
| 400 | Requête invalide (validation échouée) |
| 401 | Non authentifié (JWT manquant ou invalide) |
| 404 | Ressource non trouvée |
| 409 | Conflit (ex: email déjà utilisé) |
| 500 | Erreur serveur |

---

## 🧪 Tests avec Postman/Insomnia

Importez cette collection pour tester rapidement :

**Base URL :** `http://localhost:3000/api`

**Variables d'environnement :**
- `base_url` : `http://localhost:3000/api`
- `token` : (à définir après signup/login)

**Routes à tester dans l'ordre :**
1. POST /auth/signup → Sauvegarder le token
2. POST /auth/login → Vérifier le token
3. GET /courses (avec token)
4. GET /courses/1 (avec token)
5. GET /exercises?courseId=1 (avec token)
6. POST /attempts (avec token)
7. POST /admin/exercises (avec token)









