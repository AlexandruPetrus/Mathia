#!/usr/bin/env python3
"""
Import sécurisé des exercices via l'API Supabase
Évite les problèmes de taille de fichier SQL
"""

import os
import sys
import json
import requests
from typing import List, Dict, Any
from datetime import datetime

def get_supabase_config():
    """Récupérer la configuration Supabase depuis .env"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_ANON_KEY')
    
    if not url or not key:
        print("[ERROR] SUPABASE_URL et SUPABASE_ANON_KEY doivent être définis dans .env")
        print("Exemple:")
        print("SUPABASE_URL=https://xxxxxxxx.supabase.co")
        print("SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        return None, None
    
    return url, key

def load_exercises_from_json() -> List[Dict[str, Any]]:
    """Charger tous les exercices depuis les fichiers JSON"""
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
    file_to_chapter = {
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
    
    for filename in exercise_files:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    exercises = json.load(f)
                    if not isinstance(exercises, list):
                        exercises = [exercises]
                    
                    # Ajouter le numéro de chapitre
                    chapter_num = file_to_chapter.get(filename, 1)
                    for exercise in exercises:
                        exercise['_chapter_number'] = chapter_num
                        exercise['_source_file'] = filename
                    
                    all_exercises.extend(exercises)
                    print(f"[OK] {filename}: {len(exercises)} exercices (chapitre {chapter_num})")
                    
            except Exception as e:
                print(f"[ERROR] Erreur {filename}: {e}")
        else:
            print(f"[WARNING] Fichier non trouvé: {filename}")
    
    print(f"\n[STATS] Total: {len(all_exercises)} exercices")
    return all_exercises

def create_courses_via_api(url: str, key: str) -> Dict[int, str]:
    """Créer les cours via l'API Supabase"""
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
    
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
    
    chapter_to_course_id = {}
    
    for chapter_num, title, topic in courses:
        # Vérifier si le cours existe déjà
        response = requests.get(
            f"{url}/rest/v1/courses",
            headers=headers,
            params={"title": f"eq.{title}", "grade": "eq.6ème"}
        )
        
        if response.status_code == 200:
            existing_courses = response.json()
            if existing_courses:
                course_id = existing_courses[0]['id']
                print(f"[OK] Cours existant: {title} (ID: {course_id})")
            else:
                # Créer le nouveau cours
                course_data = {
                    "title": title,
                    "description": f"Chapitre {chapter_num} du manuel de mathématiques 6ème",
                    "content": f"Contenu du chapitre {chapter_num}: {title}",
                    "grade": "6ème",
                    "topic": topic,
                    "difficulty": "moyen",
                    "order_num": chapter_num,
                    "is_published": True
                }
                
                response = requests.post(
                    f"{url}/rest/v1/courses",
                    headers=headers,
                    json=course_data
                )
                
                if response.status_code == 201:
                    course_id = response.json()['id']
                    print(f"[OK] Nouveau cours créé: {title} (ID: {course_id})")
                else:
                    print(f"[ERROR] Erreur création cours {title}: {response.status_code} - {response.text}")
                    continue
        else:
            print(f"[ERROR] Erreur vérification cours {title}: {response.status_code}")
            continue
        
        chapter_to_course_id[chapter_num] = course_id
    
    return chapter_to_course_id

def import_exercises_via_api(exercises: List[Dict[str, Any]], 
                           chapter_to_course_id: Dict[int, str],
                           url: str, key: str):
    """Importer les exercices via l'API Supabase"""
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
    
    total_imported = 0
    total_errors = 0
    
    # Importer par batch de 50 pour éviter les timeouts
    batch_size = 50
    
    for i in range(0, len(exercises), batch_size):
        batch = exercises[i:i + batch_size]
        batch_data = []
        
        for exercise in batch:
            try:
                chapter_num = exercise.get('_chapter_number', 1)
                course_id = chapter_to_course_id.get(chapter_num)
                
                if not course_id:
                    print(f"[WARNING] Pas de cours trouvé pour le chapitre {chapter_num}")
                    total_errors += 1
                    continue
                
                # Préparer les données de l'exercice
                exercise_data = {
                    "course_id": course_id,
                    "title": f"Exercice {exercise.get('exercise_number', 'N/A')} - {exercise.get('chapter_title', '')}",
                    "description": f"Exercice du chapitre {chapter_num}",
                    "question": exercise.get('body', '')[:2000],  # Limiter la longueur
                    "answer": exercise.get('answer', ''),
                    "explanation": exercise.get('explanation', ''),
                    "difficulty": exercise.get('difficulty', 'moyen'),
                    "points": 10 if exercise.get('difficulty') == 'facile' else 15 if exercise.get('difficulty') == 'moyen' else 20,
                    "time_limit": 300,
                    "type": exercise.get('type', 'libre'),
                    "hints": exercise.get('hints', []),
                    "options": exercise.get('options'),
                    "ai_generated": False,
                    "order_num": exercise.get('exercise_number', 1),
                    "is_published": True
                }
                
                batch_data.append(exercise_data)
                
            except Exception as e:
                total_errors += 1
                if total_errors <= 5:
                    print(f"[ERROR] Erreur préparation exercice: {e}")
        
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
                print(f"[OK] Batch importé: {imported_count} exercices (Total: {total_imported})")
            else:
                total_errors += len(batch_data)
                print(f"[ERROR] Erreur batch: {response.status_code} - {response.text}")
    
    print(f"\n[RESULTAT] Import terminé:")
    print(f"  - Exercices importés: {total_imported}")
    print(f"  - Erreurs: {total_errors}")
    if total_imported + total_errors > 0:
        print(f"  - Taux de succès: {(total_imported/(total_imported+total_errors)*100):.1f}%")

def verify_import_via_api(url: str, key: str):
    """Vérifier l'import via l'API"""
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
                print(f"[VERIFICATION] Total d'exercices dans Supabase: {total_exercises}")
            else:
                exercises = response.json()
                print(f"[VERIFICATION] Total d'exercices dans Supabase: {len(exercises)}")
        
        # Statistiques par cours
        response = requests.get(
            f"{url}/rest/v1/courses",
            headers=headers,
            params={"select": "id,title,grade"}
        )
        
        if response.status_code == 200:
            courses = response.json()
            print(f"\n[VERIFICATION] Cours créés: {len(courses)}")
            for course in courses:
                print(f"  - {course['title']} ({course['grade']})")
        
    except Exception as e:
        print(f"[ERROR] Erreur lors de la vérification: {e}")

def main():
    """Fonction principale"""
    print('=' * 60)
    print('IMPORT SÉCURISÉ VIA API - MATHIA')
    print('=' * 60)
    print()
    
    # Récupérer la configuration Supabase
    url, key = get_supabase_config()
    if not url or not key:
        sys.exit(1)
    
    print(f"[INFO] Connexion à Supabase: {url}")
    
    # Charger les exercices
    exercises = load_exercises_from_json()
    if not exercises:
        print("[ERROR] Aucun exercice à importer")
        sys.exit(1)
    
    # Créer les cours
    print("\n[ETAPE 1] Création des cours dans Supabase...")
    chapter_to_course_id = create_courses_via_api(url, key)
    if not chapter_to_course_id:
        print("[ERROR] Impossible de créer les cours")
        sys.exit(1)
    
    # Importer les exercices
    print(f"\n[ETAPE 2] Import de {len(exercises)} exercices dans Supabase...")
    import_exercises_via_api(exercises, chapter_to_course_id, url, key)
    
    # Vérifier l'import
    print("\n[ETAPE 3] Vérification de l'import...")
    verify_import_via_api(url, key)
    
    print(f"\n[SUCCESS] Import terminé avec succès!")

if __name__ == '__main__':
    main()


