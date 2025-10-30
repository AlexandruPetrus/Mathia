#!/usr/bin/env python3
"""
Script pour générer seulement les exercices SQL (sans les cours)
Pour ajouter à un fichier SQL existant
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

def generate_exercises_sql_only(all_exercises: Dict[str, List[Dict[str, Any]]]) -> str:
    """Générer seulement les instructions SQL pour les exercices"""
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
            
            sql += f"""SELECT insert_exercise_if_not_exists(
    {chapter_num},
    {escape_sql_string(title)},
    {escape_sql_string(exercise.get('body', ''))},
    {escape_sql_string(exercise.get('answer', ''))},
    {escape_sql_string(exercise.get('explanation', ''))},
    '{exercise.get('difficulty', 'moyen')}',
    '{exercise_type}',
    {options_json},
    {hints_json},
    {i}
);

"""
            
            total_exercises += 1
    
    sql += f"-- Total d'exercices générés: {total_exercises}\n"
    return sql

def main():
    """Fonction principale"""
    print('=' * 60)
    print('GENERATEUR EXERCICES SEULEMENT - MATHIA')
    print('=' * 60)
    print()
    
    # Charger tous les exercices
    all_exercises = load_all_exercise_files()
    
    if not all_exercises:
        print("Aucun fichier d'exercices trouve!")
        return ""
    
    # Générer le SQL des exercices seulement
    exercises_sql = generate_exercises_sql_only(all_exercises)
    
    # Ajouter la fin du script
    final_sql = exercises_sql + """
-- Réactiver les contraintes
SET session_replication_role = DEFAULT;

-- Supprimer les fonctions temporaires
DROP FUNCTION IF EXISTS insert_course_if_not_exists(TEXT, TEXT, TEXT, grade_level, topic_type, difficulty_level, INTEGER);
DROP FUNCTION IF EXISTS insert_exercise_if_not_exists(INTEGER, TEXT, TEXT, TEXT, TEXT, difficulty_level, exercise_type, JSONB, JSONB, INTEGER);

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
    
    # Sauvegarder dans un fichier
    output_file = "exercices_only.sql"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_sql)
        
        print(f"[SUCCESS] Exercices SQL generes avec succes!")
        print(f"[FILE] Fichier cree: {output_file}")
        print()
        print("[INFO] Ce fichier contient seulement les exercices.")
        print("[INFO] Ajoutez ce contenu a la fin de votre fichier SQL principal.")
        
    except Exception as e:
        print(f"[ERROR] Erreur lors de la sauvegarde: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()


