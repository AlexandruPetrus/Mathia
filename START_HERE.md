# 🚀 Démarrage rapide - Mathia

Guide ultra-rapide pour lancer le projet complet en 5 minutes.

## ⚡ Installation express (5 minutes)

### 1️⃣ Configuration (1 minute)

```bash
# Installer les dépendances
npm install

# Créer le fichier .env
cat > .env << 'EOF'
PORT=3000
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mathia
JWT_SECRET=super_secret_jwt_key_change_in_production
OPENAI_API_KEY=sk-xxxxxx
EOF
```

### 2️⃣ Base de données (1 minute)

```bash
# Créer la base de données
createdb mathia

# Ou depuis psql :
psql -U postgres -c "CREATE DATABASE mathia;"

# Synchroniser les modèles (créer les tables)
npm run db:sync
```

### 3️⃣ Données de test (1 minute)

```bash
# Se connecter à la base
psql -U postgres -d mathia

# Créer quelques cours
INSERT INTO courses (title, grade, chapter, description, "createdAt", "updatedAt")
VALUES 
  ('Les fractions', '6ème', 'Arithmétique', 'Apprendre les fractions simples', NOW(), NOW()),
  ('Géométrie de base', '6ème', 'Géométrie', 'Les formes géométriques', NOW(), NOW()),
  ('Les équations', '3ème', 'Algèbre', 'Résoudre des équations du premier degré', NOW(), NOW());

-- Quitter psql
\q
```

### 4️⃣ Démarrer le backend (10 secondes)

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

✅ **Backend fonctionnel !**

### 5️⃣ Tester l'API (1 minute)

```bash
# Dans un nouveau terminal

# 1. Créer un compte
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "test123"
  }'

# 2. Copier le token de la réponse et l'exporter
export TOKEN="votre_token_ici"

# 3. Récupérer les cours
curl http://localhost:3000/api/courses \
  -H "Authorization: Bearer $TOKEN"

# 4. Créer un exercice
curl -X POST http://localhost:3000/api/admin/exercises \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "courseId": 1,
    "type": "qcm",
    "body": "Quelle est la moitié de 10?",
    "options": {"A": "3", "B": "5", "C": "7", "D": "10"},
    "answer": "B",
    "explanation": "10 divisé par 2 égale 5",
    "difficulty": "facile",
    "tags": ["fractions", "division"]
  }'

# 5. Lister les exercices
curl "http://localhost:3000/api/exercises?courseId=1&difficulty=facile" \
  -H "Authorization: Bearer $TOKEN"

# 6. Répondre à l'exercice
curl -X POST http://localhost:3000/api/attempts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exerciseId": 1,
    "userAnswer": "B"
  }'
```

✅ **API testée et fonctionnelle !**

### 6️⃣ Lancer l'app iOS (2 minutes)

**Option A : Créer le projet Xcode**

1. Ouvrir Xcode
2. File → New → Project
3. iOS → App
4. Product Name: **MathiaApp**
5. Interface: **SwiftUI**, Language: **Swift**
6. Sauvegarder dans le dossier `mobile/`
7. Glisser tous les fichiers `.swift` dans Xcode
8. Ajouter `Info.plist` au projet
9. Run (⌘+R)

**Option B : Utiliser le projet existant**

Si vous avez déjà un `.xcodeproj` :
```bash
cd mobile/MathiaApp
open MathiaApp.xcodeproj
```

**Configurer l'URL** dans `APIService.swift` :
```swift
private let baseURL = "http://localhost:3000/api"
```

**Lancer** : Cliquer sur Play (▶️) ou ⌘+R

✅ **App iOS lancée !**

---

## 🎉 C'est prêt !

Vous avez maintenant :

✅ **Backend API** tournant sur `http://localhost:3000`  
✅ **Base de données** PostgreSQL avec tables et données  
✅ **Documentation** accessible sur `http://localhost:3000/api-docs`  
✅ **App iOS** dans le Simulator (si Xcode configuré)  

## 📚 Que faire ensuite ?

### Utiliser l'app iOS

1. **S'inscrire** dans l'app
2. **Explorer les cours**
3. **Résoudre des exercices**
4. **Voir les explications**

### Générer plus d'exercices avec l'IA

```bash
# Configurer votre clé OpenAI dans .env
OPENAI_API_KEY=sk-proj-xxxxxxxx

# Générer 10 exercices
python scripts/ai_generate_exercises.py \
  --chapter "Les fractions" \
  --grade "6ème" \
  --difficulty "facile" \
  --type "qcm" \
  --count 10

# Importer en base
python scripts/import_exercises.py \
  --file backend/data/generated_exercises.json \
  --course-id 1
```

### Explorer la documentation

- **API Swagger** : http://localhost:3000/api-docs
- **README** : Documentation complète
- **ROUTES.md** : Tous les endpoints
- **mobile/README.md** : Documentation iOS

## 🐛 Problèmes ?

### Backend ne démarre pas

```bash
# Vérifier PostgreSQL
pg_ctl status

# Vérifier le .env
cat .env

# Réinstaller les dépendances
rm -rf node_modules
npm install
```

### App iOS ne se connecte pas

1. Vérifier que le backend tourne
2. Tester manuellement : `curl http://localhost:3000/api/health`
3. Vérifier l'URL dans `APIService.swift`
4. Vérifier `Info.plist` (permissions HTTP)

### Bases de données vide

```sql
-- Se connecter
psql -U postgres -d mathia

-- Voir les tables
\dt

-- Ajouter des cours
INSERT INTO courses (title, grade, chapter, description, "createdAt", "updatedAt")
VALUES ('Test', '6ème', 'Test', 'Test', NOW(), NOW());
```

---

## 📖 Documentation détaillée

| Fichier | Description |
|---------|-------------|
| `README.md` | Documentation principale backend |
| `QUICK_START.md` | Guide de démarrage backend |
| `PROJECT_SUMMARY.md` | Vue d'ensemble complète du projet |
| `BACKEND_CHECKLIST.md` | Vérification fonctionnalité backend |
| `mobile/README.md` | Documentation iOS |
| `mobile/SETUP_GUIDE.md` | Configuration Xcode |

---

🎓 **Bon développement avec Mathia !**





