# 🆘 Supabase - Guide de Dépannage

## Erreurs communes et solutions

---

## ❌ Erreur 1 : "permission denied for schema auth"

### Symptôme
```
ERROR: 42501: permission denied for schema auth
```

### Cause
Vous essayez de créer une fonction dans le schéma `auth`, qui est protégé par Supabase.

### Solution
✅ **Déjà corrigé !** Le fichier `security.sql` a été mis à jour.

- Utilisez directement `auth.uid()` au lieu de créer `auth.user_id()`
- Toutes les fonctions custom doivent être dans le schéma `public`

### Exemple
```sql
-- ❌ NE PAS FAIRE
CREATE FUNCTION auth.user_id() ...

-- ✅ UTILISER À LA PLACE
SELECT auth.uid()  -- Déjà disponible dans Supabase
```

---

## ❌ Erreur 2 : "relation does not exist"

### Symptôme
```
ERROR: relation "public.users" does not exist
```

### Cause
Les tables n'ont pas été créées. Vous n'avez pas exécuté `schema.sql`.

### Solution
1. Allez dans **SQL Editor** de Supabase
2. Copiez le contenu de `supabase/schema.sql`
3. Cliquez sur **"Run"**
4. Vérifiez dans **Table Editor** que les tables sont créées

---

## ❌ Erreur 3 : "new row violates row-level security policy"

### Symptôme
```
ERROR: new row violates row-level security policy for table "users"
```

### Cause
1. RLS est activé mais les policies ne sont pas configurées
2. Ou vous n'êtes pas authentifié

### Solution

#### Option A : Vérifier les policies
```sql
-- Vérifier que les policies existent
SELECT tablename, policyname 
FROM pg_policies 
WHERE schemaname = 'public';
```

Si vide, exécutez `supabase/security.sql`.

#### Option B : Utiliser service_role key (backend seulement)
```javascript
// Dans votre backend, utilisez la service_role key
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY  // Contourne RLS
);
```

⚠️ **Attention** : Ne JAMAIS exposer la `service_role` key côté client !

#### Option C : Vérifier l'authentification
```dart
// Dans Flutter, vérifiez que l'utilisateur est connecté
final user = Supabase.instance.client.auth.currentUser;
print('User: ${user?.id}');  // Doit afficher un UUID, pas null
```

---

## ❌ Erreur 4 : "function does not exist"

### Symptôme
```
ERROR: function "get_my_stats" does not exist
```

### Cause
Vous n'avez pas exécuté `functions.sql`.

### Solution
1. Allez dans **SQL Editor**
2. Copiez le contenu de `supabase/functions.sql`
3. Cliquez sur **"Run"**

### Vérification
```sql
-- Vérifier que les fonctions existent
SELECT routine_name 
FROM information_schema.routines 
WHERE routine_schema = 'public'
  AND routine_type = 'FUNCTION';
```

---

## ❌ Erreur 5 : "type does not exist"

### Symptôme
```
ERROR: type "grade_level" does not exist
```

### Cause
Les types ENUM n'ont pas été créés.

### Solution
Exécutez `schema.sql` **dans l'ordre** :
1. Les types ENUM sont créés au début du fichier
2. Puis les tables qui les utilisent

### Vérification
```sql
-- Vérifier les types ENUM
SELECT typname 
FROM pg_type 
WHERE typname IN ('grade_level', 'user_role', 'difficulty_level', 'exercise_type', 'topic_type');
```

---

## ❌ Erreur 6 : "Invalid JWT"

### Symptôme
```
ERROR: Invalid JWT
```

### Cause
1. La clé `SUPABASE_ANON_KEY` est incorrecte dans `.env`
2. Ou vous utilisez la clé d'un autre projet

### Solution
1. Allez dans **Supabase Dashboard** → **Settings** → **API**
2. Copiez la clé **anon public** (pas service_role)
3. Mettez-la dans `.env` :
```env
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
4. Redémarrez votre app Flutter

---

## ❌ Erreur 7 : "Failed to fetch"

### Symptôme
```
Error: Failed to fetch
```

### Cause
1. L'URL Supabase est incorrecte
2. Ou problème de connexion internet
3. Ou le projet Supabase est en pause (plan gratuit non utilisé)

### Solution
1. Vérifiez `SUPABASE_URL` dans `.env` :
```env
SUPABASE_URL=https://xxxxxxxx.supabase.co
```
2. Vérifiez que le projet est actif dans le dashboard
3. Si projet en pause, réactivez-le (plan gratuit se met en pause après 1 semaine d'inactivité)

---

## ❌ Erreur 8 : "duplicate key value violates unique constraint"

### Symptôme
```
ERROR: duplicate key value violates unique constraint "users_username_key"
```

### Cause
Vous essayez d'insérer un username qui existe déjà.

### Solution
```dart
// Vérifier si le username existe avant d'insérer
final existing = await supabase
    .from('users')
    .select('username')
    .eq('username', username)
    .maybeSingle();

if (existing != null) {
  throw Exception('Ce nom d\'utilisateur existe déjà');
}
```

---

## ❌ Erreur 9 : "insert or update on table violates foreign key constraint"

### Symptôme
```
ERROR: insert or update on table "exercises" violates foreign key constraint "exercises_course_id_fkey"
```

### Cause
Vous essayez de créer un exercice avec un `course_id` qui n'existe pas.

### Solution
```dart
// Vérifier que le cours existe
final course = await supabase
    .from('courses')
    .select('id')
    .eq('id', courseId)
    .single();

// Puis créer l'exercice
await supabase.from('exercises').insert({
  'course_id': courseId,
  // ...
});
```

---

## ❌ Erreur 10 : "column does not exist"

### Symptôme
```
ERROR: column "total_points" does not exist
```

### Cause
1. Faute de frappe dans le nom de colonne
2. Ou la table n'a pas été créée correctement

### Solution
1. Vérifiez l'orthographe : `total_points` (avec underscore)
2. Vérifiez dans **Table Editor** que la colonne existe
3. Si manquante, ajoutez-la :
```sql
ALTER TABLE public.users ADD COLUMN total_points INTEGER DEFAULT 0;
```

---

## 🔍 Commandes de diagnostic

### Vérifier toutes les tables
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
```

### Vérifier les colonnes d'une table
```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name = 'users'
ORDER BY ordinal_position;
```

### Vérifier RLS
```sql
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';
```

### Vérifier les policies
```sql
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
```

### Vérifier les fonctions
```sql
SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
ORDER BY routine_name;
```

### Vérifier l'utilisateur actuel
```sql
SELECT auth.uid() AS current_user_id;
-- NULL = pas authentifié
-- UUID = authentifié
```

---

## 🧪 Script de test complet

Exécutez ce script pour vérifier que tout est bien configuré :

```sql
-- ============================================
-- SCRIPT DE VÉRIFICATION COMPLÈTE
-- ============================================

-- Test 1: Tables
SELECT 'Tables' AS test, COUNT(*) AS count
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN ('users', 'courses', 'exercises', 'attempts', 'course_progress', 'favorites');
-- Attendu: 6

-- Test 2: RLS activé
SELECT 'RLS' AS test, COUNT(*) AS count
FROM pg_tables 
WHERE schemaname = 'public' 
  AND rowsecurity = true;
-- Attendu: 6

-- Test 3: Policies
SELECT 'Policies' AS test, COUNT(*) AS count
FROM pg_policies 
WHERE schemaname = 'public';
-- Attendu: 20+

-- Test 4: Fonctions
SELECT 'Functions' AS test, COUNT(*) AS count
FROM information_schema.routines
WHERE routine_schema = 'public'
  AND routine_name LIKE 'get_%' OR routine_name LIKE 'is_%';
-- Attendu: 10+

-- Test 5: Types ENUM
SELECT 'ENUM Types' AS test, COUNT(*) AS count
FROM pg_type 
WHERE typname IN ('grade_level', 'user_role', 'difficulty_level', 'exercise_type', 'topic_type');
-- Attendu: 5

-- ✅ Si tous les tests affichent les bonnes valeurs, votre base est prête !
```

---

## 📞 Besoin d'aide supplémentaire ?

### Ressources
- [Documentation Supabase](https://supabase.com/docs)
- [Community Discord](https://discord.supabase.com)
- [GitHub Discussions](https://github.com/supabase/supabase/discussions)

### Dans le dashboard Supabase
1. **Logs** → Voir les erreurs en temps réel
2. **Table Editor** → Vérifier les données
3. **SQL Editor** → Exécuter des requêtes de diagnostic
4. **API Docs** → Voir les endpoints générés

---

## 💡 Astuces

### Activer les logs détaillés (Flutter)
```dart
await Supabase.initialize(
  url: supabaseUrl,
  anonKey: supabaseKey,
  debug: true,  // Active les logs détaillés
);
```

### Tester RLS désactivé temporairement
```sql
-- ⚠️ SEULEMENT POUR DEBUG !
ALTER TABLE public.users DISABLE ROW LEVEL SECURITY;

-- Tester vos requêtes...

-- Réactiver
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
```

### Utiliser service_role pour debug
```dart
// Dans votre terminal Flutter
final supabase = SupabaseClient(
  supabaseUrl,
  supabaseServiceKey,  // Contourne RLS
);

// Tester si la requête fonctionne sans RLS
```

---

Bonne chance ! 🚀




