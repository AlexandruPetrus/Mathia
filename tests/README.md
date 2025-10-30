# 🧪 Tests de l'API Mathia

Scripts automatisés pour tester tous les endpoints de l'API.

## 📋 Prérequis

1. **Serveur démarré** :
   ```bash
   npm run dev
   ```

2. **Base de données** PostgreSQL configurée et connectée

## 🚀 Lancer les tests

### Option 1 : Script Bash (recommandé pour Linux/Mac)

```bash
bash tests/test_api.sh
```

**Prérequis** : `jq` pour le formatage JSON (optionnel)
```bash
# Mac
brew install jq

# Linux
sudo apt-get install jq
```

### Option 2 : Script Node.js (multi-plateforme)

```bash
node tests/test_api.js
```

Fonctionne sur Windows, Mac et Linux sans dépendances supplémentaires.

## 📊 Tests effectués

Les scripts testent dans l'ordre :

### ✅ Test 1 : POST /auth/signup
- Créer un nouveau compte utilisateur
- Vérifier que le token JWT est retourné
- Vérifier que le password est hashé (pas visible dans la réponse)

### ✅ Test 2 : POST /auth/login
- Se connecter avec les credentials
- Vérifier l'obtention d'un nouveau JWT
- Vérifier que les infos utilisateur sont retournées

### ✅ Test 3 : GET /courses
- Récupérer tous les cours
- Vérifier l'authentification JWT
- Compter le nombre de cours disponibles

### ✅ Test 4 : GET /exercises
- Lister tous les exercices
- Vérifier l'inclusion des infos du cours
- Récupérer le premier exercice ID pour les tests suivants

### ✅ Test 5 : GET /exercises?courseId=1&difficulty=facile
- Tester le filtrage par cours
- Tester le filtrage par difficulté
- Vérifier que les deux filtres peuvent être combinés

### ✅ Test 6 : POST /attempts
- Soumettre une réponse à un exercice
- Vérifier l'enregistrement dans la base de données
- Vérifier le retour de `isCorrect`

### ✅ Test 7 : Test sans authentification
- Tester une route protégée sans token
- Vérifier que l'API retourne 401 Unauthorized
- Confirmer que la protection JWT fonctionne

## 📝 Exemple de sortie

```
======================================================================
🧪 TEST DE L'API MATHIA
======================================================================

📍 URL de base: http://localhost:3000/api
📧 Email de test: test_1705330000@example.com

======================================================================
TEST 1: POST /auth/signup - Créer un compte
======================================================================

📤 Requête:
POST http://localhost:3000/api/auth/signup
Body: { name: "Test User", email: "test_1705330000@example.com", password: "***" }

📥 Réponse (HTTP 201):
{
  "success": true,
  "message": "Inscription réussie",
  "data": {
    "user": {
      "id": 5,
      "name": "Test User",
      "email": "test_1705330000@example.com",
      "createdAt": "2025-01-15T14:30:00.000Z",
      "updatedAt": "2025-01-15T14:30:00.000Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}

✅ Inscription réussie
🔑 Token récupéré (152 caractères)
👤 User ID: 5

[...]

======================================================================
📊 RÉSUMÉ DES TESTS
======================================================================

✅ Tests terminés

🔑 Token JWT généré: eyJhbGciOiJIUzI1NiIsInR5cCI...
👤 User ID: 5
📧 Email: test_1705330000@example.com

💡 Vous pouvez maintenant utiliser ce token pour tester d'autres endpoints:
   export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   curl -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/courses

======================================================================
```

## 🎯 Tests manuels avec curl

Si vous préférez tester manuellement :

### 1. Créer un compte

```bash
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "test123"
  }'
```

### 2. Se connecter

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

### 3. Exporter le token

```bash
export TOKEN="votre_token_ici"
```

### 4. Récupérer les cours

```bash
curl http://localhost:3000/api/courses \
  -H "Authorization: Bearer $TOKEN"
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

## 🔍 Vérifier les données en base

```sql
-- Voir les utilisateurs de test
SELECT id, name, email, "createdAt" FROM users WHERE email LIKE 'test%';

-- Voir les tentatives enregistrées
SELECT u.name, e.body, a."userAnswer", a."isCorrect", a."createdAt"
FROM attempts a
JOIN users u ON a."userId" = u.id
JOIN exercises e ON a."exerciseId" = e.id
ORDER BY a."createdAt" DESC
LIMIT 10;

-- Nettoyer les utilisateurs de test
DELETE FROM users WHERE email LIKE 'test%';
```

## 🐛 Dépannage

### Erreur "Connection refused"

Le serveur n'est pas démarré :
```bash
npm run dev
```

### Erreur 404 sur /attempts

Aucun exercice en base de données. Créez-en un :
```bash
curl -X POST http://localhost:3000/api/admin/exercises \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "courseId": 1,
    "type": "qcm",
    "body": "Test question",
    "answer": "A"
  }'
```

### Erreur "jq: command not found" (script bash)

Installez `jq` ou utilisez le script Node.js à la place.

## 📝 Scripts npm

Ajoutez dans `package.json` :

```json
"scripts": {
  "test:api": "node tests/test_api.js",
  "test:api:bash": "bash tests/test_api.sh"
}
```

Puis lancez :
```bash
npm run test:api
```

---

✅ **Tous les endpoints sont testés automatiquement !**









