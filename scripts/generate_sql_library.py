#!/usr/bin/env python3
"""
Script pour générer une bibliothèque SQL complète des exercices
Transforme tous les fichiers JSON en instructions SQL INSERT
"""

import os
import json
import sys
from typing import List, Dict, Any
from datetime import datetime

def load_all_exercise_files() -> Dict[str, List[Dict[str, Any]]]:
    """Charger tous les fichiers d'exercices JSON"""
    exercise_files = {
        'exercices_6eme.json': '6ème',
        'exercices_chapitre_1.json': '6ème - Chapitre 1',
        'exercices_chapitre_2.json': '6ème - Chapitre 2',
        'exercices_chapitre_3.json': '6ème - Chapitre 3',
        'exercices_chapitre_4.json': '6ème - Chapitre 4',
        'exercices_chapitre_5.json': '6ème - Chapitre 5',
        'exercices_chapitre_6.json': '6ème - Chapitre 6',
        'exercices_chapitre_7.json': '6ème - Chapitre 7',
        'exercices_chapitre_8.json': '6ème - Chapitre 8',
        'exercices_chapitre_9.json': '6ème - Chapitre 9'
    }
    
    all_exercises = {}
    
    for filename, description in exercise_files.items():
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    exercises = json.load(f)
                    if not isinstance(exercises, list):
                        exercises = [exercises]
                    all_exercises[filename] = exercises
                    print(f"[OK] Charge {len(exercises)} exercices depuis {filename}")
            except Exception as e:
                print(f"[ERREUR] Erreur chargement {filename}: {e}")
        else:
            print(f"[WARNING] Fichier non trouve: {filename}")
    
    return all_exercises

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

def generate_courses_sql() -> str:
    """Générer les instructions SQL pour créer les cours"""
    courses = [
        (1, "Nombres entiers", "Arithmétique", "6ème"),
        (2, "Nombres décimaux", "Arithmétique", "6ème"),
        (3, "Opérations sur les nombres", "Arithmétique", "6ème"),
        (4, "Fractions", "Fractions", "6ème"),
        (5, "Proportionnalité", "Proportionnalité", "6ème"),
        (6, "Géométrie - Droites et angles", "Géométrie", "6ème"),
        (7, "Géométrie - Triangles et quadrilatères", "Géométrie", "6ème"),
        (8, "Périmètres et aires", "Géométrie", "6ème"),
        (9, "Statistiques et probabilités", "Statistiques", "6ème")
    ]
    
    sql = "-- ============================================\n"
    sql += "-- COURS - Insertion des cours de 6ème\n"
    sql += "-- ============================================\n\n"
    
    for chapter_num, title, topic, grade in courses:
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
    {escape_sql_string(title)},
    {escape_sql_string(f"Chapitre {chapter_num} du manuel de mathématiques 6ème")},
    {escape_sql_string(f"Contenu du chapitre {chapter_num}: {title}")},
    '{grade}',
    '{topic}',
    'moyen',
    {chapter_num},
    true
);\n\n"""
    
    return sql

def generate_exercises_sql(all_exercises: Dict[str, List[Dict[str, Any]]]) -> str:
    """Générer les instructions SQL pour tous les exercices"""
    sql = "-- ============================================\n"
    sql += "-- EXERCICES - Insertion de tous les exercices\n"
    sql += "-- ============================================\n\n"
    
    # Mapping des fichiers vers les chapitres
    file_to_chapter = {
        'exercices_6eme.json': 1,  # Par défaut chapitre 1
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
    
    total_exercises = 0
    
    for filename, exercises in all_exercises.items():
        chapter_num = file_to_chapter.get(filename, 1)
        
        sql += f"-- Exercices du fichier: {filename} (Chapitre {chapter_num})\n"
        sql += f"-- Nombre d'exercices: {len(exercises)}\n\n"
        
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
);\n\n"""
            
            total_exercises += 1
    
    sql += f"-- Total d'exercices générés: {total_exercises}\n"
    return sql

def generate_complete_sql_library() -> str:
    """Générer la bibliothèque SQL complète"""
    print("Génération de la bibliothèque SQL complète...")
    
    # Charger tous les exercices
    all_exercises = load_all_exercise_files()
    
    if not all_exercises:
        print("Aucun fichier d'exercices trouvé!")
        return ""
    
    # Générer le SQL
    sql = f"""-- ============================================
-- BIBLIOTHÈQUE SQL MATHIA - EXERCICES 6ÈME
-- ============================================
-- Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- Contient tous les exercices des fichiers JSON
-- 
-- INSTRUCTIONS D'UTILISATION:
-- 1. Exécutez d'abord le schéma: supabase/schema.sql
-- 2. Puis exécutez ce fichier dans le SQL Editor de Supabase
-- 3. Vérifiez les données avec les requêtes de test à la fin
-- ============================================

-- Désactiver les contraintes temporairement pour l'import
SET session_replication_role = replica;

"""
    
    # Ajouter les cours
    sql += generate_courses_sql()
    
    # Ajouter les exercices
    sql += generate_exercises_sql(all_exercises)
    
    # Réactiver les contraintes
    sql += """-- Réactiver les contraintes
SET session_replication_role = DEFAULT;

-- ============================================
-- REQUÊTES DE VÉRIFICATION
-- ============================================

-- Compter les cours créés
SELECT 'Cours créés' as type, COUNT(*) as nombre FROM public.courses;

-- Compter les exercices par cours
SELECT 
    c.title as cours,
    COUNT(e.id) as nombre_exercices
FROM public.courses c
LEFT JOIN public.exercises e ON c.id = e.course_id
GROUP BY c.id, c.title
ORDER BY c.order_num;

-- Compter les exercices par difficulté
SELECT 
    difficulty as difficulté,
    COUNT(*) as nombre
FROM public.exercises
GROUP BY difficulty
ORDER BY 
    CASE difficulty 
        WHEN 'facile' THEN 1 
        WHEN 'moyen' THEN 2 
        WHEN 'difficile' THEN 3 
    END;

-- Compter les exercices par type
SELECT 
    type as type_exercice,
    COUNT(*) as nombre
FROM public.exercises
GROUP BY type
ORDER BY type;

-- Total général
SELECT 'Total exercices' as type, COUNT(*) as nombre FROM public.exercises;

-- ============================================
-- BIBLIOTHÈQUE SQL GÉNÉRÉE AVEC SUCCÈS !
-- ============================================
"""
    
    return sql

def main():
    """Fonction principale"""
    print('=' * 60)
    print('GÉNÉRATEUR DE BIBLIOTHÈQUE SQL - MATHIA')
    print('=' * 60)
    print()
    
    # Générer la bibliothèque SQL
    sql_library = generate_complete_sql_library()
    
    if not sql_library:
        print("Erreur: Impossible de générer la bibliothèque SQL")
        sys.exit(1)
    
    # Sauvegarder dans un fichier
    output_file = "mathia_exercises_library.sql"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sql_library)
        
        print(f"[SUCCESS] Bibliotheque SQL generee avec succes!")
        print(f"[FILE] Fichier cree: {output_file}")
        print()
        print("[INSTRUCTIONS] UTILISATION:")
        print("1. Ouvrez le SQL Editor dans votre projet Supabase")
        print("2. Copiez-collez le contenu du fichier mathia_exercises_library.sql")
        print("3. Executez le script")
        print("4. Verifiez les resultats avec les requetes de test incluses")
        print()
        print("[INFO] Cette bibliotheque contient TOUS vos exercices JSON transformes en SQL!")
        
    except Exception as e:
        print(f"[ERROR] Erreur lors de la sauvegarde: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
