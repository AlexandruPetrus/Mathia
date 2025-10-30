# 📚 Guide d'utilisation de la documentation Swagger

## 🚀 Accéder à la documentation

Une fois le serveur démarré :

```bash
npm run dev
```

Ouvrez votre navigateur et accédez à :

**http://localhost:3000/api-docs**

## 🎯 Fonctionnalités de la documentation

### 📖 Interface Swagger UI

L'interface vous permet de :
- ✅ Visualiser toutes les routes disponibles
- ✅ Voir les paramètres requis et optionnels
- ✅ Consulter les exemples de requêtes et réponses
- ✅ **Tester directement les endpoints** depuis le navigateur

## 🔐 Tester les routes authentifiées

### Étape 1 : S'inscrire ou se connecter

1. Cliquez sur **Auth** → **POST /auth/signup** ou **POST /auth/login**
2. Cliquez sur "Try it out"
3. Entrez vos données :
   ```json
   {
     "name": "Test User",
     "email": "test@example.com",
     "password": "test123"
   }
   ```
4. Cliquez sur "Execute"
5. **Copiez le token** depuis la réponse

### Étape 2 : Autoriser les requêtes

1. Cliquez sur le bouton **"Authorize" 🔒** (en haut à droite)
2. Collez votre token dans le champ "Value" : 
   ```
   votre_token_ici
   ```
   (Sans le préfixe "Bearer", Swagger l'ajoute automatiquement)
3. Cliquez sur "Authorize"
4. Fermez la modal

### Étape 3 : Tester les routes protégées

Toutes les routes marquées avec un cadenas 🔒 sont maintenant accessibles !

Exemple avec GET /courses :
1. Cliquez sur **Courses** → **GET /courses**
2. Cliquez sur "Try it out"
3. Cliquez sur "Execute"
4. Consultez la réponse

## 📋 Organisation de la documentation

### Tags (sections)

- **Auth** : Routes publiques (signup, login)
- **Courses** : Gestion des cours (GET /courses, GET /courses/:id)
- **Exercises** : Gestion des exercices (GET /exercises avec filtres)
- **Attempts** : Soumission de réponses (POST /attempts)
- **Admin** : Routes administrateur (POST /admin/exercises)

### Pour chaque route

#### 1. Description
- Explication claire de ce que fait la route
- Fonctionnalités principales
- Si JWT est requis ou non

#### 2. Paramètres
- **Path parameters** : Variables dans l'URL (ex: `/courses/{id}`)
- **Query parameters** : Filtres dans l'URL (ex: `?courseId=1&difficulty=facile`)
- **Body** : Données JSON à envoyer

#### 3. Exemples multiples
Plusieurs exemples pour chaque route :
- Cas d'usage standard
- Cas avec options
- Cas minimal (champs requis uniquement)

#### 4. Réponses
Pour chaque code HTTP :
- **200** : Succès
- **201** : Créé avec succès
- **400** : Données invalides
- **401** : Non authentifié
- **404** : Ressource non trouvée
- **409** : Conflit (ex: email déjà utilisé)

Avec exemples de réponses pour chaque cas !

## 🎮 Scénario complet de test

### 1. Créer un compte
```
POST /auth/signup
Body:
{
  "name": "Test User",
  "email": "test@test.com",
  "password": "test123"
}
```
→ Copier le token

### 2. Autoriser (bouton "Authorize" 🔒)
Coller le token

### 3. Lister les cours
```
GET /courses
```

### 4. Créer un exercice
```
POST /admin/exercises
Body:
{
  "courseId": 1,
  "type": "qcm",
  "body": "Quelle est la moitié de 10?",
  "options": {"A": "3", "B": "5", "C": "7", "D": "10"},
  "answer": "B",
  "explanation": "10 ÷ 2 = 5",
  "difficulty": "facile",
  "tags": ["fractions"]
}
```

### 5. Lister les exercices avec filtre
```
GET /exercises?courseId=1&difficulty=facile
```

### 6. Soumettre une réponse
```
POST /attempts
Body:
{
  "exerciseId": 1,
  "userAnswer": "B"
}
```

## 📝 Exemples inclus dans la documentation

Chaque route contient plusieurs exemples :

### POST /auth/signup
- ✅ Inscription standard
- ✅ Inscription avec nom long

### POST /attempts
- ✅ Réponse correcte (avec explication)
- ✅ Réponse incorrecte (sans explication)

### POST /admin/exercises
- ✅ Exercice QCM complet
- ✅ Exercice libre
- ✅ Exercice minimal (champs requis seulement)

### GET /exercises
- ✅ Tous les exercices
- ✅ Filtrés par cours
- ✅ Filtrés par difficulté

## 🔍 Codes de réponse documentés

| Code | Description | Exemple |
|------|-------------|---------|
| 200 | Succès | Données récupérées |
| 201 | Créé | Ressource créée avec succès |
| 400 | Requête invalide | Validation Joi échouée |
| 401 | Non authentifié | Token manquant/invalide/expiré |
| 404 | Non trouvé | Ressource inexistante |
| 409 | Conflit | Email déjà utilisé |

## 💡 Astuces

### Copier les exemples
Utilisez les boutons "Copy" dans les exemples pour copier rapidement les JSON.

### Tester plusieurs scénarios
Utilisez le sélecteur d'exemples pour tester différents cas d'usage.

### Exporter la collection
Swagger UI permet d'exporter la spécification pour l'utiliser dans :
- Postman
- Insomnia
- curl
- Code generators

### Voir les schémas
Cliquez sur "Schemas" en bas de page pour voir tous les modèles de données.

## 📦 Modèles de données (Schemas)

La documentation inclut les schémas complets :

- **User** : Structure d'un utilisateur
- **Course** : Structure d'un cours
- **Exercise** : Structure d'un exercice (complète)
- **ExerciseSimple** : Version simplifiée (dans les listes)
- **Attempt** : Structure d'une tentative
- **Error** : Format des erreurs

## 🌐 Export et intégration

### Télécharger la spécification OpenAPI

L'URL de la spec JSON :
```
http://localhost:3000/api-docs.json
```

### Importer dans Postman

1. Ouvrir Postman
2. File → Import
3. Coller l'URL : `http://localhost:3000/api-docs.json`
4. Importer

### Importer dans Insomnia

1. Ouvrir Insomnia
2. Application → Preferences → Data → Import Data
3. From URL → `http://localhost:3000/api-docs.json`

## 🎨 Personnalisation

La documentation Swagger est servie par `server.js` :

```javascript
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument, {
  customCss: '.swagger-ui .topbar { display: none }',
  customSiteTitle: 'Mathia API Documentation'
}));
```

## 📚 Ressources

- **Swagger UI** : https://swagger.io/tools/swagger-ui/
- **OpenAPI Spec 3.0** : https://spec.openapis.org/oas/v3.0.3
- **Swagger Editor** : https://editor.swagger.io/ (pour éditer le YAML)

## ✅ Validation

Le fichier `openapi.yaml` est conforme à :
- ✅ OpenAPI 3.0.3
- ✅ Toutes les routes documentées
- ✅ Exemples complets pour chaque endpoint
- ✅ Codes de réponse HTTP standards
- ✅ Schémas de données structurés

---

🎉 **Votre API est maintenant entièrement documentée et testable !**









