#!/usr/bin/env python3
"""
Script final pour importer les exercices
Utilise l'interface d'administration de l'application
"""

import os
import sys
import json
import requests
import time
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

def wait_for_server(base_url: str = "http://localhost:3000", max_attempts: int = 30):
    """Attendre que le serveur soit disponible"""
    print("Attente du serveur...")
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{base_url}/api/courses", timeout=5)
            if response.status_code == 200:
                print("Serveur disponible!")
                return True
        except:
            pass
        print(f"Tentative {attempt + 1}/{max_attempts}...")
        time.sleep(2)
    
    print("Serveur non disponible apres 60 secondes")
    return False

def create_courses_via_api(base_url: str = "http://localhost:3000") -> Dict[int, int]:
    """Creer les cours via l'API"""
    chapter_to_course_id = {}
    
    courses = [
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
        for course in courses:
            # Creer le cours
            course_data = {
                "title": course['title'],
                "grade": course['grade'],
                "chapter": f"Chapitre {course['number']}",
                "description": f"Chapitre {course['number']} du manuel de mathematiques 6eme"
            }
            
            response = requests.post(f"{base_url}/api/courses", json=course_data)
            if response.status_code == 201:
                data = response.json()
                if data.get('success'):
                    course_id = data['data']['course']['id']
                    chapter_to_course_id[course['number']] = course_id
                    print(f"Cours cree: {course['title']} (ID: {course_id})")
                else:
                    print(f"Erreur creation cours {course['title']}: {data.get('message')}")
            else:
                print(f"Erreur HTTP creation cours {course['title']}: {response.status_code}")
        
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

def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import final des exercices')
    parser.add_argument('--file', default='exercices_6eme.json', 
                       help='Fichier JSON contenant les exercices')
    parser.add_argument('--url', default='http://localhost:3000', 
                       help='URL de l\'API')
    
    args = parser.parse_args()
    
    print('=' * 60)
    print('Import final des exercices dans Mathia')
    print('=' * 60 + '\n')
    
    # Attendre que le serveur soit disponible
    if not wait_for_server(args.url):
        print("Impossible de se connecter au serveur")
        sys.exit(1)
    
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
    
    print(f"\nImport termine avec succes!")

if __name__ == '__main__':
    main()

