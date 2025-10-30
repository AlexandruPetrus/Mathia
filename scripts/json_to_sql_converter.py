#!/usr/bin/env python3
"""
Convertisseur simple JSON vers SQL INSERT
Transforme rapidement les fichiers JSON en instructions SQL
"""

import os
import json
import sys
from typing import List, Dict, Any
from datetime import datetime

def escape_sql(text: str) -> str:
    """Échapper le texte pour SQL"""
    if not text:
        return "NULL"
    return f"'{text.replace(chr(39), chr(39)+chr(39))}'"

def convert_json_to_sql_inserts(json_file: str, output_file: str = None) -> str:
    """Convertir un fichier JSON en instructions SQL INSERT"""
    
    if not os.path.exists(json_file):
        print(f"[ERROR] Fichier non trouve: {json_file}")
        return ""
    
    # Charger le JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            exercises = json.load(f)
            if not isinstance(exercises, list):
                exercises = [exercises]
    except Exception as e:
        print(f"[ERROR] Erreur lecture {json_file}: {e}")
        return ""
    
    # Déterminer le chapitre
    chapter_num = 1
    if 'chapitre' in json_file:
        try:
            chapter_num = int(json_file.split('chapitre_')[1].split('.')[0])
        except:
            pass
    
    # Générer le SQL
    sql = f"""-- ============================================
-- EXERCICES {json_file.upper()}
-- ============================================
-- Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- Nombre d'exercices: {len(exercises)}
-- Chapitre: {chapter_num}
-- ============================================

"""
    
    for i, exercise in enumerate(exercises, 1):
        # Données de base
        title = f"Exercice {exercise.get('exercise_number', i)}"
        if exercise.get('chapter_title'):
            title += f" - {exercise['chapter_title']}"
        
        question = exercise.get('body', '')
        answer = exercise.get('answer', '')
        explanation = exercise.get('explanation', '')
        difficulty = exercise.get('difficulty', 'moyen')
        exercise_type = exercise.get('type', 'libre')
        
        # Options pour QCM
        options = exercise.get('options')
        options_sql = "NULL"
        if options and isinstance(options, dict):
            options_sql = f"'{json.dumps(options, ensure_ascii=False)}'"
        
        # Indices
        hints = exercise.get('hints', [])
        if not isinstance(hints, list):
            hints = []
        hints_sql = f"'{json.dumps(hints, ensure_ascii=False)}'"
        
        # Points selon la difficulté
        points = 10 if difficulty == 'facile' else 15 if difficulty == 'moyen' else 20
        
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
    {escape_sql(title)},
    {escape_sql(f"Exercice du chapitre {chapter_num}")},
    {escape_sql(question)},
    {escape_sql(answer)},
    {escape_sql(explanation)},
    '{difficulty}',
    {points},
    300,
    '{exercise_type}',
    {hints_sql},
    {options_sql},
    false,
    {i},
    true
);

"""
    
    # Sauvegarder si demandé
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(sql)
            print(f"[SUCCESS] SQL genere: {output_file}")
        except Exception as e:
            print(f"[ERROR] Erreur sauvegarde: {e}")
    
    return sql

def convert_all_json_files():
    """Convertir tous les fichiers JSON en SQL"""
    
    json_files = [
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
    
    all_sql = f"""-- ============================================
-- BIBLIOTHÈQUE SQL COMPLÈTE - MATHIA
-- ============================================
-- Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- Conversion automatique JSON → SQL
-- ============================================

"""
    
    total_exercises = 0
    
    for json_file in json_files:
        if os.path.exists(json_file):
            print(f"[CONVERT] Conversion de {json_file}...")
            sql = convert_json_to_sql_inserts(json_file)
            if sql:
                all_sql += sql + "\n"
                # Compter les exercices
                with open(json_file, 'r', encoding='utf-8') as f:
                    exercises = json.load(f)
                    if not isinstance(exercises, list):
                        exercises = [exercises]
                    total_exercises += len(exercises)
                    print(f"   [OK] {len(exercises)} exercices convertis")
        else:
            print(f"[WARNING] Fichier non trouve: {json_file}")
    
    # Ajouter les requêtes de vérification
    all_sql += f"""
-- ============================================
-- VÉRIFICATIONS
-- ============================================

-- Total d'exercices importés
SELECT 'Total exercices' as type, COUNT(*) as nombre FROM public.exercises;

-- Par chapitre
SELECT 
    c.title as chapitre,
    COUNT(e.id) as exercices
FROM public.courses c
LEFT JOIN public.exercises e ON c.id = e.course_id
GROUP BY c.id, c.title
ORDER BY c.order_num;

-- Par difficulté
SELECT 
    difficulty,
    COUNT(*) as nombre
FROM public.exercises
GROUP BY difficulty
ORDER BY difficulty;

-- ============================================
-- CONVERSION TERMINÉE !
-- Total: {total_exercises} exercices
-- ============================================
"""
    
    # Sauvegarder le fichier complet
    output_file = "mathia_complete_library.sql"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(all_sql)
        
        print(f"\n[SUCCESS] Bibliotheque SQL complete generee!")
        print(f"[FILE] Fichier: {output_file}")
        print(f"[STATS] Total: {total_exercises} exercices")
        
    except Exception as e:
        print(f"[ERROR] Erreur sauvegarde: {e}")

def main():
    """Fonction principale"""
    print('=' * 50)
    print('CONVERTISSEUR JSON -> SQL - MATHIA')
    print('=' * 50)
    print()
    
    if len(sys.argv) > 1:
        # Conversion d'un fichier spécifique
        json_file = sys.argv[1]
        output_file = json_file.replace('.json', '.sql')
        convert_json_to_sql_inserts(json_file, output_file)
    else:
        # Conversion de tous les fichiers
        convert_all_json_files()
    
    print("\n[INFO] Utilisation:")
    print("1. Executez le schema Supabase: supabase/schema.sql")
    print("2. Copiez-collez le SQL genere dans le SQL Editor")
    print("3. Executez le script")

if __name__ == '__main__':
    main()
