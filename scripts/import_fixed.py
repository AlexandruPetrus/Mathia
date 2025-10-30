#!/usr/bin/env python3
"""
Script pour importer les exercices extraits dans la base de données
Version corrigée pour les problèmes d'encodage
"""

import os
import sys
import json
from typing import List, Dict, Any

try:
    import psycopg2
    from psycopg2.extras import Json
except ImportError:
    print("Erreur: Le module psycopg2 n'est pas installe.")
    print("Installez-le avec: pip install psycopg2-binary")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = lambda: None

# Charger les variables d'environnement
load_dotenv()

def get_db_connection():
    """Creer une connexion a la base de donnees PostgreSQL"""
    try:
        # Utiliser directement la DATABASE_URL
        database_url = "postgresql://postgres:SSampeligreno_22@localhost:5432/mathia"
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print(f"Erreur de connexion a la base de donnees: {e}")
        return None


def create_courses(conn) -> Dict[int, int]:
    """Creer les cours dans la base de donnees"""
    if not conn:
        print("Pas de connexion a la base de donnees")
        return {}
    
    cursor = conn.cursor()
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
            cursor.execute(
                "SELECT id FROM courses WHERE title = %s AND grade = %s",
                (chapter['title'], chapter['grade'])
            )
            existing = cursor.fetchone()
            
            if existing:
                course_id = existing[0]
                print(f"Cours existant trouve: {chapter['title']} (ID: {course_id})")
            else:
                # Creer le nouveau cours
                cursor.execute(
                    """
                    INSERT INTO courses (title, grade, chapter, description, "createdAt", "updatedAt")
                    VALUES (%s, %s, %s, %s, NOW(), NOW())
                    RETURNING id
                    """,
                    (
                        chapter['title'],
                        chapter['grade'],
                        f"Chapitre {chapter['number']}",
                        f"Chapitre {chapter['number']} du manuel de mathematiques 6eme"
                    )
                )
                course_id = cursor.fetchone()[0]
                print(f"Nouveau cours cree: {chapter['title']} (ID: {course_id})")
            
            chapter_to_course_id[chapter['number']] = course_id
        
        conn.commit()
        cursor.close()
        return chapter_to_course_id
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        print(f"Erreur lors de la creation des cours: {e}")
        return {}


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


def import_exercises_to_db(exercises: List[Dict[str, Any]], 
                          chapter_to_course_id: Dict[int, int], 
                          conn):
    """Importer les exercices dans la base de donnees"""
    if not conn:
        print("Pas de connexion a la base de donnees")
        return
    
    cursor = conn.cursor()
    total_imported = 0
    total_errors = 0
    
    try:
        print(f"Import de {len(exercises)} exercices...")
        
        for i, exercise in enumerate(exercises, 1):
            try:
                chapter_num = exercise.get('chapter_number', 1)
                course_id = chapter_to_course_id.get(chapter_num)
                
                if not course_id:
                    print(f"Pas de cours trouve pour le chapitre {chapter_num}")
                    total_errors += 1
                    continue
                
                # Nettoyer le body de l'exercice
                body = exercise.get('body', '')
                if len(body) > 1000:  # Limiter la longueur
                    body = body[:1000] + "..."
                
                cursor.execute(
                    """
                    INSERT INTO exercises 
                    ("courseId", type, body, options, answer, explanation, difficulty, tags, "createdAt", "updatedAt")
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                    RETURNING id
                    """,
                    (
                        course_id,
                        exercise.get('type', 'libre'),
                        body,
                        Json(exercise.get('options')) if exercise.get('options') else None,
                        exercise.get('answer', ''),
                        exercise.get('explanation', ''),
                        exercise.get('difficulty', 'moyen'),
                        Json(exercise.get('tags', []))
                    )
                )
                
                exercise_id = cursor.fetchone()[0]
                total_imported += 1
                
                if total_imported % 100 == 0:
                    print(f"Importe {total_imported} exercices...")
                
            except Exception as e:
                total_errors += 1
                if total_errors <= 5:  # Afficher seulement les 5 premières erreurs
                    print(f"Erreur exercice {i}: {e}")
        
        conn.commit()
        cursor.close()
        
        print(f"\nImport termine:")
        print(f"  - Exercices importes: {total_imported}")
        print(f"  - Erreurs: {total_errors}")
        if total_imported + total_errors > 0:
            print(f"  - Taux de succes: {(total_imported/(total_imported+total_errors)*100):.1f}%")
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        print(f"Erreur lors de l'import: {e}")


def verify_import(conn):
    """Verifier que l'import s'est bien passe"""
    if not conn:
        print("Pas de connexion a la base de donnees")
        return
    
    cursor = conn.cursor()
    
    try:
        # Compter le nombre total d'exercices
        cursor.execute("SELECT COUNT(*) FROM exercises")
        total_exercises = cursor.fetchone()[0]
        
        # Compter par cours
        cursor.execute("""
            SELECT c.title, c.grade, COUNT(e.id) as nb_exercices
            FROM courses c
            LEFT JOIN exercises e ON c.id = e."courseId"
            WHERE c.grade = '6eme'
            GROUP BY c.id, c.title, c.grade
            ORDER BY c.id
        """)
        courses_stats = cursor.fetchall()
        
        # Compter par type
        cursor.execute("""
            SELECT type, COUNT(*) as nb_exercices
            FROM exercises
            GROUP BY type
            ORDER BY nb_exercices DESC
        """)
        type_stats = cursor.fetchall()
        
        # Compter par difficulte
        cursor.execute("""
            SELECT difficulty, COUNT(*) as nb_exercices
            FROM exercises
            GROUP BY difficulty
            ORDER BY nb_exercices DESC
        """)
        difficulty_stats = cursor.fetchall()
        
        cursor.close()
        
        print(f"\nVERIFICATION DE L'IMPORT:")
        print(f"=" * 50)
        print(f"Total d'exercices dans la base: {total_exercises}")
        
        print(f"\nPar cours (6eme):")
        for title, grade, count in courses_stats:
            print(f"  - {title}: {count} exercices")
        
        print(f"\nPar type:")
        for ex_type, count in type_stats:
            print(f"  - {ex_type}: {count} exercices")
        
        print(f"\nPar difficulte:")
        for difficulty, count in difficulty_stats:
            print(f"  - {difficulty}: {count} exercices")
        
    except Exception as e:
        cursor.close()
        print(f"Erreur lors de la verification: {e}")


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Importer les exercices dans la base de donnees')
    parser.add_argument('--file', default='exercices_6eme.json', 
                       help='Fichier JSON contenant les exercices')
    parser.add_argument('--verify-only', action='store_true', 
                       help='Seulement verifier les donnees existantes')
    
    args = parser.parse_args()
    
    print('=' * 60)
    print('Import des exercices dans la base de donnees Mathia')
    print('=' * 60 + '\n')
    
    # Connexion a la base de donnees
    print("Connexion a la base de donnees...")
    conn = get_db_connection()
    if not conn:
        print("Erreur: Impossible de se connecter a la base de donnees")
        sys.exit(1)
    print("Connexion reussie!\n")
    
    if args.verify_only:
        # Seulement verifier
        verify_import(conn)
    else:
        # Charger les exercices
        exercises = load_exercises(args.file)
        if not exercises:
            print("Aucun exercice a importer")
            conn.close()
            sys.exit(1)
        
        # Creer les cours
        print("Creation des cours...")
        chapter_to_course_id = create_courses(conn)
        if not chapter_to_course_id:
            print("Erreur: Impossible de creer les cours")
            conn.close()
            sys.exit(1)
        
        # Importer les exercices
        print("\nImport des exercices...")
        import_exercises_to_db(exercises, chapter_to_course_id, conn)
        
        # Verifier l'import
        print("\nVerification de l'import...")
        verify_import(conn)
    
    conn.close()
    print(f"\nImport termine avec succes!")


if __name__ == '__main__':
    main()

