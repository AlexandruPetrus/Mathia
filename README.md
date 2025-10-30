# 🎓 Mathia Backend

Backend API REST pour **Mathia** - Application de révision de mathématiques pour collégiens (6ème à 3ème).

## 📋 Table des matières

- [Technologies](#-technologies)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Démarrage](#-démarrage)
- [Structure du projet](#-structure-du-projet)
- [API Documentation](#-api-documentation)
- [Génération d'exercices avec IA](#-génération-dexercices-avec-ia)
- [Scripts disponibles](#-scripts-disponibles)

## 🛠 Technologies

- **Node.js** 18+
- **Express.js** - Framework web
- **PostgreSQL** - Base de données
- **Sequelize** - ORM
- **JWT** - Authentification
- **OpenAI API** - Génération d'exercices
- **Swagger** - Documentation API

## ✨ Fonctionnalités

- 🔐 **Authentification JWT** - Inscription, connexion, gestion de profil
- 📚 **Gestion des cours** - CRUD complet avec filtres par niveau et thème
- 📝 **Exercices** - Création, modification, suppression d'exercices
- 🎯 **Tentatives** - Suivi des réponses des élèves et statistiques
- 🤖 **Génération IA** - Création automatique d'exercices avec OpenAI
- 👑 **Administration** - Gestion des utilisateurs et tableau de bord
- 📊 **Statistiques** - Taux de réussite, points, progression
- 🔒 **Sécurité** - Helmet, CORS, Rate limiting

## 📦 Installation

### Prérequis

- Node.js 18 ou supérieur
- PostgreSQL 13 ou supérieur
- npm ou yarn
- Python 3.8+ (pour le script de génération IA)

### Étapes

1. **Cloner le projet**
```bash
cd mathia-backend
```

2. **Installer les dépendances Node.js**
```bash
npm install
```

3. **Installer les dépendances Python** (pour la génération d'exercices)
```bash
pip install openai psycopg2-binary python-dotenv
```

## ⚙️ Configuration

1. **Créer le fichier `.env`** à la racine du projet

```bash
# Créer le fichier .env
cat > .env << 'EOF'
PORT=3000
DATABASE_URL=postgresql://user:password@localhost:5432/mathia
JWT_SECRET=super_secret_jwt_key
OPENAI_API_KEY=sk-xxxxxx
EOF
```

2. **Éditer `.env` avec vos vraies valeurs**

```env
PORT=3000
DATABASE_URL=postgresql://postgres:votre_password@localhost:5432/mathia
JWT_SECRET=super_secret_jwt_key
OPENAI_API_KEY=sk-xxxxxx
```

📖 **Documentation complète** : Consultez `ENV_SETUP.md` pour plus de détails

3. **Créer la base de données PostgreSQL**
```bash
# Se connecter à PostgreSQL
psql -U postgres

# Créer la base de données
CREATE DATABASE mathia_db;

# Quitter psql
\q
```

4. **Synchroniser les modèles avec la base de données**
```bash
npm run db:sync
```

## 🚀 Démarrage

### Mode développement (avec rechargement automatique)
```bash
npm run dev
```

### Mode production
```bash
npm start
```

Le serveur démarre sur `http://localhost:3000`

## 📁 Structure du projet

```
mathia-backend/
├── docs/
│   └── openapi.yaml           # Documentation Swagger
├── scripts/
│   └── ai_generate_exercises.py  # Génération d'exercices IA
├── src/
│   ├── config/
│   │   ├── database.js        # Configuration PostgreSQL
│   │   ├── ai.js              # Configuration OpenAI
│   │   └── syncDb.js          # Script de synchronisation
│   ├── controllers/
│   │   ├── authController.js   # Authentification
│   │   ├── courseController.js # Cours
│   │   ├── exerciseController.js # Exercices
│   │   ├── attemptController.js  # Tentatives
│   │   └── adminController.js    # Administration
│   ├── middleware/
│   │   ├── auth.js            # JWT & Authorization
│   │   ├── validation.js      # Validation Joi
│   │   └── errorHandler.js    # Gestion d'erreurs
│   ├── models/
│   │   ├── User.js            # Modèle Utilisateur
│   │   ├── Course.js          # Modèle Cours
│   │   ├── Exercise.js        # Modèle Exercice
│   │   ├── Attempt.js         # Modèle Tentative
│   │   └── index.js           # Relations
│   └── routes/
│       ├── auth.js            # Routes auth
│       ├── courses.js         # Routes cours
│       ├── exercises.js       # Routes exercices
│       ├── attempts.js        # Routes tentatives
│       ├── admin.js           # Routes admin
│       └── index.js           # Router principal
├── .env.template              # Template config
├── package.json
├── server.js                  # Point d'entrée
└── README.md
```

## 📚 API Documentation

Une fois le serveur démarré, accédez à la documentation interactive Swagger :

**http://localhost:3000/api-docs**

### Endpoints principaux

#### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `GET /api/auth/profile` - Profil utilisateur
- `PUT /api/auth/profile` - Mise à jour du profil

#### Cours
- `GET /api/courses` - Liste des cours (avec filtres)
- `GET /api/courses/:id` - Détails d'un cours
- `POST /api/courses` - Créer un cours (teacher/admin)
- `PUT /api/courses/:id` - Modifier un cours (teacher/admin)
- `DELETE /api/courses/:id` - Supprimer un cours (admin)

#### Exercices
- `GET /api/exercises` - Liste des exercices
- `GET /api/exercises/:id` - Détails d'un exercice
- `POST /api/exercises` - Créer un exercice (teacher/admin)
- `PUT /api/exercises/:id` - Modifier un exercice (teacher/admin)
- `DELETE /api/exercises/:id` - Supprimer un exercice (admin)

#### Tentatives
- `POST /api/attempts` - Soumettre une réponse
- `GET /api/attempts/me` - Mes tentatives
- `GET /api/attempts/me/stats` - Mes statistiques

#### Administration
- `GET /api/admin/dashboard` - Tableau de bord
- `GET /api/admin/users` - Liste des utilisateurs
- `PATCH /api/admin/users/:id/status` - Activer/désactiver
- `PATCH /api/admin/users/:id/role` - Changer le rôle

## 🤖 Génération d'exercices avec IA

Le projet inclut un script Python pour générer automatiquement des exercices avec l'API OpenAI.

### Utilisation

```bash
# Générer 5 exercices de géométrie pour la 6ème (difficulté moyenne)
python scripts/ai_generate_exercises.py --grade "6ème" --topic "Géométrie" --count 5

# Générer 3 exercices d'algèbre difficiles pour la 3ème
python scripts/ai_generate_exercises.py --grade "3ème" --topic "Algèbre" --difficulty "difficile" --count 3
```

### Paramètres disponibles

- `--grade` : Niveau (6ème, 5ème, 4ème, 3ème) - **Obligatoire**
- `--topic` : Thème (Arithmétique, Algèbre, Géométrie, etc.) - **Obligatoire**
- `--difficulty` : Difficulté (facile, moyen, difficile) - Par défaut: moyen
- `--count` : Nombre d'exercices à générer - Par défaut: 1

### Thèmes disponibles

- Arithmétique
- Algèbre
- Géométrie
- Fractions
- Équations
- Proportionnalité
- Probabilités
- Statistiques
- Fonctions
- Théorème de Pythagore

## 📜 Scripts disponibles

```bash
# Démarrer le serveur
npm start

# Mode développement (auto-reload)
npm run dev

# Synchroniser la base de données
npm run db:sync

# Générer des exercices avec IA
npm run generate:exercises
# ou directement:
python scripts/ai_generate_exercises.py --grade "6ème" --topic "Arithmétique" --count 5
```

## 🔒 Sécurité

- **Helmet** - Protection des headers HTTP
- **CORS** - Contrôle d'accès inter-origines
- **Rate Limiting** - Limitation des requêtes (100 req/15min par défaut)
- **JWT** - Tokens sécurisés avec expiration
- **Bcrypt** - Hashage des mots de passe
- **Validation** - Validation des données avec Joi

## 📊 Modèles de données

### User (Utilisateur)
- id (UUID)
- username, email, password
- firstName, lastName
- grade (6ème, 5ème, 4ème, 3ème)
- role (student, teacher, admin)
- totalPoints
- isActive

### Course (Cours)
- id (UUID)
- title, description, content
- grade, topic
- difficulty (facile, moyen, difficile)
- duration, order
- isPublished

### Exercise (Exercice)
- id (UUID)
- courseId (FK)
- title, description, question
- answer, explanation
- difficulty, points
- type (qcm, libre, vrai-faux, calcul)
- hints (array)
- aiGenerated

### Attempt (Tentative)
- id (UUID)
- userId (FK), exerciseId (FK)
- userAnswer
- isCorrect, pointsEarned
- timeSpent, hintsUsed
- attemptNumber, feedback

## 🚦 Codes de statut HTTP

- `200` - Succès
- `201` - Créé
- `400` - Requête invalide
- `401` - Non authentifié
- `403` - Accès interdit
- `404` - Non trouvé
- `409` - Conflit (ressource existe déjà)
- `429` - Trop de requêtes
- `500` - Erreur serveur

## 🔗 Connexion avec SwiftUI

Ce backend est conçu pour être facilement intégré avec une application SwiftUI iOS.

Exemple de requête depuis Swift:
```swift
let url = URL(string: "http://localhost:3000/api/auth/login")!
var request = URLRequest(url: url)
request.httpMethod = "POST"
request.setValue("application/json", forHTTPHeaderField: "Content-Type")

let body = ["email": "user@example.com", "password": "password123"]
request.httpBody = try? JSONEncoder().encode(body)

let task = URLSession.shared.dataTask(with: request) { data, response, error in
    // Traiter la réponse
}
task.resume()
```

## 📝 Licence

MIT

## 🤝 Support

Pour toute question ou problème, ouvrez une issue sur GitHub.

---

Créé avec ❤️ pour les collégiens français

