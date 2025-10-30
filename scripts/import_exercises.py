#!/usr/bin/env python3
"""
Script d'import des exercices générés vers la base de données
Pour Mathia - Application de révision de mathématiques

Usage:
    python scripts/import_exercises.py --file backend/data/generated_exercises.json --course-id 1
"""

import os
import sys
import json
import argparse

try:
    import psycopg2
    from psycopg2.extras import Json
except ImportError:
    print("❌ Le module psycopg2 n'est pas installé.")
    print("📦 Installez-le avec: pip install psycopg2-binary")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("⚠️  Le module python-dotenv n'est pas installé.")
    load_dotenv = lambda: None

# Charger les variables d'environnement
load_dotenv()

# Configuration de la base de données
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', 5432),
    'database': os.getenv('DB_NAME', 'mathia_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}


def get_db_connection():
    """Créer une connexion à la base de données PostgreSQL"""
    try:
        # Essayer d'abord avec DATABASE_URL si disponible
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            conn = psycopg2.connect(database_url)
        else:
            conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        sys.exit(1)


def load_exercises(file_path):
    """Charger les exercices depuis le fichier JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            exercises = json.load(f)
        
        if not isinstance(exercises, list):
            print("⚠️  Le fichier ne contient pas un tableau, encapsulation...")
            exercises = [exercises]
        
        print(f"✅ {len(exercises)} exercices chargés depuis {file_path}\n")
        return exercises
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de parsing JSON: {e}")
        sys.exit(1)


def verify_course_exists(conn, course_id):
    """Vérifier que le cours existe"""
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM courses WHERE id = %s', (course_id,))
    result = cursor.fetchone()
    cursor.close()
    
    if result:
        print(f"✅ Cours trouvé: [{result[0]}] {result[1]}\n")
        return True
    else:
        print(f"❌ Cours avec l'ID {course_id} non trouvé")
        return False


def import_exercise(conn, exercise, course_id):
    """Importer un exercice dans la base de données"""
    cursor = conn.cursor()
    
    try:
        # Convertir les options en JSON si c'est une liste
        options = exercise.get('options')
        if isinstance(options, list):
            # Convertir la liste en dict avec des clés A, B, C, D...
            options = {chr(65 + i): opt for i, opt in enumerate(options)}
        
        # Préparer les tags
        tags = exercise.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        
        cursor.execute(
            """
            INSERT INTO exercises 
            ("courseId", type, body, options, answer, explanation, difficulty, tags, "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            RETURNING id
            """,
            (
                course_id,
                exercise.get('type', 'qcm'),
                exercise.get('body', ''),
                Json(options) if options else None,
                exercise.get('answer', ''),
                exercise.get('explanation', ''),
                exercise.get('difficulty', 'moyen'),
                Json(tags) if tags else None
            )
        )
        
        exercise_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        
        return exercise_id
    except Exception as e:
        conn.rollback()
        cursor.close()
        raise e


def import_all_exercises(conn, exercises, course_id):
    """Importer tous les exercices"""
    success_count = 0
    error_count = 0
    
    print("📥 Import des exercices en cours...\n")
    
    for i, exercise in enumerate(exercises, 1):
        try:
            exercise_id = import_exercise(conn, exercise, course_id)
            print(f"✅ [{i}/{len(exercises)}] Exercice importé (ID: {exercise_id})")
            print(f"   📝 {exercise.get('body', 'N/A')[:60]}...")
            success_count += 1
        except Exception as e:
            print(f"❌ [{i}/{len(exercises)}] Erreur: {e}")
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Import terminé: {success_count} succès, {error_count} erreurs")
    print(f"{'='*60}\n")
    
    return success_count, error_count


def main():
    parser = argparse.ArgumentParser(
        description='Importer des exercices JSON dans la base de données',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:

  # Importer les exercices générés vers le cours ID 1
  python scripts/import_exercises.py --file backend/data/generated_exercises.json --course-id 1

  # Importer depuis un autre fichier
  python scripts/import_exercises.py --file my_exercises.json --course-id 2
        """
    )
    
    parser.add_argument(
        '--file',
        type=str,
        required=True,
        help='Fichier JSON contenant les exercices'
    )
    
    parser.add_argument(
        '--course-id',
        type=int,
        required=True,
        help='ID du cours auquel associer les exercices'
    )
    
    args = parser.parse_args()
    
    print('📥 ' + '='*58)
    print('📚 Import d\'exercices dans la base de données Mathia')
    print('📥 ' + '='*58 + '\n')
    
    # Charger les exercices
    exercises = load_exercises(args.file)
    
    # Connexion à la base de données
    print("🔌 Connexion à la base de données...")
    conn = get_db_connection()
    print("✅ Connecté à PostgreSQL\n")
    
    # Vérifier que le cours existe
    if not verify_course_exists(conn, args.course_id):
        conn.close()
        sys.exit(1)
    
    # Importer les exercices
    success, errors = import_all_exercises(conn, exercises, args.course_id)
    
    # Fermer la connexion
    conn.close()
    
    if errors > 0:
        print(f"⚠️  {errors} exercice(s) n'ont pas pu être importés")
        sys.exit(1)
    else:
        print("🎉 Tous les exercices ont été importés avec succès!")


if __name__ == '__main__':
    main()









