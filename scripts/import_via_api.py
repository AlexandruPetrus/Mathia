#!/usr/bin/env python3
"""
Script pour importer les exercices via l'API de l'application
"""

import os
import sys
import json
import requests
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


def create_courses_via_api(base_url: str = "http://localhost:3000") -> Dict[int, int]:
    """Creer les cours via l'API"""
    chapter_to_course_id = {}
    
    # Chapitres de 6eme
    chapters = [
        {"number": 1, "title": "Nombres entiers", "grade": "6eme"},
        {"number": 2, "title": "Nombres decimaux", "grade": "6eme"},
        {"number": 3, "title": "Operations sur les nombres", "grade": "6eme"},
        {"number": 4, "title": "Fractions", "grade": "6eme"},
        {"number": 5, "title": "Proportionnalite", "grade": "6eme"},
        {"number": 6, "title": "Geometrie - Droites et angles", "grade": "6eme"},
        {"number": 7, "title": "Geometrie - Triangles et quadrilateres", "grade": "6eme"},
        {"number": 8, "title": "Perimetres et aires", "grade": "6eme"},
        {"number": 9, "title": "Statistiques et probabilites", "grade": "6eme"}
    ]
    
    try:
        for chapter in chapters:
            # Verifier si le cours existe deja
            response = requests.get(f"{base_url}/api/courses", params={
                "search": chapter['title'],
                "grade": chapter['grade']
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data', {}).get('courses'):
                    # Cours existe deja
                    course = data['data']['courses'][0]
                    course_id = course['id']
                    print(f"Cours existant trouve: {chapter['title']} (ID: {course_id})")
                else:
                    # Creer le nouveau cours
                    course_data = {
                        "title": chapter['title'],
                        "grade": chapter['grade'],
                        "chapter": f"Chapitre {chapter['number']}",
                        "description": f"Chapitre {chapter['number']} du manuel de mathematiques 6eme"
                    }
                    
                    response = requests.post(f"{base_url}/api/courses", json=course_data)
                    if response.status_code == 201:
                        data = response.json()
                        if data.get('success'):
                            course_id = data['data']['course']['id']
                            print(f"Nouveau cours cree: {chapter['title']} (ID: {course_id})")
                        else:
                            print(f"Erreur creation cours {chapter['title']}: {data.get('message')}")
                            continue
                    else:
                        print(f"Erreur HTTP creation cours {chapter['title']}: {response.status_code}")
                        continue
            else:
                print(f"Erreur HTTP verification cours {chapter['title']}: {response.status_code}")
                continue
            
            chapter_to_course_id[chapter['number']] = course_id
        
        return chapter_to_course_id
        
    except Exception as e:
        print(f"Erreur lors de la creation des cours: {e}")
        return {}


def import_exercises_via_api(exercises: List[Dict[str, Any]], 
                           chapter_to_course_id: Dict[int, int],
                           base_url: str = "http://localhost:3000"):
    """Importer les exercices via l'API"""
    total_imported = 0
    total_errors = 0
    
    try:
        print(f"Import de {len(exercises)} exercices via l'API...")
        
        for i, exercise in enumerate(exercises, 1):
            try:
                chapter_num = exercise.get('chapter_number', 1)
                course_id = chapter_to_course_id.get(chapter_num)
                
                if not course_id:
                    print(f"Pas de cours trouve pour le chapitre {chapter_num}")
                    total_errors += 1
                    continue
                
                # Preparer les donnees de l'exercice
                exercise_data = {
                    "courseId": course_id,
                    "type": exercise.get('type', 'libre'),
                    "body": exercise.get('body', '')[:1000],  # Limiter la longueur
                    "answer": exercise.get('answer', ''),
                    "explanation": exercise.get('explanation', ''),
                    "difficulty": exercise.get('difficulty', 'moyen'),
                    "tags": json.dumps(exercise.get('tags', [])),
                    "options": json.dumps(exercise.get('options')) if exercise.get('options') else None
                }
                
                response = requests.post(f"{base_url}/api/exercises", json=exercise_data)
                
                if response.status_code == 201:
                    total_imported += 1
                    if total_imported % 50 == 0:
                        print(f"Importe {total_imported} exercices...")
                else:
                    total_errors += 1
                    if total_errors <= 5:
                        print(f"Erreur exercice {i}: HTTP {response.status_code}")
                
            except Exception as e:
                total_errors += 1
                if total_errors <= 5:
                    print(f"Erreur exercice {i}: {e}")
        
        print(f"\nImport termine:")
        print(f"  - Exercices importes: {total_imported}")
        print(f"  - Erreurs: {total_errors}")
        if total_imported + total_errors > 0:
            print(f"  - Taux de succes: {(total_imported/(total_imported+total_errors)*100):.1f}%")
        
    except Exception as e:
        print(f"Erreur lors de l'import: {e}")


def verify_import_via_api(base_url: str = "http://localhost:3000"):
    """Verifier l'import via l'API"""
    try:
        # Compter le nombre total d'exercices
        response = requests.get(f"{base_url}/api/exercises")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                exercises = data.get('data', {}).get('exercises', [])
                total_exercises = len(exercises)
                print(f"Total d'exercices dans la base: {total_exercices}")
                
                # Statistiques par type
                type_stats = {}
                for exercise in exercises:
                    ex_type = exercise.get('type', 'unknown')
                    type_stats[ex_type] = type_stats.get(ex_type, 0) + 1
                
                print(f"\nPar type:")
                for ex_type, count in sorted(type_stats.items(), key=lambda x: x[1], reverse=True):
                    print(f"  - {ex_type}: {count} exercices")
                
                # Statistiques par difficulte
                difficulty_stats = {}
                for exercise in exercises:
                    difficulty = exercise.get('difficulty', 'unknown')
                    difficulty_stats[difficulty] = difficulty_stats.get(difficulty, 0) + 1
                
                print(f"\nPar difficulte:")
                for difficulty, count in sorted(difficulty_stats.items(), key=lambda x: x[1], reverse=True):
                    print(f"  - {difficulty}: {count} exercices")
            else:
                print(f"Erreur API: {data.get('message')}")
        else:
            print(f"Erreur HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"Erreur lors de la verification: {e}")


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Importer les exercices via l\'API')
    parser.add_argument('--file', default='exercices_6eme.json', 
                       help='Fichier JSON contenant les exercices')
    parser.add_argument('--url', default='http://localhost:3000', 
                       help='URL de l\'API')
    parser.add_argument('--verify-only', action='store_true', 
                       help='Seulement verifier les donnees existantes')
    
    args = parser.parse_args()
    
    print('=' * 60)
    print('Import des exercices via l\'API Mathia')
    print('=' * 60 + '\n')
    
    if args.verify_only:
        # Seulement verifier
        verify_import_via_api(args.url)
    else:
        # Charger les exercices
        exercises = load_exercises(args.file)
        if not exercises:
            print("Aucun exercice a importer")
            sys.exit(1)
        
        # Creer les cours
        print("Creation des cours via l'API...")
        chapter_to_course_id = create_courses_via_api(args.url)
        if not chapter_to_course_id:
            print("Erreur: Impossible de creer les cours")
            sys.exit(1)
        
        # Importer les exercices
        print("\nImport des exercices via l'API...")
        import_exercises_via_api(exercises, chapter_to_course_id, args.url)
        
        # Verifier l'import
        print("\nVerification de l'import...")
        verify_import_via_api(args.url)
    
    print(f"\nImport termine avec succes!")


if __name__ == '__main__':
    main()

