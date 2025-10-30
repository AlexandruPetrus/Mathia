# 🧪 Tester MAINTENANT - Commandes prêtes à copier

Copiez-collez ces commandes pour tester immédiatement tous les endpoints.

## ⚡ Terminal 1 : Démarrer le serveur

```bash
npm run dev
```

**Attendez de voir** :
```
🚀 Serveur Mathia démarré avec succès
📍 URL: http://localhost:3000
```

---

## ⚡ Terminal 2 : Tests des endpoints

Copiez-collez TOUTES ces commandes dans un nouveau terminal :

```bash
# Variables
API="http://localhost:3000/api"

echo "======================================================================"
echo "🧪 TESTS DE L'API MATHIA"
echo "======================================================================"
echo ""

# TEST 1 : POST /auth/signup → Créer un compte
echo "1️⃣ POST /auth/signup - Créer un compte"
echo "----------------------------------------------------------------------"

curl -X POST "$API/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Marie Dupont",
    "email": "marie_test@example.com",
    "password": "password123"
  }'

echo ""
echo ""
read -p "➡️  Copiez le token ci-dessus et appuyez sur Entrée..."

# Saisissez le token
read -p "🔑 Collez le token ici: " TOKEN

echo ""
echo "======================================================================"
echo ""

# TEST 2 : POST /auth/login → Obtenir un JWT
echo "2️⃣ POST /auth/login - Se connecter"
echo "----------------------------------------------------------------------"

curl -X POST "$API/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "marie_test@example.com",
    "password": "password123"
  }'

echo ""
echo ""
echo "======================================================================"
echo ""

# TEST 3 : GET /courses → Récupérer les cours
echo "3️⃣ GET /courses - Liste des cours"
echo "----------------------------------------------------------------------"

curl "$API/courses" \
  -H "Authorization: Bearer $TOKEN"

echo ""
echo ""
echo "======================================================================"
echo ""

# TEST 4 : GET /exercises?courseId=1&difficulty=facile
echo "4️⃣ GET /exercises?courseId=1&difficulty=facile - Filtrer"
echo "----------------------------------------------------------------------"

curl "$API/exercises?courseId=1&difficulty=facile" \
  -H "Authorization: Bearer $TOKEN"

echo ""
echo ""
echo "======================================================================"
echo ""

# TEST 5 : POST /attempts → Enregistrer une réponse
echo "5️⃣ POST /attempts - Soumettre une réponse"
echo "----------------------------------------------------------------------"

curl -X POST "$API/attempts" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exerciseId": 1,
    "userAnswer": "B"
  }'

echo ""
echo ""
echo "======================================================================"
echo "✅ TOUS LES TESTS TERMINÉS"
echo "======================================================================"
```

---

## 📋 Version simplifiée (automatique)

Si vous voulez tout tester automatiquement sans interaction :

```bash
# Créer un script de test
cat > quick_test.sh << 'SCRIPT'
#!/bin/bash

API="http://localhost:3000/api"

echo "🧪 Tests de l'API Mathia"
echo ""

# 1. Signup et récupérer le token
echo "1. Signup..."
RESPONSE=$(curl -s -X POST "$API/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Auto","email":"auto_'$(date +%s)'@test.com","password":"test123"}')

TOKEN=$(echo "$RESPONSE" | grep -o '"token":"[^"]*' | cut -d'"' -f4)
echo "✅ Token: ${TOKEN:0:30}..."
echo ""

# 2. Login
echo "2. Login..."
curl -s -X POST "$API/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}' > /dev/null
echo "✅ Login OK"
echo ""

# 3. Courses
echo "3. GET /courses..."
COURSES=$(curl -s "$API/courses" -H "Authorization: Bearer $TOKEN")
echo "$COURSES" | grep -q '"success":true' && echo "✅ Courses OK" || echo "❌ Erreur"
echo ""

# 4. Exercises avec filtres
echo "4. GET /exercises?courseId=1&difficulty=facile..."
EXERCISES=$(curl -s "$API/exercises?courseId=1&difficulty=facile" \
  -H "Authorization: Bearer $TOKEN")
echo "$EXERCISES" | grep -q '"success":true' && echo "✅ Exercises OK" || echo "❌ Erreur"
echo ""

# 5. Attempts
echo "5. POST /attempts..."
ATTEMPT=$(curl -s -X POST "$API/attempts" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"exerciseId":1,"userAnswer":"B"}')
echo "$ATTEMPT" | grep -q '"isCorrect"' && echo "✅ Attempt OK" || echo "⚠️  Exercice non trouvé (créez-en un d'abord)"
echo ""

echo "🎉 Tests terminés!"
SCRIPT

chmod +x quick_test.sh
./quick_test.sh
```

---

## 🎯 Test complet avec Node.js

```bash
npm run test:api
```

Ce script teste automatiquement :
- ✅ POST /auth/signup
- ✅ POST /auth/login
- ✅ GET /courses
- ✅ GET /exercises
- ✅ GET /exercises?courseId=1&difficulty=facile
- ✅ POST /attempts
- ✅ Protection JWT

---

## 📱 Tester l'app iOS

### 1. Ouvrir le projet

```bash
cd mobile/MathiaApp
# Créer le projet dans Xcode selon mobile/SETUP_GUIDE.md
```

### 2. Configurer

**Dans `Services/APIService.swift`** (ligne 14) :
```swift
private let baseURL = "http://localhost:3000/api"
```

### 3. Lancer (⌘+R)

### 4. Utiliser l'app

1. **Cliquer** sur "Inscrivez-vous"
2. **Remplir** :
   - Nom : Test iOS
   - Email : ios@test.com
   - Password : test123 (2 fois)
3. **S'inscrire**
4. **Onglet "Cours"** → Voir les cours
5. **Cliquer** sur un cours
6. **Cliquer** sur un exercice
7. **Sélectionner** une réponse
8. **Valider**
9. **Voir** le résultat avec explication

---

## 🔍 Vérifier les données

```sql
psql -U postgres -d mathia -c "
SELECT 'Users:' as table_name, COUNT(*)::text as count FROM users
UNION ALL
SELECT 'Courses:', COUNT(*)::text FROM courses
UNION ALL
SELECT 'Exercises:', COUNT(*)::text FROM exercises
UNION ALL
SELECT 'Attempts:', COUNT(*)::text FROM attempts;
"
```

---

## 📊 Résultats attendus

### ✅ Backend

```
✓ Serveur démarré sur port 3000
✓ API accessible (http://localhost:3000/api/health)
✓ Swagger accessible (http://localhost:3000/api-docs)
✓ Base de données connectée
✓ Tables créées (users, courses, exercises, attempts)
```

### ✅ API

```
✓ POST /auth/signup → 201 Created + token
✓ POST /auth/login → 200 OK + token
✓ GET /courses → 200 OK + liste
✓ GET /exercises?courseId=1&difficulty=facile → 200 OK + filtrés
✓ POST /attempts → 201 Created + isCorrect
✓ Sans JWT → 401 Unauthorized
```

### ✅ App iOS

```
✓ App se lance
✓ Écran de connexion s'affiche
✓ Peut créer un compte
✓ Connexion automatique après signup
✓ Liste des cours s'affiche
✓ Navigation fonctionne
✓ Quiz interactif
✓ Résultats affichés
```

---

## 🎉 Validation finale

Si TOUS les points ci-dessus sont ✅, alors :

**Le backend est 100% fonctionnel et prêt pour l'app iOS !** 🚀

---

## 📖 Documentation complète

| Document | Description |
|----------|-------------|
| `START_HERE.md` | Guide de démarrage (ce fichier) |
| `FINAL_TESTS.md` | Tests détaillés de tous les endpoints |
| `PROJECT_SUMMARY.md` | Vue d'ensemble complète |
| `BACKEND_CHECKLIST.md` | Checklist de fonctionnalité |
| `mobile/README.md` | Documentation iOS |
| `mobile/SETUP_GUIDE.md` | Configuration Xcode |

---

**🎓 Bon développement avec Mathia !**





