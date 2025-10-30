#!/usr/bin/env python3
"""
Générateur de fichiers SQL petits directement depuis les JSON
Évite les problèmes d'encodage des gros fichiers
"""

import os
import json
import sys
from typing import List, Dict, Any
from datetime import datetime

def load_exercises_by_chapter() -> Dict[int, List[Dict[str, Any]]]:
    """Charger les exercices organisés par chapitre"""
    exercise_files = {
        'exercices_6eme.json': 1,
        'exercices_chapitre_1.json': 1,
        'exercices_chapitre_2.json': 2,
        'exercices_chapitre_3.json': 3,
        'exercices_chapitre_4.json': 4,
        'exercices_chapitre_5.json': 5,
        'exercices_chapitre_6.json': 6,
        'exercices_chapitre_7.json': 7,
        'exercices_chapitre_8.json': 8,
        'exercices_chapitre_9.json': 9
    }
    
    exercises_by_chapter = {}
    
    for filename, chapter_num in exercise_files.items():
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    exercises = json.load(f)
                    if not isinstance(exercises, list):
                        exercises = [exercises]
                    
                    if chapter_num not in exercises_by_chapter:
                        exercises_by_chapter[chapter_num] = []
                    
                    exercises_by_chapter[chapter_num].extend(exercises)
                    print(f"[OK] {filename}: {len(exercises)} exercices (chapitre {chapter_num})")
                    
            except Exception as e:
                print(f"[ERROR] Erreur {filename}: {e}")
        else:
            print(f"[WARNING] Fichier non trouvé: {filename}")
    
    return exercises_by_chapter

def escape_sql_string(text: str) -> str:
    """Échapper les caractères spéciaux pour SQL"""
    if not text:
        return "NULL"
    
    # Remplacer les apostrophes simples
    text = text.replace("'", "''")
    # Remplacer les retours à la ligne
    text = text.replace('\n', '\\n').replace('\r', '\\r')
    # Limiter la longueur pour éviter les erreurs
    if len(text) > 2000:
        text = text[:1997] + "..."
    
    return f"'{text}'"

def generate_schema_sql() -> str:
    """Générer le SQL du schéma de base"""
    return """-- ============================================
-- SCHÉMA DE BASE - MATHIA
-- ============================================
-- Exécutez ce fichier EN PREMIER dans Supabase

-- Vérifier et créer les types s'ils n'existent pas
DO $$ 
BEGIN
    -- Type pour les niveaux scolaires
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'grade_level') THEN
        CREATE TYPE grade_level AS ENUM ('6ème', '5ème', '4ème', '3ème');
    END IF;
    
    -- Type pour les rôles utilisateurs
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
        CREATE TYPE user_role AS ENUM ('student', 'teacher', 'admin');
    END IF;
    
    -- Type pour les difficultés
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'difficulty_level') THEN
        CREATE TYPE difficulty_level AS ENUM ('facile', 'moyen', 'difficile');
    END IF;
    
    -- Type pour les types d'exercices
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'exercise_type') THEN
        CREATE TYPE exercise_type AS ENUM ('qcm', 'libre', 'vrai-faux', 'calcul');
    END IF;
    
    -- Type pour les thèmes
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'topic_type') THEN
        CREATE TYPE topic_type AS ENUM (
            'Arithmétique',
            'Algèbre',
            'Géométrie',
            'Fractions',
            'Équations',
            'Proportionnalité',
            'Probabilités',
            'Statistiques',
            'Fonctions',
            'Théorème de Pythagore'
        );
    END IF;
END $$;

-- Créer les tables si elles n'existent pas
CREATE TABLE IF NOT EXISTS public.courses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    content TEXT NOT NULL,
    grade grade_level NOT NULL,
    topic topic_type NOT NULL,
    difficulty difficulty_level DEFAULT 'moyen' NOT NULL,
    duration INTEGER,
    order_num INTEGER DEFAULT 0 NOT NULL,
    is_published BOOLEAN DEFAULT false NOT NULL,
    thumbnail_url TEXT,
    author_id UUID,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE TABLE IF NOT EXISTS public.exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID REFERENCES public.courses(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    explanation TEXT,
    difficulty difficulty_level DEFAULT 'moyen' NOT NULL,
    points INTEGER DEFAULT 10 NOT NULL,
    time_limit INTEGER DEFAULT 300,
    type exercise_type DEFAULT 'qcm' NOT NULL,
    hints JSONB DEFAULT '[]'::jsonb,
    options JSONB,
    ai_generated BOOLEAN DEFAULT false NOT NULL,
    order_num INTEGER DEFAULT 0 NOT NULL,
    is_published BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Créer les index
CREATE INDEX IF NOT EXISTS idx_courses_grade ON public.courses(grade);
CREATE INDEX IF NOT EXISTS idx_courses_order ON public.courses(order_num);
CREATE INDEX IF NOT EXISTS idx_exercises_course ON public.exercises(course_id);
CREATE INDEX IF NOT EXISTS idx_exercises_difficulty ON public.exercises(difficulty);

-- ============================================
-- SCHÉMA CRÉÉ AVEC SUCCÈS !
-- ============================================
"""

def generate_courses_sql() -> str:
    """Générer le SQL pour créer les cours"""
    courses = [
        (1, "Nombres entiers", "Arithmétique"),
        (2, "Nombres décimaux", "Arithmétique"),
        (3, "Opérations sur les nombres", "Arithmétique"),
        (4, "Fractions", "Fractions"),
        (5, "Proportionnalité", "Proportionnalité"),
        (6, "Géométrie - Droites et angles", "Géométrie"),
        (7, "Géométrie - Triangles et quadrilatères", "Géométrie"),
        (8, "Périmètres et aires", "Géométrie"),
        (9, "Statistiques et probabilités", "Statistiques")
    ]
    
    sql = """-- ============================================
-- COURS - Création des cours de 6ème
-- ============================================

"""
    
    for chapter_num, title, topic in courses:
        sql += f"""INSERT INTO public.courses (
    id,
    title,
    description,
    content,
    grade,
    topic,
    difficulty,
    order_num,
    is_published
) VALUES (
    uuid_generate_v4(),
    '{title}',
    'Chapitre {chapter_num} du manuel de mathématiques 6ème',
    'Contenu du chapitre {chapter_num}: {title}',
    '6ème',
    '{topic}',
    'moyen',
    {chapter_num},
    true
) ON CONFLICT DO NOTHING;

"""
    
    return sql

def generate_exercises_sql_for_chapter(chapter_num: int, exercises: List[Dict[str, Any]]) -> str:
    """Générer le SQL pour les exercices d'un chapitre"""
    sql = f"""-- ============================================
-- EXERCICES CHAPITRE {chapter_num}
-- ============================================
-- Nombre d'exercices: {len(exercises)}

"""
    
    for i, exercise in enumerate(exercises, 1):
        # Déterminer le type d'exercice
        exercise_type = exercise.get('type', 'libre')
        if exercise_type not in ['qcm', 'libre', 'vrai-faux', 'calcul']:
            exercise_type = 'libre'
        
        # Préparer les options pour QCM
        options = exercise.get('options')
        options_json = "NULL"
        if options and isinstance(options, dict):
            options_json = f"'{json.dumps(options, ensure_ascii=False)}'"
        
        # Préparer les indices
        hints = exercise.get('hints', [])
        if not isinstance(hints, list):
            hints = []
        hints_json = f"'{json.dumps(hints, ensure_ascii=False)}'"
        
        # Titre de l'exercice
        title = f"Exercice {exercise.get('exercise_number', i)}"
        if exercise.get('chapter_title'):
            title += f" - {exercise['chapter_title']}"
        
        sql += f"""INSERT INTO public.exercises (
    id,
    course_id,
    title,
    description,
    question,
    answer,
    explanation,
    difficulty,
    points,
    time_limit,
    type,
    hints,
    options,
    ai_generated,
    order_num,
    is_published
) VALUES (
    uuid_generate_v4(),
    (SELECT id FROM public.courses WHERE order_num = {chapter_num} LIMIT 1),
    {escape_sql_string(title)},
    {escape_sql_string(f"Exercice du chapitre {chapter_num}")},
    {escape_sql_string(exercise.get('body', ''))},
    {escape_sql_string(exercise.get('answer', ''))},
    {escape_sql_string(exercise.get('explanation', ''))},
    '{exercise.get('difficulty', 'moyen')}',
    {10 if exercise.get('difficulty') == 'facile' else 15 if exercise.get('difficulty') == 'moyen' else 20},
    300,
    '{exercise_type}',
    {hints_json},
    {options_json},
    false,
    {i},
    true
);

"""
    
    return sql

def main():
    """Fonction principale"""
    print('=' * 60)
    print('GÉNÉRATEUR DE FICHIERS SQL PETITS - MATHIA')
    print('=' * 60)
    print()
    
    # Charger les exercices par chapitre
    exercises_by_chapter = load_exercises_by_chapter()
    
    if not exercises_by_chapter:
        print("[ERROR] Aucun exercice trouvé!")
        return
    
    # Générer le fichier de schéma
    schema_sql = generate_schema_sql()
    with open("01_schema.sql", 'w', encoding='utf-8') as f:
        f.write(schema_sql)
    print("[OK] Fichier créé: 01_schema.sql")
    
    # Générer le fichier des cours
    courses_sql = generate_courses_sql()
    with open("02_courses.sql", 'w', encoding='utf-8') as f:
        f.write(courses_sql)
    print("[OK] Fichier créé: 02_courses.sql")
    
    # Générer un fichier par chapitre
    for chapter_num in sorted(exercises_by_chapter.keys()):
        exercises = exercises_by_chapter[chapter_num]
        exercises_sql = generate_exercises_sql_for_chapter(chapter_num, exercises)
        
        filename = f"03_chapitre_{chapter_num:02d}.sql"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(exercises_sql)
        
        file_size = len(exercises_sql.encode('utf-8'))
        print(f"[OK] Fichier créé: {filename} ({file_size / (1024*1024):.1f} MB, {len(exercises)} exercices)")
    
    # Créer les instructions
    instructions = """# Instructions d'Import - Fichiers SQL Petits

## Fichiers Créés
Les exercices ont été organisés en fichiers séparés pour éviter les problèmes de taille.

## Ordre d'Exécution dans Supabase SQL Editor

### Étape 1: Schéma de Base
**01_schema.sql** - Exécutez ce fichier EN PREMIER
- Crée les types et tables nécessaires
- Gère les types existants automatiquement

### Étape 2: Cours
**02_courses.sql** - Crée les 9 cours de 6ème

### Étape 3: Exercices par Chapitre
Exécutez les fichiers dans l'ordre :

"""
    
    for chapter_num in sorted(exercises_by_chapter.keys()):
        exercises = exercises_by_chapter[chapter_num]
        filename = f"03_chapitre_{chapter_num:02d}.sql"
        file_size = len(generate_exercises_sql_for_chapter(chapter_num, exercises).encode('utf-8'))
        instructions += f"**{filename}** ({file_size / (1024*1024):.1f} MB, {len(exercises)} exercices)\n"
    
    instructions += """
### Étape 4: Vérification
```sql
-- Vérifier le nombre total d'exercices
SELECT COUNT(*) as total_exercices FROM public.exercises;

-- Vérifier par chapitre
SELECT 
    c.title as chapitre,
    COUNT(e.id) as exercices
FROM public.courses c
LEFT JOIN public.exercises e ON c.id = e.course_id
GROUP BY c.id, c.title
ORDER BY c.order_num;
```

## Avantages de cette Méthode
- ✅ Fichiers petits (pas de problème de taille)
- ✅ Encodage UTF-8 correct
- ✅ Import par chapitre (plus de contrôle)
- ✅ Gestion des erreurs par fichier

## Résultat Attendu
- 9 cours (chapitres 6ème)
- 3 392 exercices importés
- Bibliothèque complète prête à utiliser
"""
    
    with open("INSTRUCTIONS_IMPORT.md", 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"\n[SUCCESS] Instructions créées: INSTRUCTIONS_IMPORT.md")
    print(f"[INFO] Total: {sum(len(exercises) for exercises in exercises_by_chapter.values())} exercices")

if __name__ == '__main__':
    main()


