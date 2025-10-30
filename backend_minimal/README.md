# 🎓 Mathia Backend Minimal - Génération IA

## 📋 Vue d'ensemble

Backend **ultra-minimal** pour Mathia qui ne gère **que la génération d'exercices par IA**.

Toutes les opérations CRUD (auth, courses, exercises, attempts) sont gérées **directement par Supabase** depuis l'application Flutter.

---

## 🎯 Fonctionnalités

Ce backend offre **uniquement** :

- ✅ **Génération d'exercices** avec OpenAI GPT-4
- ✅ **Génération de contenu de cours** avec OpenAI
- ✅ **Amélioration d'exercices existants**
- ✅ **Feedback personnalisé** pour les élèves

**Ce que ce backend ne fait PAS** :
- ❌ Authentification (géré par Supabase Auth)
- ❌ CRUD des cours (géré par Supabase)
- ❌ CRUD des exercices (géré par Supabase)
- ❌ Gestion des tentatives (géré par Supabase)
- ❌ Statistiques (gérées par Supabase Functions)

---

## 📦 Installation

### Prérequis

- Node.js 18+
- Compte Supabase configuré
- Clé API OpenAI

### Étapes

```bash
# Installer les dépendances
npm install

# Copier et configurer .env
cp .env.example .env
# Éditer .env avec vos clés

# Démarrer le serveur
npm start

# Ou en mode dev avec auto-reload
npm run dev
```

---

## ⚙️ Configuration

Dans `.env` :

```env
PORT=3000
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_SERVICE_KEY=your_service_role_key
OPENAI_API_KEY=sk-xxxxxx
```

⚠️ **Important** : Utilisez la clé `service_role` de Supabase (pas `anon`) car le backend doit contourner RLS pour créer des exercices.

---

## 🔌 API Endpoints

### 1. Générer des exercices

**POST** `/api/ai/generate-exercises`

```json
{
  "courseId": "uuid-du-cours",
  "grade": "6ème",
  "topic": "Fractions",
  "difficulty": "moyen",
  "type": "qcm",
  "count": 5
}
```

**Réponse** :

```json
{
  "success": true,
  "message": "5 exercice(s) généré(s) avec succès",
  "count": 5,
  "exercises": [...],
  "usage": {
    "tokens": 1234,
    "cost": "0.0370"
  }
}
```

---

### 2. Générer du contenu de cours

**POST** `/api/ai/generate-course-content`

```json
{
  "title": "Les fractions",
  "grade": "6ème",
  "topic": "Arithmétique",
  "difficulty": "facile",
  "duration": 30
}
```

**Réponse** :

```json
{
  "success": true,
  "course": {
    "title": "...",
    "description": "...",
    "content": "...",
    "prerequisites": [...],
    "learning_objectives": [...],
    "key_concepts": [...]
  }
}
```

---

### 3. Améliorer un exercice

**POST** `/api/ai/improve-exercise`

```json
{
  "exerciseId": "uuid-de-l-exercice"
}
```

**Réponse** :

```json
{
  "success": true,
  "original": {...},
  "improved": {
    "improved_question": "...",
    "improved_explanation": "...",
    "improved_hints": [...],
    "suggestions": [...]
  }
}
```

---

### 4. Générer du feedback personnalisé

**POST** `/api/ai/generate-feedback`

```json
{
  "exerciseId": "uuid-de-l-exercice",
  "userAnswer": "Réponse de l'élève",
  "isCorrect": false
}
```

**Réponse** :

```json
{
  "success": true,
  "feedback": {
    "feedback": "...",
    "encouragement": "...",
    "next_steps": "..."
  }
}
```

---

## 🏗️ Architecture

```
backend_minimal/
├── server_minimal.js       # Serveur Express minimal
├── routes/
│   └── ai.js               # Routes de génération IA
├── package.json
├── .env.example
└── README.md
```

**C'est tout !** Plus de modèles, contrôleurs, middleware d'auth, etc.

---

## 🔐 Sécurité

### Authentification

L'API **ne nécessite pas d'authentification** car elle est censée être appelée :
1. Par des **administrateurs/professeurs** depuis un dashboard sécurisé
2. Avec des **tokens Supabase** vérifiés côté client

Si vous voulez sécuriser davantage :

```javascript
// Ajouter un middleware simple
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (token !== process.env.ADMIN_SECRET) {
    return res.status(401).json({ success: false, message: 'Non autorisé' });
  }
  
  next();
};

// Appliquer sur les routes
router.post('/generate-exercises', authMiddleware, async (req, res) => {
  // ...
});
```

---

## 💰 Coûts OpenAI

Estimation des coûts (GPT-4 - mai 2024) :

| Opération | Tokens moyens | Coût estimé |
|-----------|---------------|-------------|
| 1 exercice | 500-800 | $0.015-0.024 |
| 5 exercices | 2000-3000 | $0.06-0.09 |
| Contenu de cours | 3000-4000 | $0.09-0.12 |
| Feedback | 200-300 | $0.006-0.009 |

**Astuce** : Utilisez GPT-3.5-turbo pour les feedbacks (10x moins cher).

---

## 🚀 Déploiement

### Option 1 : Vercel / Netlify Functions

Convertissez les routes en serverless functions.

### Option 2 : Railway / Render

```bash
# Déployez directement
railway up
# ou
render deploy
```

### Option 3 : Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server_minimal.js"]
```

---

## 🧪 Test

```bash
# Générer des exercices
curl -X POST http://localhost:3000/api/ai/generate-exercises \
  -H "Content-Type: application/json" \
  -d '{
    "courseId": "123",
    "grade": "6ème",
    "topic": "Fractions",
    "count": 2
  }'
```

---

## 📊 Comparaison

| Avant (Full Backend) | Après (Minimal + Supabase) |
|---------------------|----------------------------|
| 2000+ lignes de code | ~400 lignes |
| 15+ fichiers | 4 fichiers |
| PostgreSQL local requis | Supabase géré |
| Auth custom | Supabase Auth |
| Sequelize ORM | Client Supabase |
| Maintenance élevée | Maintenance minimale |

---

## ❓ FAQ

### Q: Peut-on supprimer complètement le backend ?

**R:** Oui, si vous ne voulez pas de génération IA. Sinon, gardez ce minimal backend pour les appels OpenAI.

### Q: Pourquoi ne pas mettre la génération IA côté client ?

**R:** 
1. Sécurité : La clé OpenAI ne doit pas être exposée
2. Coûts : Contrôle centralisé des appels API
3. Supabase Functions : Alternative possible (voir ci-dessous)

### Q: Alternative avec Supabase Edge Functions ?

**R:** Vous pouvez migrer ces routes vers des Supabase Edge Functions (Deno) pour éliminer complètement ce serveur !

---

## 🎉 Résultat

Vous avez maintenant :
- ✅ Backend **90% plus petit**
- ✅ Déploiement **beaucoup plus simple**
- ✅ Maintenance **quasi-nulle**
- ✅ Supabase gère toute la complexité
- ✅ Focus sur l'IA uniquement

---

Créé avec ❤️ pour Mathia




