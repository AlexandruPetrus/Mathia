# 🚀 Guide de démarrage rapide - Mathia Backend

## 📋 Modèles Sequelize

### 🧱 User
```javascript
{
  id: INTEGER (auto-increment),
  name: STRING,
  email: STRING (unique),
  password_hash: STRING (auto-hashed)
}
```

### 📘 Course
```javascript
{
  id: INTEGER (auto-increment),
  title: STRING,
  grade: STRING,  // "6ème", "5ème", "4ème", "3ème"
  chapter: STRING,
  description: TEXT
}
```

### 🧮 Exercise
```javascript
{
  id: INTEGER (auto-increment),
  courseId: INTEGER (FK → courses),
  type: STRING,  // "qcm", "libre", "vrai-faux", "calcul"
  body: TEXT,
  options: JSON,  // Pour les QCM: { "A": "...", "B": "..." }
  answer: TEXT,
  explanation: TEXT,
  difficulty: STRING,  // "facile", "moyen", "difficile"
  tags: JSON  // ["algèbre", "équations"]
}
```

### 🧾 Attempt
```javascript
{
  id: INTEGER (auto-increment),
  userId: INTEGER (FK → users),
  exerciseId: INTEGER (FK → exercises),
  userAnswer: TEXT,
  isCorrect: BOOLEAN,
  createdAt: DATE
}
```

## ⚡ Installation rapide

```bash
# 1. Installer les dépendances
npm install

# 2. Configurer l'environnement
cp .env.template .env
# Éditer .env avec vos paramètres PostgreSQL

# 3. Créer la base de données
createdb mathia_db
# ou depuis psql: CREATE DATABASE mathia_db;

# 4. Synchroniser les modèles (créer les tables)
npm run db:sync

# 5. Démarrer le serveur
npm run dev
```

## 🎯 Endpoints principaux

### Authentification
- `POST /api/auth/register` - Inscription (name, email, password)
- `POST /api/auth/login` - Connexion (email, password)
- `GET /api/auth/profile` - Profil (nécessite token JWT)

### Cours
- `GET /api/courses` - Liste des cours (filtres: grade, chapter, search)
- `GET /api/courses/:id` - Détails d'un cours avec ses exercices
- `POST /api/courses` - Créer un cours (title, grade, chapter, description)
- `PUT /api/courses/:id` - Modifier un cours
- `DELETE /api/courses/:id` - Supprimer un cours (admin)

### Exercices
- `GET /api/exercises` - Liste des exercices (filtres: courseId, type, difficulty)
- `GET /api/exercises/:id` - Détails d'un exercice
- `POST /api/exercises` - Créer un exercice (courseId, type, body, answer, ...)
- `PUT /api/exercises/:id` - Modifier un exercice
- `DELETE /api/exercises/:id` - Supprimer un exercice (admin)

### Tentatives
- `POST /api/attempts` - Soumettre une réponse (exerciseId, userAnswer)
- `GET /api/attempts/me` - Mes tentatives
- `GET /api/attempts/me/stats` - Mes statistiques

### Admin
- `GET /api/admin/dashboard` - Statistiques globales
- `GET /api/admin/users` - Liste des utilisateurs
- `DELETE /api/admin/users/:userId` - Supprimer un utilisateur

## 📝 Exemple d'utilisation

### 1. Inscription
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Marie Dupont",
    "email": "marie@example.com",
    "password": "password123"
  }'
```

### 2. Créer un cours
```bash
curl -X POST http://localhost:3000/api/courses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Les fractions",
    "grade": "6ème",
    "chapter": "Arithmétique",
    "description": "Apprendre les fractions simples"
  }'
```

### 3. Créer un exercice
```bash
curl -X POST http://localhost:3000/api/exercises \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
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
```

### 4. Soumettre une réponse
```bash
curl -X POST http://localhost:3000/api/attempts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "exerciseId": 1,
    "userAnswer": "B"
  }'
```

## 🔑 Variables d'environnement importantes

```env
# Base de données
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mathia_db
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe

# JWT
JWT_SECRET=votre_secret_jwt_très_long_et_sécurisé
JWT_EXPIRES_IN=7d

# Serveur
PORT=3000
NODE_ENV=development
```

## 📚 Documentation complète

- **API Documentation**: http://localhost:3000/api-docs (Swagger UI)
- **Health Check**: http://localhost:3000/api/health
- **README complet**: Voir `README.md`

## 🔗 Relations Sequelize

Les relations sont automatiquement configurées :

```javascript
// Un cours a plusieurs exercices
Course.hasMany(Exercise, { foreignKey: 'courseId', as: 'exercises' })

// Un utilisateur a plusieurs tentatives
User.hasMany(Attempt, { foreignKey: 'userId', as: 'attempts' })

// Un exercice a plusieurs tentatives
Exercise.hasMany(Attempt, { foreignKey: 'exerciseId', as: 'attempts' })
```

Vous pouvez faire des requêtes avec includes :
```javascript
const course = await Course.findByPk(1, {
  include: [{ model: Exercise, as: 'exercises' }]
});
```

## ⚠️ Notes importantes

1. Le mot de passe est automatiquement hashé avec bcrypt lors de la création/mise à jour
2. Les tokens JWT sont envoyés dans le header: `Authorization: Bearer {token}`
3. Les IDs sont des INTEGER avec auto-increment (pas des UUID)
4. Le champ `createdAt` dans Attempt est géré automatiquement
5. La réponse d'un exercice n'est visible qu'après l'avoir résolu correctement

## 🐛 Debugging

```bash
# Voir les logs SQL
NODE_ENV=development npm run dev

# Resynchroniser la base de données (ATTENTION: supprime les données)
# Modifier src/config/syncDb.js pour utiliser { force: true } si nécessaire
npm run db:sync
```

## 🎓 Prêt pour SwiftUI

Ce backend est conçu pour être facilement intégré à une app iOS SwiftUI. 
Les réponses sont toujours au format JSON avec une structure cohérente :

```json
{
  "success": true,
  "data": { ... },
  "message": "..." (optionnel)
}
```

Bon développement ! 🚀









