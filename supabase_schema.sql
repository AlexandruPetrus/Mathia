-- ============================================
-- SCHÉMA SUPABASE POUR MATHIA
-- Base de données optimisée pour app mobile
-- ============================================

-- Activer les extensions nécessaires
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- Pour la recherche full-text

-- ============================================
-- TABLE: users (profils utilisateurs)
-- ============================================
-- Note: auth.users est géré par Supabase Auth
-- Cette table contient les données de profil supplémentaires

CREATE TABLE IF NOT EXISTS public.users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  grade TEXT NOT NULL CHECK (grade IN ('6ème', '5ème', '4ème', '3ème')),
  role TEXT DEFAULT 'student' CHECK (role IN ('student', 'teacher', 'admin')),
  avatar_url TEXT,
  total_points INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  last_login TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour améliorer les performances
CREATE INDEX idx_users_grade ON public.users(grade);
CREATE INDEX idx_users_role ON public.users(role);
CREATE INDEX idx_users_email ON public.users(email);

-- Trigger pour mettre à jour updated_at automatiquement
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- TABLE: courses (cours)
-- ============================================

CREATE TABLE IF NOT EXISTS public.courses (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  description TEXT,
  content TEXT,
  grade TEXT NOT NULL CHECK (grade IN ('6ème', '5ème', '4ème', '3ème')),
  topic TEXT NOT NULL, -- Arithmétique, Algèbre, Géométrie, etc.
  difficulty TEXT CHECK (difficulty IN ('facile', 'moyen', 'difficile')),
  duration INTEGER, -- Durée estimée en minutes
  order_num INTEGER DEFAULT 0, -- Pour l'ordre d'affichage
  is_published BOOLEAN DEFAULT true,
  thumbnail_url TEXT,
  created_by UUID REFERENCES public.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour recherche et filtres
CREATE INDEX idx_courses_grade ON public.courses(grade);
CREATE INDEX idx_courses_topic ON public.courses(topic);
CREATE INDEX idx_courses_difficulty ON public.courses(difficulty);
CREATE INDEX idx_courses_is_published ON public.courses(is_published);
CREATE INDEX idx_courses_order ON public.courses(order_num);

-- Index pour recherche full-text
CREATE INDEX idx_courses_search ON public.courses USING GIN (
  to_tsvector('french', coalesce(title, '') || ' ' || coalesce(description, ''))
);

CREATE TRIGGER update_courses_updated_at BEFORE UPDATE ON public.courses
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- TABLE: exercises (exercices)
-- ============================================

CREATE TABLE IF NOT EXISTS public.exercises (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  course_id UUID NOT NULL REFERENCES public.courses(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  question TEXT NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('qcm', 'libre', 'vrai-faux', 'calcul')),
  options JSONB, -- Pour les QCM: {"A": "...", "B": "...", "C": "...", "D": "..."}
  answer TEXT NOT NULL,
  explanation TEXT,
  difficulty TEXT CHECK (difficulty IN ('facile', 'moyen', 'difficile')),
  points INTEGER DEFAULT 10,
  hints JSONB, -- Array de hints: ["hint 1", "hint 2"]
  tags JSONB, -- Array de tags: ["fractions", "division"]
  order_num INTEGER DEFAULT 0,
  is_published BOOLEAN DEFAULT true,
  ai_generated BOOLEAN DEFAULT false,
  validated_by_teacher BOOLEAN DEFAULT false,
  usage_count INTEGER DEFAULT 0, -- Nombre de fois utilisé
  success_rate DECIMAL(5,2) DEFAULT 0, -- Taux de réussite en %
  created_by UUID REFERENCES public.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour optimiser les requêtes
CREATE INDEX idx_exercises_course_id ON public.exercises(course_id);
CREATE INDEX idx_exercises_difficulty ON public.exercises(difficulty);
CREATE INDEX idx_exercises_type ON public.exercises(type);
CREATE INDEX idx_exercises_is_published ON public.exercises(is_published);
CREATE INDEX idx_exercises_order ON public.exercises(order_num);
CREATE INDEX idx_exercises_ai_generated ON public.exercises(ai_generated, validated_by_teacher);

-- Index GIN pour recherche dans JSONB tags
CREATE INDEX idx_exercises_tags ON public.exercises USING GIN (tags);

-- Index pour recherche full-text
CREATE INDEX idx_exercises_search ON public.exercises USING GIN (
  to_tsvector('french', coalesce(title, '') || ' ' || coalesce(description, '') || ' ' || coalesce(question, ''))
);

CREATE TRIGGER update_exercises_updated_at BEFORE UPDATE ON public.exercises
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- TABLE: attempts (tentatives des élèves)
-- ============================================

CREATE TABLE IF NOT EXISTS public.attempts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  exercise_id UUID NOT NULL REFERENCES public.exercises(id) ON DELETE CASCADE,
  user_answer TEXT NOT NULL,
  is_correct BOOLEAN NOT NULL,
  points_earned INTEGER DEFAULT 0,
  time_spent INTEGER, -- Temps passé en secondes
  hints_used INTEGER DEFAULT 0,
  attempt_number INTEGER DEFAULT 1, -- Numéro de la tentative (1, 2, 3...)
  feedback TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour optimiser les requêtes
CREATE INDEX idx_attempts_user_id ON public.attempts(user_id);
CREATE INDEX idx_attempts_exercise_id ON public.attempts(exercise_id);
CREATE INDEX idx_attempts_user_exercise ON public.attempts(user_id, exercise_id);
CREATE INDEX idx_attempts_is_correct ON public.attempts(is_correct);
CREATE INDEX idx_attempts_created_at ON public.attempts(created_at DESC);

-- ============================================
-- TABLE: favorites (cours favoris)
-- ============================================

CREATE TABLE IF NOT EXISTS public.favorites (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  course_id UUID NOT NULL REFERENCES public.courses(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, course_id) -- Un utilisateur ne peut pas favoriser 2x le même cours
);

CREATE INDEX idx_favorites_user_id ON public.favorites(user_id);
CREATE INDEX idx_favorites_course_id ON public.favorites(course_id);

-- ============================================
-- TABLE: progress (progression des élèves)
-- ============================================

CREATE TABLE IF NOT EXISTS public.progress (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  course_id UUID NOT NULL REFERENCES public.courses(id) ON DELETE CASCADE,
  exercises_completed INTEGER DEFAULT 0,
  exercises_total INTEGER DEFAULT 0,
  score DECIMAL(5,2) DEFAULT 0, -- Score moyen en %
  time_spent INTEGER DEFAULT 0, -- Temps total en secondes
  last_activity TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ, -- Date de complétion si terminé
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, course_id)
);

CREATE INDEX idx_progress_user_id ON public.progress(user_id);
CREATE INDEX idx_progress_course_id ON public.progress(course_id);
CREATE INDEX idx_progress_last_activity ON public.progress(last_activity DESC);

CREATE TRIGGER update_progress_updated_at BEFORE UPDATE ON public.progress
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- POLITIQUES DE SÉCURITÉ (ROW LEVEL SECURITY)
-- ============================================

-- Activer RLS sur toutes les tables
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.favorites ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.progress ENABLE ROW LEVEL SECURITY;

-- Politiques pour users
CREATE POLICY "Users can view their own profile" ON public.users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON public.users
  FOR UPDATE USING (auth.uid() = id);

-- Politiques pour courses (lecture publique pour étudiants)
CREATE POLICY "Anyone can view published courses" ON public.courses
  FOR SELECT USING (is_published = true);

CREATE POLICY "Teachers can insert courses" ON public.courses
  FOR INSERT WITH CHECK (
    auth.uid() IN (SELECT id FROM public.users WHERE role IN ('teacher', 'admin'))
  );

CREATE POLICY "Teachers can update their own courses" ON public.courses
  FOR UPDATE USING (
    created_by = auth.uid() OR
    auth.uid() IN (SELECT id FROM public.users WHERE role = 'admin')
  );

-- Politiques pour exercises
CREATE POLICY "Anyone can view published exercises" ON public.exercises
  FOR SELECT USING (is_published = true);

CREATE POLICY "Teachers can insert exercises" ON public.exercises
  FOR INSERT WITH CHECK (
    auth.uid() IN (SELECT id FROM public.users WHERE role IN ('teacher', 'admin'))
  );

CREATE POLICY "Teachers can update exercises" ON public.exercises
  FOR UPDATE USING (
    created_by = auth.uid() OR
    auth.uid() IN (SELECT id FROM public.users WHERE role = 'admin')
  );

-- Politiques pour attempts
CREATE POLICY "Users can view their own attempts" ON public.attempts
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can insert their own attempts" ON public.attempts
  FOR INSERT WITH CHECK (user_id = auth.uid());

-- Politiques pour favorites
CREATE POLICY "Users can view their own favorites" ON public.favorites
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can manage their own favorites" ON public.favorites
  FOR ALL USING (user_id = auth.uid());

-- Politiques pour progress
CREATE POLICY "Users can view their own progress" ON public.progress
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can update their own progress" ON public.progress
  FOR ALL USING (user_id = auth.uid());

-- ============================================
-- FONCTIONS UTILITAIRES
-- ============================================

-- Fonction pour créer automatiquement un profil utilisateur lors de l'inscription
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email, username, first_name, last_name, grade)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1)),
    COALESCE(NEW.raw_user_meta_data->>'first_name', 'Prénom'),
    COALESCE(NEW.raw_user_meta_data->>'last_name', 'Nom'),
    COALESCE(NEW.raw_user_meta_data->>'grade', '6ème')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger pour créer le profil automatiquement
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Fonction pour rechercher des cours
CREATE OR REPLACE FUNCTION search_courses(search_query TEXT)
RETURNS TABLE (
  id UUID,
  title TEXT,
  description TEXT,
  grade TEXT,
  topic TEXT,
  difficulty TEXT,
  rank REAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    c.id,
    c.title,
    c.description,
    c.grade,
    c.topic,
    c.difficulty,
    ts_rank(
      to_tsvector('french', coalesce(c.title, '') || ' ' || coalesce(c.description, '')),
      plainto_tsquery('french', search_query)
    ) AS rank
  FROM public.courses c
  WHERE
    c.is_published = true
    AND to_tsvector('french', coalesce(c.title, '') || ' ' || coalesce(c.description, ''))
    @@ plainto_tsquery('french', search_query)
  ORDER BY rank DESC;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour mettre à jour les statistiques d'un exercice
CREATE OR REPLACE FUNCTION update_exercise_stats()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE public.exercises
  SET
    usage_count = (
      SELECT COUNT(*) FROM public.attempts WHERE exercise_id = NEW.exercise_id
    ),
    success_rate = (
      SELECT COALESCE(
        AVG(CASE WHEN is_correct THEN 100.0 ELSE 0.0 END),
        0
      )
      FROM public.attempts
      WHERE exercise_id = NEW.exercise_id
    )
  WHERE id = NEW.exercise_id;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour mettre à jour les stats après chaque tentative
DROP TRIGGER IF EXISTS update_stats_after_attempt ON public.attempts;
CREATE TRIGGER update_stats_after_attempt
  AFTER INSERT ON public.attempts
  FOR EACH ROW EXECUTE FUNCTION update_exercise_stats();

-- Fonction pour mettre à jour les points de l'utilisateur
CREATE OR REPLACE FUNCTION update_user_points()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE public.users
  SET total_points = (
    SELECT COALESCE(SUM(points_earned), 0)
    FROM public.attempts
    WHERE user_id = NEW.user_id AND is_correct = true
  )
  WHERE id = NEW.user_id;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour mettre à jour les points après chaque tentative
DROP TRIGGER IF EXISTS update_points_after_attempt ON public.attempts;
CREATE TRIGGER update_points_after_attempt
  AFTER INSERT ON public.attempts
  FOR EACH ROW EXECUTE FUNCTION update_user_points();

-- ============================================
-- DONNÉES DE TEST (OPTIONNEL - à supprimer en production)
-- ============================================

-- Vous pouvez insérer des données de test ici si nécessaire
-- Exemple de cours de démonstration :
/*
INSERT INTO public.courses (title, description, grade, topic, difficulty, is_published, order_num)
VALUES
  ('Introduction aux fractions', 'Apprendre les bases des fractions', '6ème', 'Arithmétique', 'facile', true, 1),
  ('Les équations du premier degré', 'Résoudre des équations simples', '3ème', 'Algèbre', 'moyen', true, 2),
  ('Géométrie : les triangles', 'Propriétés des triangles', '5ème', 'Géométrie', 'moyen', true, 3);
*/

-- ============================================
-- FIN DU SCHÉMA
-- ============================================

-- Pour vérifier que tout est bien créé :
SELECT
  'Tables créées: ' || COUNT(*) AS summary
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('users', 'courses', 'exercises', 'attempts', 'favorites', 'progress');
