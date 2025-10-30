# 🚀 Guide de Migration - PostgreSQL vers Supabase

## ⚠️ IMPORTANT : Quelle app mobile utilisez-vous ?

**Votre projet utilise actuellement SwiftUI (iOS natif), pas Flutter !**

📱 Consultez d'abord **[QUELLE_APP_MOBILE.md](QUELLE_APP_MOBILE.md)** pour comprendre votre situation.

### Guides disponibles

- 🍎 **SwiftUI** (ce que vous avez) → [SUPABASE_SWIFT_INTEGRATION.md](SUPABASE_SWIFT_INTEGRATION.md)
- 🦋 **Flutter** (si vous voulez créer une nouvelle app) → [SUPABASE_FLUTTER_INTEGRATION.md](SUPABASE_FLUTTER_INTEGRATION.md)

---

## 📋 Plan de migration complet

Ce guide vous accompagne étape par étape pour migrer Mathia de PostgreSQL local + Express vers Supabase.

---

## 📊 Vue d'ensemble de la migration

### Avant
```
┌─────────────┐
│   Flutter   │
│   Mobile    │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   Express   │
│   Backend   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ PostgreSQL  │
│   Local     │
└─────────────┘
```

### Après
```
┌─────────────┐
│   Flutter   │──────┐
│   Mobile    │      │
└─────────────┘      │
                     │ Supabase SDK
                     ▼
              ┌─────────────┐
              │  Supabase   │
              │ (PostgreSQL │
              │  + Auth +   │
              │  API REST)  │
              └─────────────┘
                     ▲
                     │ (optionnel)
              ┌──────┴──────┐
              │   Backend   │
              │  Minimal    │
              │  (IA only)  │
              └─────────────┘
```

---

## ✅ Checklist de migration

### Phase 1 : Préparation (30 min)
- [ ] Créer un compte Supabase
- [ ] Créer un nouveau projet Supabase
- [ ] Noter les clés API (URL, anon key, service key)
- [ ] Installer le CLI Supabase (optionnel)

### Phase 2 : Base de données (1h)
- [ ] Exécuter `supabase/schema.sql` dans SQL Editor
- [ ] Exécuter `supabase/security.sql` (RLS)
- [ ] Exécuter `supabase/functions.sql` (fonctions SQL)
- [ ] Vérifier les tables dans Table Editor
- [ ] Configurer l'authentification (Email, providers)

### Phase 3 : Backend Minimal (30 min)
- [ ] Copier le dossier `backend_minimal/`
- [ ] Installer les dépendances (`npm install`)
- [ ] Configurer `.env` avec clés Supabase + OpenAI
- [ ] Tester le démarrage (`npm start`)
- [ ] Tester la génération d'exercices

### Phase 4 : App Mobile SwiftUI (2-3h)
- [ ] Ouvrir le projet dans Xcode
- [ ] Ajouter le package Supabase Swift
- [ ] Créer `Config.swift` avec les clés
- [ ] Initialiser Supabase dans `MathiaApp.swift`
- [ ] Mettre à jour les modèles (`Models/`)
- [ ] Créer les nouveaux services (`Services/`)
- [ ] Mettre à jour les vues (`Views/`)

**📖 Guide détaillé** : [SUPABASE_SWIFT_INTEGRATION.md](SUPABASE_SWIFT_INTEGRATION.md)

### Phase 5 : Tests (1h)
- [ ] Tester l'inscription
- [ ] Tester la connexion
- [ ] Tester l'affichage des cours
- [ ] Tester la soumission d'exercices
- [ ] Tester les statistiques
- [ ] Tester le leaderboard

### Phase 6 : Nettoyage (30 min)
- [ ] Supprimer l'ancien backend Express
- [ ] Supprimer les anciens services HTTP dans Flutter
- [ ] Mettre à jour la documentation
- [ ] Commit et push

---

## 🔧 Étape 1 : Configuration Supabase

### 1.1 Créer le projet

1. Allez sur [https://supabase.com](https://supabase.com)
2. Créez un compte / Connectez-vous
3. Créez un nouveau projet :
   - **Nom** : mathia-production
   - **Password** : Générez un mot de passe fort
   - **Region** : Europe (Frankfurt) ou plus proche
   - **Plan** : Free

### 1.2 Récupérer les clés

Une fois le projet créé (2-3 min) :

1. Allez dans **Settings** → **API**
2. Notez :
   - **Project URL** : `https://xxxxxxxx.supabase.co`
   - **anon public** : `eyJhbGc...`
   - **service_role** : `eyJhbGc...` (⚠️ SECRET)

### 1.3 Exécuter les scripts SQL

Dans **SQL Editor** → **New query** :

1. **Schéma** : Copiez/collez `supabase/schema.sql` → Run
2. **Sécurité** : Copiez/collez `supabase/security.sql` → Run
3. **Fonctions** : Copiez/collez `supabase/functions.sql` → Run

✅ Vérifiez dans **Table Editor** que les tables sont créées.

---

## 📱 Étape 2 : Migrer l'application mobile

### ⚠️ Votre app est en SwiftUI, pas Flutter !

Vous avez actuellement une app **SwiftUI** dans `mobile/MathiaApp/`.

### 2.1 Ouvrir le projet Xcode

```bash
cd mobile
open MathiaApp.xcodeproj
```

### 2.2 Ajouter le package Supabase

Dans **Xcode** :
1. **File** → **Add Package Dependencies**
2. URL : `https://github.com/supabase/supabase-swift`
3. Version : `2.0.0`
4. Sélectionnez : `Supabase`, `Auth`, `PostgREST`, `Realtime`
5. **Add Package**

### 2.3 Configuration

Créez `mobile/MathiaApp/Config.swift` :

```swift
import Foundation

enum SupabaseConfig {
    static let url = URL(string: "https://xxxxxxxx.supabase.co")!
    static let anonKey = "eyJhbGc..."  // Votre anon key ici
}
```

### 2.4 Initialiser Supabase

Dans `mobile/MathiaApp/MathiaApp.swift` :

```swift
import SwiftUI
import Supabase

@main
struct MathiaApp: App {
    static let supabase = SupabaseClient(
        supabaseURL: SupabaseConfig.url,
        supabaseKey: SupabaseConfig.anonKey
    )
    
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### 2.5 Créer les services et modèles

📖 **Guide complet** : Suivez [SUPABASE_SWIFT_INTEGRATION.md](SUPABASE_SWIFT_INTEGRATION.md) pour :
- Mettre à jour les modèles (User, Course, Exercise, Attempt)
- Créer `SupabaseAuthService`
- Créer `CourseService`
- Créer `ExerciseService`
- Mettre à jour les vues

---

### 🦋 Si vous vouliez utiliser Flutter à la place

Si vous préférez créer une nouvelle app Flutter (iOS + Android), consultez :
- [QUELLE_APP_MOBILE.md](QUELLE_APP_MOBILE.md) - Comparer les options
- [SUPABASE_FLUTTER_INTEGRATION.md](SUPABASE_FLUTTER_INTEGRATION.md) - Guide Flutter complet

---

## 🤖 Étape 3 : Backend Minimal (Optionnel)

Si vous voulez garder la génération IA :

```bash
# Copier le backend minimal
cp -r backend_minimal/ mathia-backend-ai/

# Installer
cd mathia-backend-ai
npm install

# Configurer
cp .env.example .env
# Éditer .env avec vos clés

# Démarrer
npm start
```

Si vous ne voulez **pas** de génération IA, vous pouvez **complètement sauter** cette étape ! 🎉

---

## 📊 Étape 4 : Migrer les données existantes (Optionnel)

Si vous avez déjà des données dans PostgreSQL :

### Option A : Export/Import manuel

```bash
# Exporter depuis PostgreSQL
pg_dump -U postgres -d mathia_db --table=users --data-only --column-inserts > users.sql
pg_dump -U postgres -d mathia_db --table=courses --data-only --column-inserts > courses.sql

# Puis exécuter ces fichiers dans Supabase SQL Editor
```

### Option B : CSV

1. Exportez vos tables en CSV
2. Dans Supabase **Table Editor** → Table → **Import from CSV**

### Option C : Script de migration

Créez `scripts/migrate_data.js` :

```javascript
const { createClient } = require('@supabase/supabase-js');
const { Sequelize } = require('sequelize');

// Ancienne DB
const sequelize = new Sequelize(process.env.OLD_DATABASE_URL);

// Nouvelle DB (Supabase)
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

async function migrate() {
  // Migrer users
  const [users] = await sequelize.query('SELECT * FROM users');
  for (const user of users) {
    await supabase.from('users').insert({
      id: user.id,
      username: user.username,
      // ... autres champs
    });
  }
  
  // Migrer courses, exercises, attempts...
}

migrate();
```

---

## 🧪 Étape 5 : Tester

### Test 1 : Authentification

```dart
// Dans Flutter
final authService = AuthService();

// Inscription
final user = await authService.signUp(
  email: 'test@example.com',
  password: 'password123',
  username: 'test_user',
  firstName: 'Test',
  lastName: 'User',
  grade: '6ème',
);

print('Utilisateur créé : ${user.username}');
```

### Test 2 : Récupérer les cours

```dart
final courseService = CourseService();
final courses = await courseService.getCourses();

print('${courses.length} cours trouvés');
```

### Test 3 : Soumettre un exercice

```dart
final exerciseService = ExerciseService();

final result = await exerciseService.submitAttempt(
  exerciseId: 'uuid-exercice',
  userAnswer: '42',
  timeSpent: 120,
  hintsUsed: 0,
);

print('Correct : ${result['is_correct']}');
print('Points gagnés : ${result['points_earned']}');
```

### Test 4 : Statistiques

```dart
final statsService = StatsService();
final stats = await statsService.getMyStats();

print('Total points : ${stats['total_points']}');
print('Taux de réussite : ${stats['success_rate']}%');
```

---

## 🔥 Étape 6 : Nettoyage

Une fois que tout fonctionne :

### Supprimer l'ancien code

```bash
# Sauvegarder l'ancien backend (au cas où)
mv backend/ backend_old/

# Supprimer l'ancien code HTTP dans Flutter
rm -rf mobile/lib/services/http_service.dart
rm -rf mobile/lib/services/api_service.dart

# Garder seulement le backend minimal (si nécessaire)
mv backend_minimal/ backend/
```

### Mettre à jour la doc

```bash
# Mettre à jour README.md
# Mettre à jour les instructions d'installation
# Supprimer les références à PostgreSQL local
```

---

## 🎯 Résultats attendus

### Avant la migration
- ⏳ Installation complexe (PostgreSQL, Node.js, Python)
- 📦 2000+ lignes de code backend
- 🐛 Maintenance élevée
- 🔐 Auth custom à gérer
- 💾 Backups manuels

### Après la migration
- ✅ Installation simple (Flutter + clés Supabase)
- 📦 ~400 lignes de code backend (ou 0 sans IA)
- 🎉 Maintenance minimale
- 🔐 Auth gérée par Supabase
- 💾 Backups automatiques
- 🚀 Temps réel disponible
- 📊 Dashboard admin intégré
- 🔒 RLS automatique
- 📈 Évolutivité infinie

---

## 💰 Coûts

### Plan Gratuit Supabase
- ✅ 500 MB de base de données
- ✅ 1 GB de stockage
- ✅ 2 GB de bande passante
- ✅ 50,000 utilisateurs actifs/mois
- ✅ Row Level Security illimité

**Suffisant pour 100-500 utilisateurs actifs** 🎉

### Si vous dépassez (Pro Plan - $25/mois)
- 8 GB de base de données
- 100 GB de stockage
- 250 GB de bande passante
- Support prioritaire

---

## 🆘 Dépannage

### Erreur : "relation users does not exist"
➡️ Vous n'avez pas exécuté `schema.sql`

### Erreur : RLS policy violation
➡️ Vous n'avez pas exécuté `security.sql` ou l'utilisateur n'est pas authentifié

### Erreur : Function not found
➡️ Vous n'avez pas exécuté `functions.sql`

### Les tables sont vides
➡️ Normal si nouvelle installation. Inscrivez un utilisateur de test.

### OpenAI API error
➡️ Vérifiez votre clé API OpenAI dans `.env`

---

## 📚 Ressources

- [Documentation Supabase](https://supabase.com/docs)
- [Supabase Flutter](https://supabase.com/docs/reference/dart/introduction)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
- [SQL Editor](https://supabase.com/docs/guides/database/sql-editor)
- [Table Editor](https://supabase.com/docs/guides/database/table-editor)

---

## ⏱️ Temps estimé

| Étape | Durée | Difficulté |
|-------|-------|------------|
| Créer compte Supabase | 10 min | ⭐ |
| Exécuter scripts SQL | 15 min | ⭐ |
| Configurer Flutter | 30 min | ⭐⭐ |
| Créer les services | 1h | ⭐⭐⭐ |
| Migrer les écrans | 2h | ⭐⭐⭐ |
| Tests | 1h | ⭐⭐ |
| **TOTAL** | **~5h** | ⭐⭐⭐ |

---

## 🎉 Félicitations !

Vous avez maintenant :
- ✅ Une architecture moderne et scalable
- ✅ Un backend **90% plus petit**
- ✅ Une maintenance **quasi-nulle**
- ✅ Une sécurité **renforcée** (RLS)
- ✅ Le temps réel **disponible**
- ✅ Un dashboard **admin gratuit**
- ✅ Des backups **automatiques**

**Bienvenue dans le futur ! 🚀**

---

Créé avec ❤️ pour Mathia

