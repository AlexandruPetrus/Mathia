#!/usr/bin/env python3
"""
Extracteur spécialisé pour le manuel de mathématiques 6ème
Extrait et classe les exercices par chapitres
"""

import os
import sys
import json
import re
from typing import List, Dict, Any, Tuple, Optional

try:
    import pdfplumber
except ImportError:
    print("❌ Le module pdfplumber n'est pas installé.")
    print("📦 Installez-le avec: pip install pdfplumber")
    sys.exit(1)

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


class Manual6emeExtractor:
    """Extracteur spécialisé pour le manuel de mathématiques 6ème"""
    
    def __init__(self):
        self.chapters = []
        self.exercises = []
        self.current_chapter = None
        
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extraire le contenu du PDF et identifier les chapitres"""
        print(f"Extraction du contenu depuis: {pdf_path}")
        
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            page_texts = []
            
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    page_texts.append({
                        'page': page_num,
                        'text': page_text
                    })
                    all_text += f"\n--- PAGE {page_num} ---\n{page_text}\n"
            
            print(f"OK: {len(page_texts)} pages extraites")
            
            # Identifier les chapitres
            chapters = self._identify_chapters(all_text, page_texts)
            
            # Extraire les exercices par chapitre
            exercises_by_chapter = self._extract_exercises_by_chapter(all_text, chapters)
            
            return {
                'chapters': chapters,
                'exercises_by_chapter': exercises_by_chapter,
                'total_pages': len(page_texts)
            }
    
    def _identify_chapters(self, text: str, page_texts: List[Dict]) -> List[Dict[str, Any]]:
        """Identifier les chapitres dans le manuel"""
        chapters = []
        
        # Patterns pour identifier les chapitres
        chapter_patterns = [
            r'Chapitre\s+(\d+)[:.\s]+([^\n]+)',
            r'CHAPITRE\s+(\d+)[:.\s]+([^\n]+)',
            r'(\d+)[:.\s]+([^\n]+)',  # Pattern générique
            r'Partie\s+(\d+)[:.\s]+([^\n]+)',
            r'Module\s+(\d+)[:.\s]+([^\n]+)'
        ]
        
        # Rechercher dans tout le texte
        for pattern in chapter_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                chapter_num = match.group(1)
                chapter_title = match.group(2).strip()
                
                # Nettoyer le titre
                chapter_title = re.sub(r'[^\w\s\-àâäéèêëïîôöùûüÿç]', '', chapter_title)
                chapter_title = ' '.join(chapter_title.split())
                
                if len(chapter_title) > 3 and chapter_title not in [ch['title'] for ch in chapters]:
                    chapters.append({
                        'number': int(chapter_num),
                        'title': chapter_title,
                        'position': match.start()
                    })
        
        # Trier par position dans le texte
        chapters.sort(key=lambda x: x['position'])
        
        # Si pas de chapitres trouvés, créer des chapitres génériques
        if not chapters:
            print("Aucun chapitre detecte, creation de chapitres generiques...")
            chapters = self._create_generic_chapters(text)
        
        print(f"{len(chapters)} chapitres identifies:")
        for chapter in chapters:
            print(f"   {chapter['number']}. {chapter['title']}")
        
        return chapters
    
    def _create_generic_chapters(self, text: str) -> List[Dict[str, Any]]:
        """Créer des chapitres génériques basés sur le contenu"""
        chapters = []
        
        # Thèmes typiques de 6ème
        themes_6eme = [
            "Nombres entiers et décimaux",
            "Opérations sur les nombres",
            "Fractions",
            "Proportionnalité",
            "Géométrie - Droites et angles",
            "Géométrie - Triangles et quadrilatères",
            "Périmètres et aires",
            "Statistiques et probabilités"
        ]
        
        for i, theme in enumerate(themes_6eme, 1):
            chapters.append({
                'number': i,
                'title': theme,
                'position': i * 1000  # Position approximative
            })
        
        return chapters
    
    def _extract_exercices_by_chapter(self, text: str, chapters: List[Dict]) -> Dict[str, List[Dict]]:
        """Extraire les exercices organisés par chapitre"""
        exercises_by_chapter = {}
        
        for chapter in chapters:
            chapter_key = f"chapitre_{chapter['number']}"
            exercises_by_chapter[chapter_key] = []
        
        # Patterns pour identifier les exercices
        exercise_patterns = [
            r'Exercice\s+(\d+)[:.\s]*(.*?)(?=Exercice\s+\d+|Chapitre\s+\d+|$)',
            r'(\d+)[:.\s]*(.*?)(?=\d+[:.]|Chapitre\s+\d+|$)',
            r'Question\s+(\d+)[:.\s]*(.*?)(?=Question\s+\d+|Chapitre\s+\d+|$)',
            r'Problème\s+(\d+)[:.\s]*(.*?)(?=Problème\s+\d+|Chapitre\s+\d+|$)'
        ]
        
        # Diviser le texte par chapitres approximatifs
        chapter_sections = self._split_text_by_chapters(text, chapters)
        
        for chapter in chapters:
            chapter_key = f"chapitre_{chapter['number']}"
            chapter_text = chapter_sections.get(chapter_key, "")
            
            if not chapter_text:
                continue
            
            # Extraire les exercices de ce chapitre
            exercises = self._extract_exercises_from_text(chapter_text, chapter)
            exercises_by_chapter[chapter_key] = exercises
            
            print(f"Chapitre {chapter['number']}: {len(exercises)} exercices extraits")
        
        return exercises_by_chapter
    
    def _split_text_by_chapters(self, text: str, chapters: List[Dict]) -> Dict[str, str]:
        """Diviser le texte en sections par chapitre"""
        sections = {}
        
        for i, chapter in enumerate(chapters):
            chapter_key = f"chapitre_{chapter['number']}"
            
            # Déterminer les limites du chapitre
            start_pos = chapter['position']
            
            if i + 1 < len(chapters):
                end_pos = chapters[i + 1]['position']
            else:
                end_pos = len(text)
            
            # Extraire la section
            section_text = text[start_pos:end_pos]
            sections[chapter_key] = section_text
        
        return sections
    
    def _extract_exercises_from_text(self, text: str, chapter: Dict) -> List[Dict[str, Any]]:
        """Extraire les exercices d'un texte de chapitre"""
        exercises = []
        
        # Patterns pour les exercices
        exercise_patterns = [
            r'Exercice\s+(\d+)[:.\s]*(.*?)(?=Exercice\s+\d+|$)',
            r'(\d+)[:.\s]*(.*?)(?=\d+[:.]|$)',
        ]
        
        for pattern in exercise_patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                exercise_num = match.group(1)
                content = match.group(2).strip()
                
                if len(content) > 20:  # Filtrer les contenus trop courts
                    exercise = self._format_exercise(content, exercise_num, chapter)
                    if exercise:
                        exercises.append(exercise)
        
        return exercises
    
    def _format_exercise(self, content: str, exercise_num: str, chapter: Dict) -> Optional[Dict[str, Any]]:
        """Formater un exercice"""
        # Nettoyer le contenu
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Détecter le type d'exercice
        exercise_type = self._detect_exercise_type(content)
        
        # Extraire question et réponse
        question, answer, explanation = self._extract_qa(content)
        
        if not question:
            return None
        
        return {
            'type': exercise_type,
            'body': question,
            'answer': answer or "À compléter",
            'explanation': explanation,
            'difficulty': self._estimate_difficulty(content),
            'tags': [
                '6ème',
                f'chapitre_{chapter["number"]}',
                chapter['title'].lower().replace(' ', '_'),
                exercise_type
            ],
            'options': self._extract_options(content) if exercise_type == 'qcm' else None,
            'chapter_number': chapter['number'],
            'chapter_title': chapter['title'],
            'exercise_number': exercise_num
        }
    
    def _detect_exercise_type(self, content: str) -> str:
        """Détecter le type d'exercice"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['a)', 'b)', 'c)', 'd)', 'choisir', 'sélectionner']):
            return 'qcm'
        elif any(word in content_lower for word in ['vrai', 'faux', 'correct', 'incorrect']):
            return 'vrai-faux'
        elif any(word in content_lower for word in ['calculer', 'résoudre', 'trouver', 'déterminer']):
            return 'calcul'
        else:
            return 'libre'
    
    def _extract_qa(self, content: str) -> Tuple[str, str, str]:
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
                question = content[:match.start()].strip()
                break
        else:
            question = content
            answer = "À compléter"
        
        return question, answer, explanation
    
    def _extract_options(self, content: str) -> Optional[Dict[str, str]]:
        """Extraire les options pour les QCM"""
        options = {}
        
        option_pattern = r'([A-D])\)\s*([^\n]+)'
        matches = re.findall(option_pattern, content)
        
        for letter, text in matches:
            options[letter] = text.strip()
        
        return options if options else None
    
    def _estimate_difficulty(self, content: str) -> str:
        """Estimer la difficulté de l'exercice"""
        content_lower = content.lower()
        
        # Mots-clés de difficulté
        easy_keywords = ['simple', 'facile', 'basique', 'direct']
        hard_keywords = ['complexe', 'difficile', 'compliqué', 'démonstration']
        
        if any(word in content_lower for word in easy_keywords):
            return 'facile'
        elif any(word in content_lower for word in hard_keywords):
            return 'difficile'
        else:
            return 'moyen'
    
    def save_results(self, results: Dict[str, Any], output_dir: str):
        """Sauvegarder les résultats"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Sauvegarder les chapitres
        chapters_file = os.path.join(output_dir, 'chapitres_6eme.json')
        with open(chapters_file, 'w', encoding='utf-8') as f:
            json.dump(results['chapters'], f, ensure_ascii=False, indent=2)
        
        # Sauvegarder les exercices par chapitre
        for chapter_key, exercises in results['exercises_by_chapter'].items():
            if exercises:
                exercises_file = os.path.join(output_dir, f'{chapter_key}_exercices.json')
                with open(exercises_file, 'w', encoding='utf-8') as f:
                    json.dump(exercises, f, ensure_ascii=False, indent=2)
        
        # Sauvegarder un résumé
        summary = {
            'total_chapters': len(results['chapters']),
            'total_exercises': sum(len(exercises) for exercises in results['exercises_by_chapter'].values()),
            'exercises_by_chapter': {
                chapter_key: len(exercises) 
                for chapter_key, exercises in results['exercises_by_chapter'].items()
            },
            'chapters': results['chapters']
        }
        
        summary_file = os.path.join(output_dir, 'resume_extraction.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"Resultats sauvegardes dans: {output_dir}")
        return summary


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
        print(f"Erreur de connexion a la base de donnees: {e}")
        return None


def create_courses_for_chapters(chapters: List[Dict], conn) -> Dict[int, int]:
    """Créer les cours correspondants aux chapitres"""
    if not conn:
        print("Pas de connexion a la base de donnees")
        return {}
    
    cursor = conn.cursor()
    chapter_to_course_id = {}
    
    try:
        for chapter in chapters:
            # Vérifier si le cours existe déjà
            cursor.execute(
                "SELECT id FROM courses WHERE title = %s AND grade = %s",
                (chapter['title'], '6ème')
            )
            existing = cursor.fetchone()
            
            if existing:
                course_id = existing[0]
                print(f"Cours existant trouve: {chapter['title']} (ID: {course_id})")
            else:
                # Créer le nouveau cours
                cursor.execute(
                    """
                    INSERT INTO courses (title, grade, chapter, description, "createdAt", "updatedAt")
                    VALUES (%s, %s, %s, %s, NOW(), NOW())
                    RETURNING id
                    """,
                    (
                        chapter['title'],
                        '6eme',
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


def import_exercises_to_db(exercises_by_chapter: Dict[str, List[Dict]], 
                          chapter_to_course_id: Dict[int, int], 
                          conn):
    """Importer les exercices dans la base de données"""
    if not conn:
        print("Pas de connexion a la base de donnees")
        return
    
    cursor = conn.cursor()
    total_imported = 0
    total_errors = 0
    
    try:
        for chapter_key, exercises in exercises_by_chapter.items():
            if not exercises:
                continue
            
            # Récupérer le numéro de chapitre
            chapter_num = int(chapter_key.split('_')[1])
            course_id = chapter_to_course_id.get(chapter_num)
            
            if not course_id:
                print(f"Pas de cours trouve pour le chapitre {chapter_num}")
                continue
            
            print(f"Import des exercices du chapitre {chapter_num}...")
            
            for exercise in exercises:
                try:
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
                    print(f"   Exercice importe (ID: {exercise_id})")
                    
                except Exception as e:
                    total_errors += 1
                    print(f"   Erreur: {e}")
        
        conn.commit()
        cursor.close()
        
        print(f"\nImport termine: {total_imported} exercices importes, {total_errors} erreurs")
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        print(f"Erreur lors de l'import: {e}")


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extracteur du manuel de mathématiques 6ème')
    parser.add_argument('--pdf', default='Cours maths college pdf/livre-prof-indigo-6eme.pdf', 
                       help='Chemin vers le PDF du manuel')
    parser.add_argument('--output', default='extracted_6eme', 
                       help='Dossier de sortie pour les résultats')
    parser.add_argument('--import-db', action='store_true', 
                       help='Importer directement dans la base de données')
    parser.add_argument('--no-save', action='store_true', 
                       help='Ne pas sauvegarder les fichiers JSON')
    
    args = parser.parse_args()
    
    print('='*60)
    print('Extracteur du manuel de mathematiques 6eme')
    print('='*60 + '\n')
    
    # Vérifier que le fichier PDF existe
    if not os.path.exists(args.pdf):
        print(f"Erreur: Fichier PDF non trouve: {args.pdf}")
        sys.exit(1)
    
    # Extraire le contenu
    extractor = Manual6emeExtractor()
    results = extractor.extract_from_pdf(args.pdf)
    
    # Afficher le résumé
    print(f"\nRESUME DE L'EXTRACTION:")
    print(f"   Pages analysees: {results['total_pages']}")
    print(f"   Chapitres identifies: {len(results['chapters'])}")
    
    total_exercises = sum(len(exercises) for exercises in results['exercises_by_chapter'].values())
    print(f"   Exercices extraits: {total_exercises}")
    
    # Détail par chapitre
    print(f"\nDETAIL PAR CHAPITRE:")
    for chapter in results['chapters']:
        chapter_key = f"chapitre_{chapter['number']}"
        exercises_count = len(results['exercises_by_chapter'].get(chapter_key, []))
        print(f"   {chapter['number']}. {chapter['title']}: {exercises_count} exercices")
    
    # Sauvegarder les résultats
    if not args.no_save:
        summary = extractor.save_results(results, args.output)
        print(f"\nFichiers sauvegardes dans: {args.output}")
    
    # Importer dans la base de données si demandé
    if args.import_db:
        print(f"\nImport dans la base de donnees...")
        
        conn = get_db_connection()
        if conn:
            # Créer les cours
            chapter_to_course_id = create_courses_for_chapters(results['chapters'], conn)
            
            if chapter_to_course_id:
                # Importer les exercices
                import_exercises_to_db(results['exercises_by_chapter'], chapter_to_course_id, conn)
            
            conn.close()
        else:
            print("Erreur: Impossible de se connecter a la base de donnees")
    
    print(f"\nExtraction terminee avec succes!")


if __name__ == '__main__':
    main()
