#!/usr/bin/env python3
"""
Script d'import simple pour les exercices
"""

import os
import sys
import json
import psycopg2
from psycopg2.extras import Json

def get_db_connection():
    """Creer une connexion a la base de donnees"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="mathia",
            user="postgres",
            password="SSampeligreno_22"
        )
        return conn
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        return None

def create_course(conn, course_id, title, grade, chapter, description):
    """Creer un cours"""
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO courses (id, title, grade, chapter, description, "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            ON CONFLICT (id) DO NOTHING
            """,
            (course_id, title, grade, chapter, description)
        )
        conn.commit()
        print(f"Cours cree: {title} (ID: {course_id})")
    except Exception as e:
        print(f"Erreur creation cours {title}: {e}")
    finally:
        cursor.close()

def import_exercises(conn, exercises, course_id):
    """Importer les exercices"""
    cursor = conn.cursor()
    imported = 0
    errors = 0
    
    try:
        for exercise in exercises:
            try:
                cursor.execute(
                    """
                    INSERT INTO exercises 
                    ("courseId", type, body, options, answer, explanation, difficulty, tags, "createdAt", "updatedAt")
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                    """,
                    (
                        course_id,
                        exercise.get('type', 'libre'),
                        exercise.get('body', '')[:1000],
                        Json(exercise.get('options')) if exercise.get('options') else None,
                        exercise.get('answer', ''),
                        exercise.get('explanation', ''),
                        exercise.get('difficulty', 'moyen'),
                        Json(exercise.get('tags', []))
                    )
                )
                imported += 1
                if imported % 50 == 0:
                    print(f"Importe {imported} exercices...")
            except Exception as e:
                errors += 1
                if errors <= 3:
                    print(f"Erreur: {e}")
        
        conn.commit()
        print(f"Import termine: {imported} importes, {errors} erreurs")
        
    except Exception as e:
        conn.rollback()
        print(f"Erreur import: {e}")
    finally:
        cursor.close()

def main():
    # Creer les cours
    conn = get_db_connection()
    if not conn:
        return
    
    courses = [
        (1, "Nombres entiers", "6eme", "Chapitre 1", "Chapitre 1 du manuel de mathematiques 6eme"),
        (2, "Nombres decimaux", "6eme", "Chapitre 2", "Chapitre 2 du manuel de mathematiques 6eme"),
        (3, "Operations sur les nombres", "6eme", "Chapitre 3", "Chapitre 3 du manuel de mathematiques 6eme"),
        (4, "Fractions", "6eme", "Chapitre 4", "Chapitre 4 du manuel de mathematiques 6eme"),
        (5, "Proportionnalite", "6eme", "Chapitre 5", "Chapitre 5 du manuel de mathematiques 6eme"),
        (6, "Geometrie - Droites et angles", "6eme", "Chapitre 6", "Chapitre 6 du manuel de mathematiques 6eme"),
        (7, "Geometrie - Triangles et quadrilateres", "6eme", "Chapitre 7", "Chapitre 7 du manuel de mathematiques 6eme"),
        (8, "Perimetres et aires", "6eme", "Chapitre 8", "Chapitre 8 du manuel de mathematiques 6eme"),
        (9, "Statistiques et probabilites", "6eme", "Chapitre 9", "Chapitre 9 du manuel de mathematiques 6eme")
    ]
    
    print("Creation des cours...")
    for course_id, title, grade, chapter, description in courses:
        create_course(conn, course_id, title, grade, chapter, description)
    
    # Importer les exercices par chapitre
    for chapter_num in range(1, 10):
        filename = f"exercices_chapitre_{chapter_num}.json"
        if os.path.exists(filename):
            print(f"\nImport du chapitre {chapter_num}...")
            with open(filename, 'r', encoding='utf-8') as f:
                exercises = json.load(f)
            import_exercises(conn, exercises, chapter_num)
    
    conn.close()
    print("\nImport termine avec succes!")

if __name__ == '__main__':
    main()

