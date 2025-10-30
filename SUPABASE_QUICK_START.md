# 🚀 Démarrage Rapide avec Supabase

## 🎯 **Étapes simples pour démarrer Mathia avec Supabase**

### **1. Créer un compte Supabase (2 minutes)**
1. Allez sur [https://supabase.com](https://supabase.com)
2. Cliquez sur **"Start your project"**
3. Connectez-vous avec GitHub
4. Créez un nouveau projet :
   - **Nom** : `mathia`
   - **Mot de passe** : Choisissez un mot de passe sécurisé
   - **Région** : Europe (Frankfurt)
   - **Plan** : Free

### **2. Récupérer les clés (1 minute)**
Une fois le projet créé :
1. Allez dans **Settings** → **API**
2. Copiez ces informations :
   - **Project URL** : `https://xxxxxxxx.supabase.co`
   - **anon key** : `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### **3. Configurer l'environnement**
Créez un fichier `.env` avec :
```env
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
PORT=3000
```

### **4. Créer les tables**
Dans Supabase, allez dans **SQL Editor** et exécutez ce script :

```sql
-- Créer les tables pour Mathia
CREATE TABLE IF NOT EXISTS users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  role TEXT DEFAULT 'student' CHECK (role IN ('student', 'teacher', 'admin')),
  grade TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS courses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT NOT NULL,
  grade TEXT NOT NULL,
  chapter TEXT,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS exercises (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
  type TEXT NOT NULL CHECK (type IN ('qcm', 'libre', 'vrai-faux', 'calcul')),
  body TEXT NOT NULL,
  options JSONB,
  answer TEXT NOT NULL,
  explanation TEXT,
  difficulty TEXT DEFAULT 'moyen' CHECK (difficulty IN ('facile', 'moyen', 'difficile')),
  tags JSONB DEFAULT '[]',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS attempts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  exercise_id UUID REFERENCES exercises(id) ON DELETE CASCADE,
  answer TEXT NOT NULL,
  is_correct BOOLEAN NOT NULL,
  time_spent INTEGER, -- en secondes
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Activer Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE attempts ENABLE ROW LEVEL SECURITY;

-- Politiques de sécurité basiques
CREATE POLICY "Users can view their own data" ON users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Anyone can view courses" ON courses
  FOR SELECT USING (true);

CREATE POLICY "Anyone can view exercises" ON exercises
  FOR SELECT USING (true);

CREATE POLICY "Users can view their own attempts" ON attempts
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own attempts" ON attempts
  FOR INSERT WITH CHECK (auth.uid() = user_id);
```

### **5. Démarrer l'application**
```bash
npm install
npm run dev
```

### **6. Importer les exercices**
Une fois Supabase configuré, utilisez le script d'import :
```bash
python scripts/import_to_supabase.py
```

---

## 🎉 **Avantages de Supabase :**

- ✅ **Pas d'installation PostgreSQL** - Tout est hébergé
- ✅ **API REST automatique** - Plus besoin de créer les routes
- ✅ **Authentification intégrée** - JWT, OAuth, etc.
- ✅ **Interface d'administration** - Dashboard visuel
- ✅ **Temps réel** - Mises à jour en direct
- ✅ **Gratuit** - Plan gratuit très généreux

---

## 📱 **Pour l'app mobile Flutter :**

Ajoutez dans `pubspec.yaml` :
```yaml
dependencies:
  supabase_flutter: ^2.3.0
```

Et initialisez Supabase dans votre app Flutter avec les mêmes clés.

---

**🚀 En 10 minutes, vous aurez Mathia qui fonctionne avec Supabase !**