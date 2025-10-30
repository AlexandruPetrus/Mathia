# 🎉 Installation complète - Guide en 3 étapes

Guide ultra-rapide pour avoir Mathia (Backend + iOS) opérationnel en moins de 10 minutes.

## 📦 Ce qui a été créé

✅ **Backend complet** (Node.js + Express + PostgreSQL)  
✅ **App iOS** (SwiftUI native)  
✅ **Documentation complète** (15+ guides)  
✅ **Tests automatisés**  
✅ **Scripts de génération IA**  

---

## 🚀 ÉTAPE 1 : Backend (5 minutes)

### A. Installation

```bash
# 1. Installer les dépendances
npm install

# 2. Créer le fichier .env
cat > .env << 'EOF'
PORT=3000
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mathia
JWT_SECRET=super_secret_jwt_key_change_in_production
OPENAI_API_KEY=sk-xxxxxx
EOF

# 3. Créer la base de données
createdb mathia

# 4. Créer les tables
npm run db:sync
```

### B. Démarrer

```bash
npm run dev
```

**✅ Attendez de voir :**
```
✅ Connexion à PostgreSQL établie avec succès
✅ Modèles synchronisés avec la base de données
🚀 Serveur Mathia démarré avec succès
📍 URL: http://localhost:3000
```

### C. Créer des données de test

```bash
# Dans un nouveau terminal
psql -U postgres -d mathia << 'EOF'
INSERT INTO courses (title, grade, chapter, description, "createdAt", "updatedAt")
VALUES 
  ('Les fractions', '6ème', 'Arithmétique', 'Apprendre les fractions simples', NOW(), NOW()),
  ('Géométrie', '6ème', 'Géométrie', 'Les formes géométriques', NOW(), NOW());
EOF
```

### D. Tester l'API

```bash
# Créer un compte
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","password":"test123"}'

# Copier le token de la réponse
export TOKEN="votre_token_ici"

# Créer un exercice
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

# Lister les exercices
curl "http://localhost:3000/api/exercises?courseId=1&difficulty=facile" \
  -H "Authorization: Bearer $TOKEN"
```

**✅ Backend fonctionnel !**

---

## 📱 ÉTAPE 2 : App iOS (5 minutes)

### A. Créer le projet Xcode

1. **Ouvrir Xcode**

2. **File → New → Project**
   - Platform: **iOS**
   - Template: **App**
   - Product Name: **MathiaApp**
   - Interface: **SwiftUI**
   - Language: **Swift**
   - Sauvegarder dans : `mobile/`

3. **Organiser les fichiers** :
   - Créer les dossiers : Models, Services, Views
   - Dans Views : Auth, Courses, Exercises, Profile
   - Glisser tous les fichiers `.swift` dans leurs dossiers

4. **Ajouter Info.plist** au projet

### B. Configuration

**Éditer `Services/APIService.swift`** :

```swift
// Ligne 14 - Choisir selon votre situation

// Simulator iOS
private let baseURL = "http://localhost:3000/api"

// iPhone physique (remplacer X.X.X.X par l'IP de votre Mac)
// private let baseURL = "http://192.168.1.X:3000/api"
```

**Trouver l'IP de votre Mac** :
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

### C. Lancer

1. **Sélectionner simulator** : iPhone 14 Pro
2. **Run** : Cliquer sur Play (▶️) ou ⌘+R
3. **Attendre** le build (30-60 secondes)

**✅ App lancée !**

### D. Tester

1. **S'inscrire** :
   - Cliquer sur "Inscrivez-vous"
   - Nom : "Test iOS"
   - Email : "ios@test.com"
   - Password : "test123"
   - Confirmer : "test123"
   - "S'inscrire"

2. **Voir les cours** : Onglet "Cours"

3. **Ouvrir un cours** : Cliquer sur "Les fractions"

4. **Résoudre** :
   - Cliquer sur l'exercice
   - Sélectionner "B"
   - "Valider"
   - Voir le résultat ✅ avec explication

**✅ App iOS fonctionnelle !**

---

## 📊 ÉTAPE 3 : Vérification complète

### Backend

```bash
# API accessible
curl http://localhost:3000/api/health

# Documentation Swagger
open http://localhost:3000/api-docs
```

### Base de données

```sql
psql -U postgres -d mathia -c "
SELECT 
  (SELECT COUNT(*) FROM users) as users,
  (SELECT COUNT(*) FROM courses) as courses,
  (SELECT COUNT(*) FROM exercises) as exercises,
  (SELECT COUNT(*) FROM attempts) as attempts;
"
```

### App iOS

- [ ] App se lance sans erreur
- [ ] Peut créer un compte
- [ ] Peut se connecter
- [ ] Liste des cours s'affiche
- [ ] Peut ouvrir un cours
- [ ] Peut répondre à un exercice
- [ ] Le résultat s'affiche

---

## ✅ C'est terminé !

Vous avez maintenant :

🖥️ **Backend API REST**
- 7 endpoints fonctionnels
- Authentification JWT sécurisée
- Base de données PostgreSQL
- Documentation Swagger

📱 **App iOS SwiftUI**
- Interface moderne et intuitive
- Connexion au backend
- QCM interactifs
- Feedback en temps réel

🤖 **Génération IA**
- Scripts Python pour OpenAI
- Import automatique en DB

📚 **Documentation complète**
- 15+ guides et tutoriels
- Exemples pour chaque endpoint
- Tests automatisés

---

## 📚 Prochaines étapes

### Explorer la documentation

```bash
# Ouvrir dans votre éditeur préféré
code .

# Fichiers importants :
# - PROJECT_SUMMARY.md (vue d'ensemble complète)
# - FINAL_TESTS.md (tests de tous les endpoints)
# - mobile/README.md (documentation iOS)
# - docs/openapi.yaml (spécification API)
```

### Générer des exercices avec l'IA

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

### Déployer en production

1. **Backend** : Heroku, Render, Railway, DigitalOcean
2. **iOS** : TestFlight → App Store
3. **Voir** : Documentation pour chaque plateforme

---

## 🐛 Problèmes ?

### Backend ne démarre pas

```bash
# Vérifier PostgreSQL
pg_ctl status

# Réinstaller
rm -rf node_modules
npm install
```

### App iOS ne se connecte pas

1. Backend tourne ? → `curl http://localhost:3000/api/health`
2. URL correcte dans `APIService.swift` ?
3. Info.plist configure les permissions HTTP ?

### Besoin d'aide ?

Consultez :
- `FINAL_TESTS.md` - Tests détaillés
- `TESTING_GUIDE.md` - Guide de dépannage
- `mobile/SETUP_GUIDE.md` - Configuration iOS

---

## 🎊 Félicitations !

Vous avez créé une application complète de révision de mathématiques avec :

✅ Backend sécurisé et scalable  
✅ App iOS native et moderne  
✅ IA pour générer du contenu  
✅ Documentation professionnelle  

**🚀 Happy coding avec Mathia !**





