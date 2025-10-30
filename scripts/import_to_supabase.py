#!/usr/bin/env python3
"""
Script pour importer les exercices dans Supabase
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

def get_supabase_config():
    """Recuperer la configuration Supabase depuis .env"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_ANON_KEY')
    
    if not url or not key:
        print("Erreur: SUPABASE_URL et SUPABASE_ANON_KEY doivent etre definis dans .env")
        print("Exemple:")
        print("SUPABASE_URL=https://xxxxxxxx.supabase.co")
        print("SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        return None, None
    
    return url, key

def create_courses_in_supabase(url: str, key: str) -> Dict[int, str]:
    """Creer les cours dans Supabase"""
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
    
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
    
    chapter_to_course_id = {}
    
    try:
        for course in courses:
            # Verifier si le cours existe deja
            response = requests.get(
                f"{url}/rest/v1/courses",
                headers=headers,
                params={"title": f"eq.{course['title']}", "grade": f"eq.{course['grade']}"}
            )
            
            if response.status_code == 200:
                existing_courses = response.json()
                if existing_courses:
                    course_id = existing_courses[0]['id']
                    print(f"Cours existant trouve: {course['title']} (ID: {course_id})")
                else:
                    # Creer le nouveau cours
                    course_data = {
                        "title": course['title'],
                        "grade": course['grade'],
                        "chapter": f"Chapitre {course['number']}",
                        "description": f"Chapitre {course['number']} du manuel de mathematiques 6eme"
                    }
                    
                    response = requests.post(
                        f"{url}/rest/v1/courses",
                        headers=headers,
                        json=course_data
                    )
                    
                    if response.status_code == 201:
                        course_id = response.json()['id']
                        print(f"Nouveau cours cree: {course['title']} (ID: {course_id})")
                    else:
                        print(f"Erreur creation cours {course['title']}: {response.status_code} - {response.text}")
                        continue
            else:
                print(f"Erreur verification cours {course['title']}: {response.status_code}")
                continue
            
            chapter_to_course_id[course['number']] = course_id
        
        return chapter_to_course_id
        
    except Exception as e:
        print(f"Erreur lors de la creation des cours: {e}")
        return {}

def import_exercises_to_supabase(exercises: List[Dict[str, Any]], 
                                chapter_to_course_id: Dict[int, str],
                                url: str, key: str):
    """Importer les exercices dans Supabase"""
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
    
    total_imported = 0
    total_errors = 0
    
    try:
        print(f"Import de {len(exercises)} exercices dans Supabase...")
        
        # Importer par batch de 100 pour eviter les timeouts
        batch_size = 100
        for i in range(0, len(exercises), batch_size):
            batch = exercises[i:i + batch_size]
            batch_data = []
            
            for exercise in batch:
                try:
                    chapter_num = exercise.get('chapter_number', 1)
                    course_id = chapter_to_course_id.get(chapter_num)
                    
                    if not course_id:
                        print(f"Pas de cours trouve pour le chapitre {chapter_num}")
                        total_errors += 1
                        continue
                    
                    # Preparer les donnees de l'exercice
                    exercise_data = {
                        "course_id": course_id,
                        "type": exercise.get('type', 'libre'),
                        "body": exercise.get('body', '')[:1000],  # Limiter la longueur
                        "answer": exercise.get('answer', ''),
                        "explanation": exercise.get('explanation', ''),
                        "difficulty": exercise.get('difficulty', 'moyen'),
                        "tags": exercise.get('tags', []),
                        "options": exercise.get('options')
                    }
                    
                    batch_data.append(exercise_data)
                    
                except Exception as e:
                    total_errors += 1
                    if total_errors <= 5:
                        print(f"Erreur preparation exercice: {e}")
            
            if batch_data:
                # Envoyer le batch
                response = requests.post(
                    f"{url}/rest/v1/exercises",
                    headers=headers,
                    json=batch_data
                )
                
                if response.status_code == 201:
                    imported_count = len(batch_data)
                    total_imported += imported_count
                    print(f"Batch importe: {imported_count} exercices (Total: {total_imported})")
                else:
                    total_errors += len(batch_data)
                    print(f"Erreur batch: {response.status_code} - {response.text}")
        
        print(f"\nImport termine:")
        print(f"  - Exercices importes: {total_imported}")
        print(f"  - Erreurs: {total_errors}")
        if total_imported + total_errors > 0:
            print(f"  - Taux de succes: {(total_imported/(total_imported+total_errors)*100):.1f}%")
        
    except Exception as e:
        print(f"Erreur lors de l'import: {e}")

def verify_import_in_supabase(url: str, key: str):
    """Verifier l'import dans Supabase"""
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}'
    }
    
    try:
        # Compter le nombre total d'exercices
        response = requests.get(
            f"{url}/rest/v1/exercises",
            headers=headers,
            params={"select": "count"}
        )
        
        if response.status_code == 200:
            # Supabase retourne le count dans les headers
            count_header = response.headers.get('content-range')
            if count_header:
                total_exercises = int(count_header.split('/')[-1])
                print(f"Total d'exercices dans Supabase: {total_exercises}")
            else:
                exercises = response.json()
                print(f"Total d'exercices dans Supabase: {len(exercises)}")
        
        # Statistiques par cours
        response = requests.get(
            f"{url}/rest/v1/courses",
            headers=headers,
            params={"select": "id,title,grade"}
        )
        
        if response.status_code == 200:
            courses = response.json()
            print(f"\nCours crees: {len(courses)}")
            for course in courses:
                print(f"  - {course['title']} ({course['grade']})")
        
    except Exception as e:
        print(f"Erreur lors de la verification: {e}")

def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Importer les exercices dans Supabase')
    parser.add_argument('--file', default='exercices_6eme.json', 
                       help='Fichier JSON contenant les exercices')
    parser.add_argument('--verify-only', action='store_true', 
                       help='Seulement verifier les donnees existantes')
    
    args = parser.parse_args()
    
    print('=' * 60)
    print('Import des exercices dans Supabase')
    print('=' * 60 + '\n')
    
    # Recuperer la configuration Supabase
    url, key = get_supabase_config()
    if not url or not key:
        sys.exit(1)
    
    print(f"Connexion a Supabase: {url}")
    
    if args.verify_only:
        # Seulement verifier
        verify_import_in_supabase(url, key)
    else:
        # Charger les exercices
        exercises = load_exercises(args.file)
        if not exercises:
            print("Aucun exercice a importer")
            sys.exit(1)
        
        # Creer les cours
        print("Creation des cours dans Supabase...")
        chapter_to_course_id = create_courses_in_supabase(url, key)
        if not chapter_to_course_id:
            print("Erreur: Impossible de creer les cours")
            sys.exit(1)
        
        # Importer les exercices
        print("\nImport des exercices dans Supabase...")
        import_exercises_to_supabase(exercises, chapter_to_course_id, url, key)
        
        # Verifier l'import
        print("\nVerification de l'import...")
        verify_import_in_supabase(url, key)
    
    print(f"\nImport termine avec succes!")

if __name__ == '__main__':
    main()

