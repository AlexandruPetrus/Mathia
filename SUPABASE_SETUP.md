# 🚀 Migration vers Supabase - Guide Complet

## 📋 Vue d'ensemble

Ce guide vous permet de migrer **Mathia** de PostgreSQL local + Express vers **Supabase**.

### Avantages de cette migration :
- ✅ **Base de données hébergée** - Plus besoin d'installer PostgreSQL
- ✅ **API REST auto-générée** - Routes CRUD automatiques
- ✅ **Authentification intégrée** - JWT, OAuth, email/password
- ✅ **Temps réel** - Mises à jour en direct
- ✅ **Row Level Security** - Sécurité au niveau des lignes
- ✅ **Client Flutter officiel** - Intégration facile
- ✅ **Dashboard visuel** - Interface d'administration

---

## 🎯 Étape 1 : Créer un compte Supabase

1. Allez sur [https://supabase.com](https://supabase.com)
2. Cliquez sur **"Start your project"**
3. Connectez-vous avec GitHub (recommandé)
4. Créez une nouvelle organisation (gratuit)

---

## 🏗️ Étape 2 : Créer un projet

1. Cliquez sur **"New Project"**
2. Remplissez les informations :
   - **Nom** : `mathia-production` (ou `mathia-dev`)
   - **Database Password** : Générez un mot de passe sécurisé (sauvegardez-le !)
   - **Region** : `Europe (Frankfurt)` (ou plus proche de vous)
   - **Pricing Plan** : `Free` (pour commencer)

3. Cliquez sur **"Create new project"**
4. ⏳ Attendez 2-3 minutes que le projet soit prêt

---

## 🔑 Étape 3 : Récupérer les clés API

Une fois le projet créé :

1. Allez dans **Settings** (⚙️) → **API**
2. Notez ces informations :

```
Project URL: https://xxxxxxxx.supabase.co
anon (public) key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
JWT Secret: votre-jwt-secret
```

⚠️ **Important** :
- La clé `anon` est publique (utilisée côté client)
- La clé `service_role` est secrète (utilisée côté serveur uniquement)

---

## 📊 Étape 4 : Créer les tables SQL

1. Dans le dashboard Supabase, allez dans **SQL Editor**
2. Cliquez sur **"New query"**
3. Copiez le contenu du fichier `supabase/schema.sql` (voir ci-dessous)
4. Cliquez sur **"Run"**

Les tables suivantes seront créées :
- `users` (profils utilisateurs étendus)
- `courses` (cours de mathématiques)
- `exercises` (exercices)
- `attempts` (tentatives des élèves)

---

## 🔒 Étape 5 : Configurer Row Level Security (RLS)

1. Dans le SQL Editor, créez une nouvelle requête
2. Copiez le contenu de `supabase/security.sql`
3. Exécutez-le

Cela activera les règles de sécurité :
- Les étudiants peuvent voir leurs propres données
- Les professeurs peuvent créer/modifier les cours et exercices
- Les admins ont tous les droits

---

## ⚙️ Étape 6 : Créer les fonctions SQL

1. Créez une nouvelle requête SQL
2. Copiez le contenu de `supabase/functions.sql`
3. Exécutez-le

Fonctions créées :
- `get_user_stats()` - Statistiques de l'utilisateur
- `get_course_progress()` - Progression dans un cours
- `calculate_success_rate()` - Taux de réussite

---

## 🔧 Étape 7 : Configurer l'authentification

### 7.1 Activer les providers

1. Allez dans **Authentication** → **Providers**
2. Activez **Email** (déjà activé par défaut)
3. Optionnel : Activez **Google**, **Apple**, etc.

### 7.2 Configuration email

1. Dans **Authentication** → **Email Templates**
2. Personnalisez les templates :
   - Confirmation d'email
   - Réinitialisation de mot de passe
   - Invitation

### 7.3 URL de redirection

Dans **Authentication** → **URL Configuration** :
- **Site URL** : `mathia://` (pour l'app mobile)
- **Redirect URLs** : 
  - `mathia://login-callback`
  - `mathia://reset-password`
  - `http://localhost:3000/auth/callback` (pour dev web)

---

## 📱 Étape 8 : Configuration Flutter

### 8.1 Ajouter les dépendances

Dans `mobile/pubspec.yaml` :

```yaml
dependencies:
  supabase_flutter: ^2.3.0
  # Supprimer http si vous ne l'utilisez plus pour l'API
```

### 8.2 Initialiser Supabase

Voir le fichier `SUPABASE_FLUTTER_INTEGRATION.md` pour les détails complets.

---

## 🌍 Étape 9 : Variables d'environnement

### Pour Flutter (mobile/.env) :

```env
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Pour le backend Express réduit (.env) :

```env
# Supabase (pour les opérations serveur uniquement)
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# OpenAI (pour génération d'exercices)
OPENAI_API_KEY=sk-xxxxxx

# API minimal
PORT=3000
```

---

## 🧪 Étape 10 : Tester la connexion

### Depuis le dashboard Supabase :

1. Allez dans **Table Editor**
2. Sélectionnez la table `users`
3. Ajoutez manuellement un utilisateur de test
4. Vérifiez que les données apparaissent

### Depuis Flutter :

```dart
// Test de connexion
final response = await Supabase.instance.client
    .from('users')
    .select()
    .limit(1);
    
print('Connexion réussie : $response');
```

---

## 📊 Étape 11 : Migrer les données existantes (optionnel)

Si vous avez déjà des données dans PostgreSQL :

### Option A : Export/Import CSV

1. Exportez vos tables PostgreSQL en CSV
2. Dans Supabase : **Table Editor** → Sélectionnez une table → **Import data from CSV**

### Option B : Script de migration

Utilisez le fichier `scripts/migrate_to_supabase.js` (voir backend réduit).

---

## 🎨 Étape 12 : Utiliser le Dashboard

### Table Editor
- Voir/modifier les données directement
- Importer/exporter en CSV
- Ajouter des colonnes

### SQL Editor
- Exécuter des requêtes custom
- Créer des vues
- Analyser les performances

### Authentication
- Voir les utilisateurs inscrits
- Gérer les sessions
- Bloquer des utilisateurs

### Storage (pour plus tard)
- Uploader des images d'exercices
- Fichiers PDF de cours
- Photos de profil

---

## 🔥 Étape 13 : Backend Express Minimal

Le nouveau backend Express sera **beaucoup plus petit** et ne servira que pour :
- ✅ Génération d'exercices avec OpenAI
- ✅ Opérations complexes qui nécessitent des calculs côté serveur
- ✅ Webhooks (notifications, paiements, etc.)

Tout le reste (CRUD, auth, stats) sera géré par **Supabase directement** !

---

## 📚 Prochaines étapes

1. ✅ Exécutez `supabase/schema.sql`
2. ✅ Exécutez `supabase/security.sql`
3. ✅ Exécutez `supabase/functions.sql`
4. ✅ Configurez l'authentification
5. ✅ Intégrez le client Supabase dans Flutter
6. ✅ Testez les fonctionnalités de base
7. ✅ Migrez progressivement les écrans Flutter

---

## 🆘 Dépannage

### Erreur de connexion
- Vérifiez que le projet Supabase est bien démarré (dashboard)
- Vérifiez les URLs et clés API dans `.env`

### RLS bloque les requêtes
- Vérifiez que l'utilisateur est bien authentifié
- Testez avec la clé `service_role` (côté serveur uniquement)
- Désactivez temporairement RLS pour déboguer

### Tables non trouvées
- Vérifiez que le schema SQL a bien été exécuté
- Regardez les logs d'erreur dans SQL Editor

---

## 📖 Ressources

- [Documentation Supabase](https://supabase.com/docs)
- [Client Flutter Supabase](https://supabase.com/docs/reference/dart/introduction)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
- [Exemples Flutter](https://github.com/supabase/supabase-flutter)

---

## 💰 Pricing (plan gratuit)

Le plan gratuit Supabase offre :
- ✅ 500 MB de base de données
- ✅ 1 GB de stockage de fichiers
- ✅ 2 GB de bande passante
- ✅ 50,000 utilisateurs actifs mensuels
- ✅ Row Level Security illimité
- ✅ Authentification complète

**Largement suffisant pour démarrer !** 🚀

---

Créé avec ❤️ pour Mathia




