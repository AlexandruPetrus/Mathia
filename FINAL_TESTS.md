# 🧪 Tests finaux - Validation complète de l'API Mathia

Ce guide teste tous les endpoints demandés pour valider que le backend est totalement fonctionnel.

## 🚀 Préparation

### 1. Démarrer le serveur

```bash
npm run dev
```

**Attendez de voir** :
```
✅ Connexion à PostgreSQL établie avec succès
✅ Modèles synchronisés avec la base de données
🚀 Serveur Mathia démarré avec succès
📍 URL: http://localhost:3000
```

### 2. Ouvrir un nouveau terminal

Tous les tests ci-dessous se font dans un nouveau terminal pendant que le serveur tourne.

---

## 📝 Tests des endpoints

### ✅ TEST 1 : POST /auth/signup → Créer un compte

```bash
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Marie Dupont",
    "email": "marie@example.com",
    "password": "password123"
  }'
```

**📥 Réponse attendue :**
```json
{
  "success": true,
  "message": "Inscription réussie",
  "data": {
    "user": {
      "id": 1,
      "name": "Marie Dupont",
      "email": "marie@example.com",
      "createdAt": "2025-01-15T14:30:00.000Z",
      "updatedAt": "2025-01-15T14:30:00.000Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsImlhdCI6MTcwNTMzMDAwMCwiZXhwIjoxNzA1OTM0ODAwfQ.signature_here"
  }
}
```

**✅ Vérifications :**
- Code HTTP : **201 Created**
- Token JWT présent (3 parties séparées par des points)
- password_hash **non visible** dans la réponse
- ID utilisateur généré automatiquement

**🔑 IMPORTANT : Copiez le token !**

---

### ✅ TEST 2 : POST /auth/login → Obtenir un JWT

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "marie@example.com",
    "password": "password123"
  }'
```

**📥 Réponse attendue :**
```json
{
  "success": true,
  "message": "Connexion réussie",
  "data": {
    "user": {
      "id": 1,
      "name": "Marie Dupont",
      "email": "marie@example.com",
      "createdAt": "2025-01-15T14:30:00.000Z",
      "updatedAt": "2025-01-15T14:30:00.000Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**✅ Vérifications :**
- Code HTTP : **200 OK**
- Même utilisateur que signup
- Nouveau token généré
- Mauvais password → **401 Unauthorized**

**💾 Sauvegarder le token dans une variable :**

```bash
# Linux/Mac/Git Bash
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Windows PowerShell
$env:TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Windows CMD
set TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### ✅ TEST 3 : GET /courses → Récupérer les cours

```bash
curl http://localhost:3000/api/courses \
  -H "Authorization: Bearer $TOKEN"
```

**📥 Réponse attendue :**
```json
{
  "success": true,
  "data": {
    "courses": [
      {
        "id": 3,
        "title": "Les équations",
        "grade": "3ème",
        "chapter": "Algèbre",
        "description": "Résoudre des équations du premier degré",
        "createdAt": "2025-01-15T10:02:00.000Z",
        "updatedAt": "2025-01-15T10:02:00.000Z",
        "exercises": []
      },
      {
        "id": 2,
        "title": "Géométrie de base",
        "grade": "6ème",
        "chapter": "Géométrie",
        "description": "Les formes géométriques",
        "createdAt": "2025-01-15T10:01:00.000Z",
        "updatedAt": "2025-01-15T10:01:00.000Z",
        "exercises": []
      },
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

**✅ Vérifications :**
- Code HTTP : **200 OK**
- Tableau de cours (peut être vide si pas de données)
- Chaque cours a : id, title, grade, chapter, description
- Exercices associés (tableau peut être vide)
- Ordre décroissant (plus récents d'abord)
- **Sans token** → **401 Unauthorized**

---

### ✅ TEST 4 : GET /exercises?courseId=1&difficulty=facile → Filtrer les exercices

**Test 4a : Tous les exercices (sans filtre)**

```bash
curl http://localhost:3000/api/exercises \
  -H "Authorization: Bearer $TOKEN"
```

**Test 4b : Filtre par courseId**

```bash
curl "http://localhost:3000/api/exercises?courseId=1" \
  -H "Authorization: Bearer $TOKEN"
```

**Test 4c : Filtre par difficulty**

```bash
curl "http://localhost:3000/api/exercises?difficulty=facile" \
  -H "Authorization: Bearer $TOKEN"
```

**Test 4d : Les deux filtres combinés**

```bash
curl "http://localhost:3000/api/exercises?courseId=1&difficulty=facile" \
  -H "Authorization: Bearer $TOKEN"
```

**📥 Réponse attendue :**
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

**✅ Vérifications :**
- Code HTTP : **200 OK**
- Filtrage par `courseId` fonctionne
- Filtrage par `difficulty` fonctionne
- Les deux filtres peuvent être combinés
- Chaque exercice inclut les infos du cours
- Tableau vide `[]` si aucun résultat

---

### ✅ TEST 5 : POST /attempts → Enregistrer une réponse

**Test 5a : Réponse correcte**

```bash
curl -X POST http://localhost:3000/api/attempts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exerciseId": 1,
    "userAnswer": "B"
  }'
```

**📥 Réponse attendue (correcte) :**
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

**Test 5b : Réponse incorrecte**

```bash
curl -X POST http://localhost:3000/api/attempts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exerciseId": 1,
    "userAnswer": "A"
  }'
```

**📥 Réponse attendue (incorrecte) :**
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

**✅ Vérifications :**
- Code HTTP : **201 Created**
- `isCorrect` calculé automatiquement
- Si **correct** : `explanation` et `correctAnswer` présents
- Si **incorrect** : pas d'explication (pour ne pas donner la réponse)
- Comparaison insensible à la casse (trim + lowercase)
- Tentative enregistrée en base de données

**🔍 Vérifier en base :**
```sql
SELECT * FROM attempts ORDER BY "createdAt" DESC LIMIT 5;
```

---

## ✅ TEST BONUS : Protection JWT

### Test sans token (doit échouer)

```bash
curl http://localhost:3000/api/courses
```

**📥 Réponse attendue :**
```json
{
  "success": false,
  "message": "Accès non autorisé. Token manquant."
}
```

**Code HTTP : 401 Unauthorized** ✅

### Test avec mauvais token (doit échouer)

```bash
curl http://localhost:3000/api/courses \
  -H "Authorization: Bearer invalid_token_here"
```

**📥 Réponse attendue :**
```json
{
  "success": false,
  "message": "Token invalide."
}
```

**Code HTTP : 401 Unauthorized** ✅

---

## 📊 Récapitulatif des tests

| Endpoint | Méthode | JWT | Test | Résultat attendu |
|----------|---------|-----|------|------------------|
| `/auth/signup` | POST | ❌ Non | Créer compte | 201 + token |
| `/auth/login` | POST | ❌ Non | Se connecter | 200 + token |
| `/courses` | GET | ✅ Oui | Liste cours | 200 + tableau |
| `/exercises` | GET | ✅ Oui | Liste exercices | 200 + tableau |
| `/exercises?courseId=1&difficulty=facile` | GET | ✅ Oui | Filtre exercices | 200 + filtré |
| `/attempts` | POST | ✅ Oui | Soumettre réponse | 201 + isCorrect |
| `/courses` sans JWT | GET | ❌ Non | Test sécurité | 401 |

## ✅ Checklist finale

Vérifier que **TOUS** ces points sont validés :

### Configuration
- [ ] Serveur démarré sur port 3000
- [ ] PostgreSQL connecté
- [ ] Tables créées (users, courses, exercises, attempts)
- [ ] Fichier .env configuré

### Endpoints publics (sans JWT)
- [ ] POST /auth/signup → 201 Created
- [ ] POST /auth/login → 200 OK
- [ ] Token JWT retourné dans les deux cas
- [ ] Password hashé (bcrypt, commence par $2)

### Endpoints protégés (avec JWT)
- [ ] GET /courses → 200 OK
- [ ] GET /courses/:id → 200 OK
- [ ] GET /exercises → 200 OK
- [ ] GET /exercises?courseId=1 → 200 OK avec filtre
- [ ] GET /exercises?difficulty=facile → 200 OK avec filtre
- [ ] GET /exercises?courseId=1&difficulty=facile → 200 OK avec les deux filtres
- [ ] POST /attempts → 201 Created
- [ ] POST /admin/exercises → 201 Created

### Sécurité
- [ ] Routes protégées sans JWT → 401
- [ ] Mauvais token → 401
- [ ] Token expiré → 401
- [ ] Validation Joi fonctionne (email invalide → 400)

### Vérification des données
- [ ] isCorrect calculé correctement (B == B → true, A == B → false)
- [ ] Explication retournée si réponse correcte
- [ ] Explication cachée si réponse incorrecte
- [ ] Tentatives enregistrées en base

---

## 🎯 Script de test complet (copier-coller)

```bash
#!/bin/bash

echo "🧪 Tests de l'API Mathia"
echo ""

# 1. Signup
echo "1️⃣ POST /auth/signup"
SIGNUP=$(curl -s -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test_final@example.com","password":"test123"}')

echo "$SIGNUP" | jq '.'
TOKEN=$(echo "$SIGNUP" | jq -r '.data.token')
echo "✅ Token: ${TOKEN:0:30}..."
echo ""
sleep 1

# 2. Login
echo "2️⃣ POST /auth/login"
curl -s -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test_final@example.com","password":"test123"}' | jq '.'
echo ""
sleep 1

# 3. Courses
echo "3️⃣ GET /courses"
curl -s http://localhost:3000/api/courses \
  -H "Authorization: Bearer $TOKEN" | jq '.'
echo ""
sleep 1

# 4. Exercises sans filtre
echo "4️⃣ GET /exercises (sans filtre)"
curl -s http://localhost:3000/api/exercises \
  -H "Authorization: Bearer $TOKEN" | jq '.data.exercises | length' 
echo "exercices trouvés"
echo ""
sleep 1

# 5. Exercises avec filtres
echo "5️⃣ GET /exercises?courseId=1&difficulty=facile"
curl -s "http://localhost:3000/api/exercises?courseId=1&difficulty=facile" \
  -H "Authorization: Bearer $TOKEN" | jq '.'
echo ""
sleep 1

# 6. Attempts
echo "6️⃣ POST /attempts (réponse test)"
curl -s -X POST http://localhost:3000/api/attempts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"exerciseId":1,"userAnswer":"B"}' | jq '.'
echo ""

echo "✅ Tous les tests terminés!"
```

**Sauvegarder dans un fichier** :
```bash
cat > test_all.sh << 'EOF'
[copier le script ci-dessus]
EOF

chmod +x test_all.sh
./test_all.sh
```

---

## 🔍 Vérification en base de données

```sql
-- Se connecter
psql -U postgres -d mathia

-- Vérifier l'utilisateur créé
SELECT id, name, email, LEFT(password_hash, 10) as hash_preview 
FROM users 
WHERE email = 'marie@example.com';

-- Le password_hash doit commencer par $2a$ ou $2b$
-- Exemple: $2a$10$abcd...

-- Vérifier les tentatives
SELECT 
  u.name,
  e.body,
  a."userAnswer",
  a."isCorrect",
  a."createdAt"
FROM attempts a
JOIN users u ON a."userId" = u.id
JOIN exercises e ON a."exerciseId" = e.id
WHERE u.email = 'marie@example.com'
ORDER BY a."createdAt" DESC;
```

---

## 📱 Test avec l'app iOS

### 1. Ouvrir l'app dans Xcode

```bash
cd mobile/MathiaApp
# Ouvrir le fichier .xcodeproj dans Xcode
```

### 2. Configurer l'URL

Dans `Services/APIService.swift` :
```swift
private let baseURL = "http://localhost:3000/api"
```

### 3. Lancer l'app (⌘+R)

### 4. Tester le flux complet

1. **Inscription** : Remplir le formulaire
   - Nom : "Test iOS"
   - Email : "ios@test.com"
   - Password : "test123"
   - Confirmer : "test123"

2. **Connexion automatique** après inscription

3. **Liste des cours** : Doit afficher les 3 cours créés

4. **Ouvrir un cours** : Cliquer sur "Les fractions"

5. **Liste des exercices** : Voir l'exercice créé

6. **Résoudre l'exercice** : 
   - Lire la question
   - Sélectionner "B"
   - Cliquer sur "Valider"

7. **Voir le résultat** :
   - Carte verte avec ✅
   - Explication affichée
   - Message "Bonne réponse !"

---

## 🎉 Validation finale

Si tous ces tests passent, le backend est **totalement fonctionnel** et prêt pour :

✅ **Production** (avec configuration HTTPS)  
✅ **App iOS** (connexion testée et validée)  
✅ **Développement** (environnement complet)  
✅ **Tests automatisés**  
✅ **Génération IA d'exercices**  
✅ **Documentation complète**  

---

## 🚀 Commandes ultra-rapides

```bash
# Test complet en une commande
npm run test:api

# Ou manuellement (après avoir créé un compte)
export TOKEN="votre_token"
curl http://localhost:3000/api/courses -H "Authorization: Bearer $TOKEN"
curl "http://localhost:3000/api/exercises?courseId=1&difficulty=facile" -H "Authorization: Bearer $TOKEN"
curl -X POST http://localhost:3000/api/attempts -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"exerciseId":1,"userAnswer":"B"}'
```

---

🎓 **Le backend Mathia est 100% fonctionnel et prêt pour l'app iOS !**





