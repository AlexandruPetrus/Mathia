#!/usr/bin/env python3
"""
Script d'import d'exercices depuis des PDFs vers la base de données
Pour Mathia - Application de révision de mathématiques

Usage:
    python scripts/pdf_exercise_importer.py --pdf path/to/exercises.pdf --course-id 1
    python scripts/pdf_exercise_importer.py --pdf path/to/exercises.pdf --course-id 1 --auto-format
"""

import os
import sys
import json
import argparse
import re
from typing import List, Dict, Any, Optional

try:
    import psycopg2
    from psycopg2.extras import Json
except ImportError:
    print("❌ Le module psycopg2 n'est pas installé.")
    print("📦 Installez-le avec: pip install psycopg2-binary")
    sys.exit(1)

try:
    import PyPDF2
    import pdfplumber
except ImportError:
    print("❌ Les modules PDF ne sont pas installés.")
    print("📦 Installez-les avec: pip install PyPDF2 pdfplumber")
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


class PDFExerciseExtractor:
    """Extracteur d'exercices depuis des PDFs"""
    
    def __init__(self):
        self.exercises = []
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extraire le texte d'un PDF"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text
        except Exception as e:
            print(f"❌ Erreur lors de l'extraction du PDF: {e}")
            return ""
    
    def parse_exercises_from_text(self, text: str, auto_format: bool = False) -> List[Dict[str, Any]]:
        """Parser les exercices depuis le texte extrait"""
        exercises = []
        
        if auto_format:
            exercises = self._auto_parse_exercises(text)
        else:
            exercises = self._manual_parse_exercises(text)
        
        return exercises
    
    def _auto_parse_exercises(self, text: str) -> List[Dict[str, Any]]:
        """Parsing automatique des exercices"""
        exercises = []
        
        # Patterns pour détecter les exercices
        exercise_patterns = [
            r'Exercice\s+(\d+)[:.]?\s*(.*?)(?=Exercice\s+\d+|$)',
            r'(\d+)[:.]\s*(.*?)(?=\d+[:.]|$)',
            r'Question\s+(\d+)[:.]?\s*(.*?)(?=Question\s+\d+|$)'
        ]
        
        for pattern in exercise_patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                exercise_num = match.group(1)
                content = match.group(2).strip()
                
                if len(content) > 20:  # Filtrer les contenus trop courts
                    exercise = self._format_exercise(content, exercise_num)
                    if exercise:
                        exercises.append(exercise)
        
        return exercises
    
    def _manual_parse_exercises(self, text: str) -> List[Dict[str, Any]]:
        """Parsing manuel - demande à l'utilisateur de formater"""
        print("\n📝 Parsing manuel des exercices")
        print("=" * 50)
        print("Le texte extrait du PDF sera affiché ci-dessous.")
        print("Vous devrez créer un fichier JSON avec les exercices formatés.")
        print("=" * 50)
        
        # Afficher le texte extrait
        print("\n📄 Texte extrait du PDF:")
        print("-" * 30)
        print(text[:2000] + "..." if len(text) > 2000 else text)
        print("-" * 30)
        
        # Demander le chemin du fichier JSON
        json_path = input("\n📁 Entrez le chemin vers le fichier JSON formaté (ou 'skip' pour ignorer): ").strip()
        
        if json_path.lower() == 'skip':
            return []
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                exercises = json.load(f)
            return exercises if isinstance(exercises, list) else [exercises]
        except Exception as e:
            print(f"❌ Erreur lors du chargement du fichier JSON: {e}")
            return []
    
    def _format_exercise(self, content: str, exercise_num: str) -> Optional[Dict[str, Any]]:
        """Formater un exercice automatiquement"""
        # Nettoyer le contenu
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Détecter le type d'exercice
        exercise_type = self._detect_exercise_type(content)
        
        # Extraire la question et la réponse
        question, answer, explanation = self._extract_qa(content)
        
        if not question or not answer:
            return None
        
        return {
            'type': exercise_type,
            'body': question,
            'answer': answer,
            'explanation': explanation,
            'difficulty': 'moyen',  # Par défaut
            'tags': ['imported', f'exercice_{exercise_num}'],
            'options': self._extract_options(content) if exercise_type == 'qcm' else None
        }
    
    def _detect_exercise_type(self, content: str) -> str:
        """Détecter le type d'exercice"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['a)', 'b)', 'c)', 'd)', 'choisir', 'sélectionner']):
            return 'qcm'
        elif any(word in content_lower for word in ['vrai', 'faux', 'correct', 'incorrect']):
            return 'vrai-faux'
        elif any(word in content_lower for word in ['calculer', 'résoudre', 'trouver']):
            return 'calcul'
        else:
            return 'libre'
    
    def _extract_qa(self, content: str) -> tuple:
        """Extraire question, réponse et explication"""
        # Patterns pour détecter les réponses
        answer_patterns = [
            r'Réponse[:\s]+([^\n]+)',
            r'Solution[:\s]+([^\n]+)',
            r'Résultat[:\s]+([^\n]+)',
            r'=\s*([^\n]+)',
        ]
        
        answer = ""
        explanation = ""
        
        for pattern in answer_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                answer = match.group(1).strip()
                # La question est tout ce qui précède la réponse
                question = content[:match.start()].strip()
                break
        else:
            # Si pas de réponse détectée, prendre tout comme question
            question = content
            answer = "À compléter manuellement"
        
        return question, answer, explanation
    
    def _extract_options(self, content: str) -> Optional[Dict[str, str]]:
        """Extraire les options pour les QCM"""
        options = {}
        
        # Pattern pour les options A), B), C), D)
        option_pattern = r'([A-D])\)\s*([^\n]+)'
        matches = re.findall(option_pattern, content)
        
        for letter, text in matches:
            options[letter] = text.strip()
        
        return options if options else None


def get_db_connection():
    """Créer une connexion à la base de données PostgreSQL"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            conn = psycopg2.connect(database_url)
        else:
            conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
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


def create_example_json():
    """Créer un fichier JSON d'exemple"""
    example = [
        {
            "type": "qcm",
            "body": "Quelle est la valeur de 2 + 3 ?",
            "options": {
                "A": "4",
                "B": "5", 
                "C": "6",
                "D": "7"
            },
            "answer": "B",
            "explanation": "2 + 3 = 5",
            "difficulty": "facile",
            "tags": ["addition", "arithmétique"]
        },
        {
            "type": "calcul",
            "body": "Résoudre l'équation: x + 5 = 12",
            "answer": "x = 7",
            "explanation": "x + 5 = 12 donc x = 12 - 5 = 7",
            "difficulty": "moyen",
            "tags": ["équations", "algèbre"]
        }
    ]
    
    with open('exercises_example.json', 'w', encoding='utf-8') as f:
        json.dump(example, f, ensure_ascii=False, indent=2)
    
    print("📄 Fichier d'exemple créé: exercises_example.json")


def main():
    parser = argparse.ArgumentParser(
        description='Importer des exercices depuis un PDF vers la base de données',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:

  # Import automatique depuis un PDF
  python scripts/pdf_exercise_importer.py --pdf exercises.pdf --course-id 1 --auto-format

  # Import manuel (demande de formatage)
  python scripts/pdf_exercise_importer.py --pdf exercises.pdf --course-id 1

  # Créer un fichier d'exemple
  python scripts/pdf_exercise_importer.py --create-example
        """
    )
    
    parser.add_argument(
        '--pdf',
        type=str,
        help='Fichier PDF contenant les exercices'
    )
    
    parser.add_argument(
        '--course-id',
        type=int,
        help='ID du cours auquel associer les exercices'
    )
    
    parser.add_argument(
        '--auto-format',
        action='store_true',
        help='Formatage automatique des exercices (expérimental)'
    )
    
    parser.add_argument(
        '--create-example',
        action='store_true',
        help='Créer un fichier JSON d\'exemple'
    )
    
    args = parser.parse_args()
    
    if args.create_example:
        create_example_json()
        return
    
    if not args.pdf or not args.course_id:
        parser.print_help()
        sys.exit(1)
    
    print('📥 ' + '='*58)
    print('📚 Import d\'exercices depuis PDF dans la base de données Mathia')
    print('📥 ' + '='*58 + '\n')
    
    # Vérifier que le fichier PDF existe
    if not os.path.exists(args.pdf):
        print(f"❌ Fichier PDF non trouvé: {args.pdf}")
        sys.exit(1)
    
    # Extraire les exercices du PDF
    extractor = PDFExerciseExtractor()
    print(f"📄 Extraction du texte depuis: {args.pdf}")
    text = extractor.extract_text_from_pdf(args.pdf)
    
    if not text:
        print("❌ Impossible d'extraire le texte du PDF")
        sys.exit(1)
    
    print(f"✅ {len(text)} caractères extraits")
    
    # Parser les exercices
    exercises = extractor.parse_exercises_from_text(text, args.auto_format)
    
    if not exercises:
        print("❌ Aucun exercice trouvé ou formaté")
        sys.exit(1)
    
    print(f"✅ {len(exercises)} exercices détectés\n")
    
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

