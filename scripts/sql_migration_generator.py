#!/usr/bin/env python3
"""
Générateur de script de migration SQL pour Supabase
Crée un script SQL optimisé pour l'import avec gestion des doublons
"""

import os
import json
import sys
from typing import List, Dict, Any, Set
from datetime import datetime

def load_exercises_with_deduplication() -> List[Dict[str, Any]]:
    """Charger tous les exercices avec déduplication basée sur le contenu"""
    exercise_files = [
        'exercices_6eme.json',
        'exercices_chapitre_1.json',
        'exercices_chapitre_2.json',
        'exercices_chapitre_3.json',
        'exercices_chapitre_4.json',
        'exercices_chapitre_5.json',
        'exercices_chapitre_6.json',
        'exercices_chapitre_7.json',
        'exercices_chapitre_8.json',
        'exercices_chapitre_9.json'
    ]
    
    all_exercises = []
    seen_content = set()
    duplicates_count = 0
    
    for filename in exercise_files:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    exercises = json.load(f)
                    if not isinstance(exercises, list):
                        exercises = [exercises]
                    
                    for exercise in exercises:
                        # Créer une signature unique basée sur le contenu
                        content_signature = f"{exercise.get('body', '')[:100]}_{exercise.get('answer', '')[:50]}"
                        
                        if content_signature not in seen_content:
                            seen_content.add(content_signature)
                            # Ajouter des métadonnées sur la source
                            exercise['_source_file'] = filename
                            all_exercises.append(exercise)
                        else:
                            duplicates_count += 1
                    
                    print(f"[OK] {filename}: {len(exercises)} exercices (doublons ignores: {duplicates_count})")
                    
            except Exception as e:
                print(f"[ERROR] Erreur {filename}: {e}")
        else:
            print(f"[WARNING] Fichier non trouve: {filename}")
    
    print(f"\n[STATS] Total: {len(all_exercises)} exercices uniques (doublons supprimes: {duplicates_count})")
    return all_exercises

def generate_migration_sql(exercises: List[Dict[str, Any]]) -> str:
    """Générer le script de migration SQL optimisé"""
    
    # Déterminer les chapitres uniques
    chapters = set()
    for exercise in exercises:
        chapter_num = exercise.get('chapter_number', 1)
        chapters.add(chapter_num)
    
    chapters = sorted(list(chapters))
    
    sql = f"""-- ============================================
-- MIGRATION SQL MATHIA - EXERCICES 6ÈME
-- ============================================
-- Script de migration optimisé pour Supabase
-- Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- Exercices uniques: {len(exercises)}
-- Chapitres: {', '.join(map(str, chapters))}
-- ============================================

-- Fonction pour nettoyer et valider les données
CREATE OR REPLACE FUNCTION validate_exercise_data()
RETURNS TRIGGER AS $$
BEGIN
    -- Validation des champs obligatoires
    IF NEW.question IS NULL OR LENGTH(TRIM(NEW.question)) = 0 THEN
        RAISE EXCEPTION 'La question ne peut pas être vide';
    END IF;
    
    IF NEW.answer IS NULL OR LENGTH(TRIM(NEW.answer)) = 0 THEN
        RAISE EXCEPTION 'La réponse ne peut pas être vide';
    END IF;
    
    -- Limiter la longueur des champs
    NEW.question = LEFT(NEW.question, 2000);
    NEW.answer = LEFT(NEW.answer, 1000);
    NEW.explanation = LEFT(COALESCE(NEW.explanation, ''), 1000);
    
    -- Normaliser la difficulté
    IF NEW.difficulty NOT IN ('facile', 'moyen', 'difficile') THEN
        NEW.difficulty = 'moyen';
    END IF;
    
    -- Normaliser le type
    IF NEW.type NOT IN ('qcm', 'libre', 'vrai-faux', 'calcul') THEN
        NEW.type = 'libre';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Créer le trigger de validation
DROP TRIGGER IF EXISTS validate_exercise_data_trigger ON public.exercises;
CREATE TRIGGER validate_exercise_data_trigger
    BEFORE INSERT OR UPDATE ON public.exercises
    FOR EACH ROW
    EXECUTE FUNCTION validate_exercise_data();

-- ============================================
-- CRÉATION DES COURS (avec vérification d'existence)
-- ============================================

"""
    
    # Générer les cours avec UPSERT
    courses_data = [
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
    
    for chapter_num, title, topic in courses_data:
        sql += f"""-- Cours {chapter_num}: {title}
INSERT INTO public.courses (
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
) ON CONFLICT (title, grade) DO UPDATE SET
    description = EXCLUDED.description,
    content = EXCLUDED.content,
    topic = EXCLUDED.topic,
    updated_at = NOW();

"""
    
    sql += """
-- ============================================
-- IMPORT DES EXERCICES (avec gestion des doublons)
-- ============================================

-- Fonction pour insérer un exercice avec vérification de doublon
CREATE OR REPLACE FUNCTION insert_exercise_safe(
    p_course_order INTEGER,
    p_title TEXT,
    p_question TEXT,
    p_answer TEXT,
    p_explanation TEXT DEFAULT NULL,
    p_difficulty TEXT DEFAULT 'moyen',
    p_type TEXT DEFAULT 'libre',
    p_options JSONB DEFAULT NULL,
    p_hints JSONB DEFAULT '[]'::jsonb,
    p_order_num INTEGER DEFAULT 1
) RETURNS UUID AS $$
DECLARE
    course_id UUID;
    exercise_id UUID;
    question_hash TEXT;
BEGIN
    -- Récupérer l'ID du cours
    SELECT id INTO course_id 
    FROM public.courses 
    WHERE order_num = p_course_order 
    LIMIT 1;
    
    IF course_id IS NULL THEN
        RAISE EXCEPTION 'Cours non trouvé pour order_num: %', p_course_order;
    END IF;
    
    -- Créer un hash de la question pour détecter les doublons
    question_hash = MD5(LEFT(p_question, 200));
    
    -- Vérifier si l'exercice existe déjà
    SELECT id INTO exercise_id
    FROM public.exercises
    WHERE course_id = course_id 
    AND MD5(LEFT(question, 200)) = question_hash
    LIMIT 1;
    
    IF exercise_id IS NOT NULL THEN
        -- Mettre à jour l'exercice existant
        UPDATE public.exercises SET
            title = p_title,
            answer = p_answer,
            explanation = p_explanation,
            difficulty = p_difficulty,
            type = p_type,
            options = p_options,
            hints = p_hints,
            updated_at = NOW()
        WHERE id = exercise_id;
        
        RETURN exercise_id;
    ELSE
        -- Insérer le nouvel exercice
        INSERT INTO public.exercises (
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
            course_id,
            p_title,
            'Exercice importé automatiquement',
            p_question,
            p_answer,
            p_explanation,
            p_difficulty,
            CASE p_difficulty 
                WHEN 'facile' THEN 10 
                WHEN 'moyen' THEN 15 
                ELSE 20 
            END,
            300,
            p_type,
            p_hints,
            p_options,
            false,
            p_order_num,
            true
        ) RETURNING id INTO exercise_id;
        
        RETURN exercise_id;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- INSERTION DES EXERCICES
-- ============================================

"""
    
    # Grouper les exercices par chapitre
    exercises_by_chapter = {}
    for exercise in exercises:
        chapter_num = exercise.get('chapter_number', 1)
        if chapter_num not in exercises_by_chapter:
            exercises_by_chapter[chapter_num] = []
        exercises_by_chapter[chapter_num].append(exercise)
    
    # Générer les INSERT pour chaque chapitre
    for chapter_num in sorted(exercises_by_chapter.keys()):
        chapter_exercises = exercises_by_chapter[chapter_num]
        sql += f"-- Chapitre {chapter_num} ({len(chapter_exercises)} exercices)\n"
        
        for i, exercise in enumerate(chapter_exercises, 1):
            # Préparer les données
            title = f"Exercice {exercise.get('exercise_number', i)}"
            if exercise.get('chapter_title'):
                title += f" - {exercise['chapter_title']}"
            
            question = exercise.get('body', '').replace("'", "''")
            answer = exercise.get('answer', '').replace("'", "''")
            explanation = exercise.get('explanation', '').replace("'", "''") if exercise.get('explanation') else 'NULL'
            
            difficulty = exercise.get('difficulty', 'moyen')
            exercise_type = exercise.get('type', 'libre')
            
            # Options pour QCM
            options = exercise.get('options')
            options_json = 'NULL'
            if options and isinstance(options, dict):
                options_json = f"'{json.dumps(options, ensure_ascii=False).replace(chr(39), chr(39)+chr(39))}'"
            
            # Indices
            hints = exercise.get('hints', [])
            if not isinstance(hints, list):
                hints = []
            hints_json = f"'{json.dumps(hints, ensure_ascii=False).replace(chr(39), chr(39)+chr(39))}'"
            
            sql += f"""SELECT insert_exercise_safe(
    {chapter_num},
    '{title.replace(chr(39), chr(39)+chr(39))}',
    '{question}',
    '{answer}',
    {explanation if explanation != 'NULL' else 'NULL'},
    '{difficulty}',
    '{exercise_type}',
    {options_json},
    {hints_json},
    {i}
);

"""
    
    sql += """
-- ============================================
-- NETTOYAGE ET OPTIMISATION
-- ============================================

-- Supprimer la fonction temporaire
DROP FUNCTION IF EXISTS insert_exercise_safe(INTEGER, TEXT, TEXT, TEXT, TEXT, TEXT, TEXT, JSONB, JSONB, INTEGER);

-- Supprimer le trigger de validation
DROP TRIGGER IF EXISTS validate_exercise_data_trigger ON public.exercises;
DROP FUNCTION IF EXISTS validate_exercise_data();

-- Mettre à jour les statistiques
ANALYZE public.courses;
ANALYZE public.exercises;

-- ============================================
-- VÉRIFICATIONS FINALES
-- ============================================

-- Statistiques générales
SELECT 
    'Cours créés' as type,
    COUNT(*) as nombre
FROM public.courses
WHERE grade = '6ème';

SELECT 
    'Exercices importés' as type,
    COUNT(*) as nombre
FROM public.exercises e
JOIN public.courses c ON e.course_id = c.id
WHERE c.grade = '6ème';

-- Répartition par chapitre
SELECT 
    c.title as chapitre,
    c.order_num as numéro,
    COUNT(e.id) as exercices
FROM public.courses c
LEFT JOIN public.exercises e ON c.id = e.course_id
WHERE c.grade = '6ème'
GROUP BY c.id, c.title, c.order_num
ORDER BY c.order_num;

-- Répartition par difficulté
SELECT 
    e.difficulty as difficulté,
    COUNT(*) as nombre
FROM public.exercises e
JOIN public.courses c ON e.course_id = c.id
WHERE c.grade = '6ème'
GROUP BY e.difficulty
ORDER BY 
    CASE e.difficulty 
        WHEN 'facile' THEN 1 
        WHEN 'moyen' THEN 2 
        WHEN 'difficile' THEN 3 
    END;

-- ============================================
-- MIGRATION TERMINÉE AVEC SUCCÈS !
-- ============================================
"""
    
    return sql

def main():
    """Fonction principale"""
    print('=' * 60)
    print('GÉNÉRATEUR DE MIGRATION SQL - MATHIA')
    print('=' * 60)
    print()
    
    # Charger et dédupliquer les exercices
    exercises = load_exercises_with_deduplication()
    
    if not exercises:
        print("❌ Aucun exercice trouvé!")
        sys.exit(1)
    
    # Générer le script de migration
    migration_sql = generate_migration_sql(exercises)
    
    # Sauvegarder
    output_file = "mathia_migration.sql"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(migration_sql)
        
        print(f"[SUCCESS] Script de migration genere avec succes!")
        print(f"[FILE] Fichier cree: {output_file}")
        print()
        print("[INSTRUCTIONS] UTILISATION:")
        print("1. Assurez-vous que le schema Supabase est cree (supabase/schema.sql)")
        print("2. Ouvrez le SQL Editor dans votre projet Supabase")
        print("3. Copiez-collez le contenu du fichier mathia_migration.sql")
        print("4. Executez le script complet")
        print("5. Verifiez les resultats avec les requetes de verification")
        print()
        print("[ADVANTAGES] Avantages de cette migration:")
        print("   - Gestion automatique des doublons")
        print("   - Validation des donnees")
        print("   - Mise a jour des exercices existants")
        print("   - Statistiques detaillees")
        
    except Exception as e:
        print(f"[ERROR] Erreur lors de la sauvegarde: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
