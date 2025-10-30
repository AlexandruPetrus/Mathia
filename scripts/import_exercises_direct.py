#!/usr/bin/env python3
"""
Script pour importer les exercices directement dans la base de données
Utilise le script d'import existant de l'application
"""

import os
import sys
import json
import subprocess
from typing import List, Dict, Any

def load_exercises(file_path: str) -> List[Dict[str, Any]]:
    """Charger les exercices depuis le fichier JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            exercises = json.load(f)
        
        if not isinstance(exercises, list):
            exercises = [exercises]
        
        print(f"Chargement de {len(exercises)} exercices depuis {file_path}")
        return exercises
    except FileNotFoundError:
        print(f"Fichier non trouve: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Erreur de parsing JSON: {e}")
        return []


def create_courses_json():
    """Creer un fichier JSON avec les cours"""
    courses = [
        {
            "id": 1,
            "title": "Nombres entiers",
            "grade": "6eme",
            "chapter": "Chapitre 1",
            "description": "Chapitre 1 du manuel de mathematiques 6eme"
        },
        {
            "id": 2,
            "title": "Nombres decimaux",
            "grade": "6eme",
            "chapter": "Chapitre 2",
            "description": "Chapitre 2 du manuel de mathematiques 6eme"
        },
        {
            "id": 3,
            "title": "Operations sur les nombres",
            "grade": "6eme",
            "chapter": "Chapitre 3",
            "description": "Chapitre 3 du manuel de mathematiques 6eme"
        },
        {
            "id": 4,
            "title": "Fractions",
            "grade": "6eme",
            "chapter": "Chapitre 4",
            "description": "Chapitre 4 du manuel de mathematiques 6eme"
        },
        {
            "id": 5,
            "title": "Proportionnalite",
            "grade": "6eme",
            "chapter": "Chapitre 5",
            "description": "Chapitre 5 du manuel de mathematiques 6eme"
        },
        {
            "id": 6,
            "title": "Geometrie - Droites et angles",
            "grade": "6eme",
            "chapter": "Chapitre 6",
            "description": "Chapitre 6 du manuel de mathematiques 6eme"
        },
        {
            "id": 7,
            "title": "Geometrie - Triangles et quadrilateres",
            "grade": "6eme",
            "chapter": "Chapitre 7",
            "description": "Chapitre 7 du manuel de mathematiques 6eme"
        },
        {
            "id": 8,
            "title": "Perimetres et aires",
            "grade": "6eme",
            "chapter": "Chapitre 8",
            "description": "Chapitre 8 du manuel de mathematiques 6eme"
        },
        {
            "id": 9,
            "title": "Statistiques et probabilites",
            "grade": "6eme",
            "chapter": "Chapitre 9",
            "description": "Chapitre 9 du manuel de mathematiques 6eme"
        }
    ]
    
    with open('cours_6eme.json', 'w', encoding='utf-8') as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)
    
    print("Fichier cours_6eme.json cree")
    return courses


def split_exercises_by_chapter(exercises: List[Dict[str, Any]]) -> Dict[int, List[Dict[str, Any]]]:
    """Diviser les exercices par chapitre"""
    exercises_by_chapter = {}
    
    for exercise in exercises:
        chapter_num = exercise.get('chapter_number', 1)
        if chapter_num not in exercises_by_chapter:
            exercises_by_chapter[chapter_num] = []
        exercises_by_chapter[chapter_num].append(exercise)
    
    return exercises_by_chapter


def create_chapter_files(exercises_by_chapter: Dict[int, List[Dict[str, Any]]]):
    """Creer des fichiers JSON par chapitre"""
    for chapter_num, chapter_exercises in exercises_by_chapter.items():
        filename = f"exercices_chapitre_{chapter_num}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chapter_exercises, f, ensure_ascii=False, indent=2)
        print(f"Fichier {filename} cree avec {len(chapter_exercises)} exercices")


def import_via_existing_script():
    """Importer via le script existant de l'application"""
    try:
        # Essayer d'importer chaque chapitre
        for chapter_num in range(1, 10):
            filename = f"exercices_chapitre_{chapter_num}.json"
            if os.path.exists(filename):
                print(f"Import du chapitre {chapter_num}...")
                result = subprocess.run([
                    'python', 'scripts/import_exercises.py',
                    '--file', filename,
                    '--course-id', str(chapter_num)
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"Chapitre {chapter_num} importe avec succes")
                else:
                    print(f"Erreur import chapitre {chapter_num}: {result.stderr}")
        
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'import: {e}")
        return False


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Importer les exercices directement')
    parser.add_argument('--file', default='exercices_6eme.json', 
                       help='Fichier JSON contenant les exercices')
    
    args = parser.parse_args()
    
    print('=' * 60)
    print('Import direct des exercices dans Mathia')
    print('=' * 60 + '\n')
    
    # Charger les exercices
    exercises = load_exercises(args.file)
    if not exercises:
        print("Aucun exercice a importer")
        sys.exit(1)
    
    # Creer les cours
    print("Creation des cours...")
    courses = create_courses_json()
    
    # Diviser les exercices par chapitre
    print("Division des exercices par chapitre...")
    exercises_by_chapter = split_exercises_by_chapter(exercises)
    
    # Creer les fichiers par chapitre
    print("Creation des fichiers par chapitre...")
    create_chapter_files(exercises_by_chapter)
    
    # Afficher les statistiques
    print(f"\nSTATISTIQUES:")
    print(f"Total d'exercices: {len(exercises)}")
    for chapter_num, chapter_exercises in exercises_by_chapter.items():
        chapter_title = next((c['title'] for c in courses if c['id'] == chapter_num), f"Chapitre {chapter_num}")
        print(f"  - {chapter_title}: {len(chapter_exercises)} exercices")
    
    print(f"\nFichiers crees:")
    print(f"  - cours_6eme.json (cours)")
    for chapter_num in exercises_by_chapter.keys():
        print(f"  - exercices_chapitre_{chapter_num}.json")
    
    print(f"\nPour importer dans la base de donnees, utilisez:")
    print(f"python scripts/import_exercises.py --file exercices_chapitre_X.json --course-id X")
    
    print(f"\nOu importez tous les chapitres d'un coup:")
    for chapter_num in exercises_by_chapter.keys():
        print(f"python scripts/import_exercises.py --file exercices_chapitre_{chapter_num}.json --course-id {chapter_num}")


if __name__ == '__main__':
    main()

