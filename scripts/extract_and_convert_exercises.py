#!/usr/bin/env python3
"""
Extracteur et convertisseur d'exercices pour Mathia
Extrait les exercices du PDF et les convertit au format de l'application
"""

import os
import sys
import json
import re
from typing import List, Dict, Any, Optional

try:
    import pdfplumber
except ImportError:
    print("Erreur: Le module pdfplumber n'est pas installe.")
    print("Installez-le avec: pip install pdfplumber")
    sys.exit(1)

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

# Configuration de la base de données
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', 5432),
    'database': os.getenv('DB_NAME', 'mathia_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}


class ExerciseExtractor:
    """Extracteur et convertisseur d'exercices pour Mathia"""
    
    def __init__(self):
        self.exercises = []
        self.chapters = [
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
    
    def extract_from_pdf(self, pdf_path: str) -> str:
        """Extraire le texte du PDF"""
        print(f"Extraction du texte depuis: {pdf_path}")
        
        all_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        # Nettoyer le texte
                        page_text = self._clean_text(page_text)
                        all_text += f"\n--- PAGE {page_num} ---\n{page_text}\n"
                except Exception as e:
                    print(f"Erreur page {page_num}: {e}")
                    continue
        
        print(f"Extraction terminee: {len(all_text)} caracteres extraits")
        return all_text
    
    def _clean_text(self, text: str) -> str:
        """Nettoyer le texte des caracteres problematiques"""
        # Remplacer les caracteres accentues
        replacements = {
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'à': 'a', 'â': 'a', 'ä': 'a',
            'ù': 'u', 'û': 'u', 'ü': 'u',
            'ô': 'o', 'ö': 'o',
            'î': 'i', 'ï': 'i',
            'ç': 'c',
            'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
            'À': 'A', 'Â': 'A', 'Ä': 'A',
            'Ù': 'U', 'Û': 'U', 'Ü': 'U',
            'Ô': 'O', 'Ö': 'O',
            'Î': 'I', 'Ï': 'I',
            'Ç': 'C'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def find_exercises_in_text(self, text: str) -> List[Dict[str, Any]]:
        """Trouver et extraire les exercices dans le texte"""
        exercises = []
        
        # Patterns pour identifier les exercices
        exercise_patterns = [
            r'Exercice\s+(\d+)[:.\s]*(.*?)(?=Exercice\s+\d+|$)',
            r'(\d+)[:.\s]*(.*?)(?=\d+[:.]|$)',
            r'Question\s+(\d+)[:.\s]*(.*?)(?=Question\s+\d+|$)',
        ]
        
        for pattern in exercise_patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                exercise_num = match.group(1)
                content = match.group(2).strip()
                
                if len(content) > 30:  # Filtrer les contenus trop courts
                    exercise = self._convert_to_app_format(content, exercise_num)
                    if exercise:
                        exercises.append(exercise)
        
        print(f"Trouve {len(exercises)} exercices dans le texte")
        return exercises
    
    def _convert_to_app_format(self, content: str, exercise_num: str) -> Optional[Dict[str, Any]]:
        """Convertir un exercice au format de l'application"""
        # Nettoyer le contenu
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Determiner le type d'exercice
        exercise_type = self._detect_exercise_type(content)
        
        # Extraire la question
        question = self._extract_question(content)
        
        if not question or len(question) < 10:
            return None
        
        # Determiner le chapitre
        chapter = self._determine_chapter(content)
        
        # Creer l'exercice au format de l'application
        exercise = {
            'type': exercise_type,
            'body': question,
            'answer': self._extract_answer(content),
            'explanation': self._extract_explanation(content),
            'difficulty': self._estimate_difficulty(content),
            'tags': [
                '6eme',
                f'chapitre_{chapter["number"]}',
                chapter['title'].lower().replace(' ', '_'),
                exercise_type,
                'extrait_manuel'
            ],
            'options': self._extract_options(content) if exercise_type == 'qcm' else None,
            'chapter_number': chapter['number'],
            'chapter_title': chapter['title'],
            'exercise_number': exercise_num
        }
        
        return exercise
    
    def _detect_exercise_type(self, content: str) -> str:
        """Detecter le type d'exercice"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['a)', 'b)', 'c)', 'd)', 'choisir', 'selectionner']):
            return 'qcm'
        elif any(word in content_lower for word in ['vrai', 'faux', 'correct', 'incorrect']):
            return 'vrai-faux'
        elif any(word in content_lower for word in ['calculer', 'resoudre', 'trouver', 'determiner']):
            return 'calcul'
        else:
            return 'libre'
    
    def _extract_question(self, content: str) -> str:
        """Extraire la question de l'exercice"""
        # Supprimer les reponses et explications
        content = re.sub(r'Reponse[:\s]+[^\n]+', '', content, flags=re.IGNORECASE)
        content = re.sub(r'Solution[:\s]+[^\n]+', '', content, flags=re.IGNORECASE)
        content = re.sub(r'Resultat[:\s]+[^\n]+', '', content, flags=re.IGNORECASE)
        
        # Nettoyer
        question = content.strip()
        question = re.sub(r'\s+', ' ', question)
        
        return question
    
    def _extract_answer(self, content: str) -> str:
        """Extraire la reponse de l'exercice"""
        answer_patterns = [
            r'Reponse[:\s]+([^\n]+)',
            r'Solution[:\s]+([^\n]+)',
            r'Resultat[:\s]+([^\n]+)',
        ]
        
        for pattern in answer_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "A completer"
    
    def _extract_explanation(self, content: str) -> Optional[str]:
        """Extraire l'explication de l'exercice"""
        # Pour l'instant, pas d'explication dans le PDF
        return None
    
    def _extract_options(self, content: str) -> Optional[Dict[str, str]]:
        """Extraire les options pour les QCM"""
        options = {}
        
        option_pattern = r'([A-D])\)\s*([^\n]+)'
        matches = re.findall(option_pattern, content)
        
        for letter, text in matches:
            options[letter] = text.strip()
        
        return options if options else None
    
    def _estimate_difficulty(self, content: str) -> str:
        """Estimer la difficulte de l'exercice"""
        content_lower = content.lower()
        
        easy_keywords = ['simple', 'facile', 'basique', 'direct']
        hard_keywords = ['complexe', 'difficile', 'complique', 'demonstration']
        
        if any(word in content_lower for word in easy_keywords):
            return 'facile'
        elif any(word in content_lower for word in hard_keywords):
            return 'difficile'
        else:
            return 'moyen'
    
    def _determine_chapter(self, content: str) -> Dict[str, Any]:
        """Determiner le chapitre de l'exercice"""
        content_lower = content.lower()
        
        # Mots-cles par chapitre
        chapter_keywords = {
            1: ['nombre', 'entier', 'millier', 'million', 'milliard'],
            2: ['decimal', 'virgule', 'dixieme', 'centieme', 'millieme'],
            3: ['addition', 'soustraction', 'multiplication', 'division', 'operation'],
            4: ['fraction', 'numerateur', 'denominateur', 'partage'],
            5: ['proportionnel', 'pourcentage', 'echelle', 'coefficient'],
            6: ['droite', 'angle', 'perpendiculaire', 'parallele', 'mesure'],
            7: ['triangle', 'quadrilatere', 'rectangle', 'carre', 'losange'],
            8: ['perimetre', 'aire', 'surface', 'formule', 'calculer'],
            9: ['statistique', 'moyenne', 'graphique', 'diagramme', 'probabilite']
        }
        
        # Compter les occurrences
        scores = {}
        for chapter_num, keywords in chapter_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            if score > 0:
                scores[chapter_num] = score
        
        # Retourner le chapitre avec le meilleur score
        if scores:
            best_chapter = max(scores, key=scores.get)
            return self.chapters[best_chapter - 1]
        else:
            return self.chapters[0]  # Par defaut, premier chapitre
    
    def save_exercises(self, exercises: List[Dict[str, Any]], output_file: str):
        """Sauvegarder les exercices dans un fichier JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(exercises, f, ensure_ascii=False, indent=2)
        
        print(f"Exercices sauvegardes dans: {output_file}")
    
    def create_courses_in_db(self, conn) -> Dict[int, int]:
        """Creer les cours dans la base de donnees"""
        if not conn:
            print("Pas de connexion a la base de donnees")
            return {}
        
        cursor = conn.cursor()
        chapter_to_course_id = {}
        
        try:
            for chapter in self.chapters:
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
    
    def import_exercises_to_db(self, exercises: List[Dict[str, Any]], 
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
            for exercise in exercises:
                try:
                    chapter_num = exercise.get('chapter_number', 1)
                    course_id = chapter_to_course_id.get(chapter_num)
                    
                    if not course_id:
                        print(f"Pas de cours trouve pour le chapitre {chapter_num}")
                        continue
                    
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
                            exercise.get('body', ''),
                            Json(exercise.get('options')) if exercise.get('options') else None,
                            exercise.get('answer', ''),
                            exercise.get('explanation', ''),
                            exercise.get('difficulty', 'moyen'),
                            Json(exercise.get('tags', []))
                        )
                    )
                    
                    exercise_id = cursor.fetchone()[0]
                    total_imported += 1
                    
                    if total_imported % 10 == 0:
                        print(f"Importe {total_imported} exercices...")
                    
                except Exception as e:
                    total_errors += 1
                    print(f"Erreur exercice: {e}")
            
            conn.commit()
            cursor.close()
            
            print(f"Import termine: {total_imported} exercices importes, {total_errors} erreurs")
            
        except Exception as e:
            conn.rollback()
            cursor.close()
            print(f"Erreur lors de l'import: {e}")


def get_db_connection():
    """Creer une connexion a la base de donnees PostgreSQL"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            conn = psycopg2.connect(database_url)
        else:
            conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Erreur de connexion a la base de donnees: {e}")
        return None


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extracteur et convertisseur d\'exercices pour Mathia')
    parser.add_argument('--pdf', default='Cours maths college pdf/livre-prof-indigo-6eme.pdf', 
                       help='Chemin vers le PDF du manuel')
    parser.add_argument('--output', default='exercices_6eme.json', 
                       help='Fichier de sortie pour les exercices')
    parser.add_argument('--import-db', action='store_true', 
                       help='Importer directement dans la base de donnees')
    parser.add_argument('--no-save', action='store_true', 
                       help='Ne pas sauvegarder le fichier JSON')
    
    args = parser.parse_args()
    
    print('='*60)
    print('Extracteur et convertisseur d\'exercices pour Mathia')
    print('='*60 + '\n')
    
    # Verifier que le fichier PDF existe
    if not os.path.exists(args.pdf):
        print(f"Erreur: Fichier PDF non trouve: {args.pdf}")
        sys.exit(1)
    
    # Extraire et convertir
    extractor = ExerciseExtractor()
    
    # Extraire le texte du PDF
    text = extractor.extract_from_pdf(args.pdf)
    
    # Trouver et convertir les exercices
    exercises = extractor.find_exercises_in_text(text)
    
    # Afficher le resume
    print(f"\nRESUME DE L'EXTRACTION:")
    print(f"   Exercices trouves: {len(exercises)}")
    
    # Statistiques par type
    type_stats = {}
    for exercise in exercises:
        ex_type = exercise.get('type', 'unknown')
        type_stats[ex_type] = type_stats.get(ex_type, 0) + 1
    
    print(f"   Par type:")
    for ex_type, count in type_stats.items():
        print(f"     {ex_type}: {count}")
    
    # Statistiques par chapitre
    chapter_stats = {}
    for exercise in exercises:
        chapter_num = exercise.get('chapter_number', 1)
        chapter_stats[chapter_num] = chapter_stats.get(chapter_num, 0) + 1
    
    print(f"   Par chapitre:")
    for chapter_num, count in sorted(chapter_stats.items()):
        chapter_title = next((ch['title'] for ch in extractor.chapters if ch['number'] == chapter_num), f"Chapitre {chapter_num}")
        print(f"     {chapter_num}. {chapter_title}: {count}")
    
    # Sauvegarder les exercices
    if not args.no_save:
        extractor.save_exercises(exercises, args.output)
        print(f"\nFichier sauvegarde: {args.output}")
    
    # Importer dans la base de donnees si demande
    if args.import_db:
        print(f"\nImport dans la base de donnees...")
        
        conn = get_db_connection()
        if conn:
            # Creer les cours
            chapter_to_course_id = extractor.create_courses_in_db(conn)
            
            if chapter_to_course_id:
                # Importer les exercices
                extractor.import_exercises_to_db(exercises, chapter_to_course_id, conn)
            
            conn.close()
        else:
            print("Erreur: Impossible de se connecter a la base de donnees")
    
    print(f"\nExtraction et conversion terminees avec succes!")


if __name__ == '__main__':
    main()

