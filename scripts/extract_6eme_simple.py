#!/usr/bin/env python3
"""
Extracteur simplifié pour le manuel de mathématiques 6ème
Version sans problèmes d'encodage
"""

import os
import sys
import json
import re
from typing import List, Dict, Any, Tuple, Optional

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


class Simple6emeExtractor:
    """Extracteur simplifié pour le manuel de mathématiques 6ème"""
    
    def __init__(self):
        self.chapters = []
        self.exercises = []
        
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extraire le contenu du PDF et identifier les chapitres"""
        print(f"Extraction du contenu depuis: {pdf_path}")
        
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            page_texts = []
            
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        # Nettoyer le texte des caractères problématiques
                        page_text = self._clean_text(page_text)
                        page_texts.append({
                            'page': page_num,
                            'text': page_text
                        })
                        all_text += f"\n--- PAGE {page_num} ---\n{page_text}\n"
                except Exception as e:
                    print(f"Erreur page {page_num}: {e}")
                    continue
            
            print(f"OK: {len(page_texts)} pages extraites")
            
            # Identifier les chapitres
            chapters = self._identify_chapters(all_text)
            
            # Extraire les exercices par chapitre
            exercises_by_chapter = self._extract_exercises_by_chapter(all_text, chapters)
            
            return {
                'chapters': chapters,
                'exercises_by_chapter': exercises_by_chapter,
                'total_pages': len(page_texts)
            }
    
    def _clean_text(self, text: str) -> str:
        """Nettoyer le texte des caractères problématiques"""
        # Remplacer les caractères problématiques
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
    
    def _identify_chapters(self, text: str) -> List[Dict[str, Any]]:
        """Identifier les chapitres dans le manuel"""
        chapters = []
        
        # Patterns pour identifier les chapitres
        chapter_patterns = [
            r'Chapitre\s+(\d+)[:.\s]+([^\n]+)',
            r'CHAPITRE\s+(\d+)[:.\s]+([^\n]+)',
            r'(\d+)[:.\s]+([^\n]+)',  # Pattern générique
        ]
        
        # Rechercher dans tout le texte
        for pattern in chapter_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                chapter_num = match.group(1)
                chapter_title = match.group(2).strip()
                
                # Nettoyer le titre
                chapter_title = re.sub(r'[^\w\s\-]', '', chapter_title)
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
            chapters = self._create_generic_chapters()
        
        print(f"{len(chapters)} chapitres identifies:")
        for chapter in chapters:
            print(f"   {chapter['number']}. {chapter['title']}")
        
        return chapters
    
    def _create_generic_chapters(self) -> List[Dict[str, Any]]:
        """Créer des chapitres génériques basés sur le contenu"""
        chapters = []
        
        # Thèmes typiques de 6ème
        themes_6eme = [
            "Nombres entiers et decimaux",
            "Operations sur les nombres",
            "Fractions",
            "Proportionnalite",
            "Geometrie - Droites et angles",
            "Geometrie - Triangles et quadrilateres",
            "Perimetres et aires",
            "Statistiques et probabilites"
        ]
        
        for i, theme in enumerate(themes_6eme, 1):
            chapters.append({
                'number': i,
                'title': theme,
                'position': i * 1000  # Position approximative
            })
        
        return chapters
    
    def _extract_exercises_by_chapter(self, text: str, chapters: List[Dict]) -> Dict[str, List[Dict]]:
        """Extraire les exercices organisés par chapitre"""
        exercises_by_chapter = {}
        
        for chapter in chapters:
            chapter_key = f"chapitre_{chapter['number']}"
            exercises_by_chapter[chapter_key] = []
        
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
            'answer': answer or "A completer",
            'explanation': explanation,
            'difficulty': self._estimate_difficulty(content),
            'tags': [
                '6eme',
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
        
        if any(word in content_lower for word in ['a)', 'b)', 'c)', 'd)', 'choisir', 'selectionner']):
            return 'qcm'
        elif any(word in content_lower for word in ['vrai', 'faux', 'correct', 'incorrect']):
            return 'vrai-faux'
        elif any(word in content_lower for word in ['calculer', 'resoudre', 'trouver', 'determiner']):
            return 'calcul'
        else:
            return 'libre'
    
    def _extract_qa(self, content: str) -> Tuple[str, str, str]:
        """Extraire question, réponse et explication"""
        # Patterns pour détecter les réponses
        answer_patterns = [
            r'Reponse[:\s]+([^\n]+)',
            r'Solution[:\s]+([^\n]+)',
            r'Resultat[:\s]+([^\n]+)',
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
            answer = "A completer"
        
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
        hard_keywords = ['complexe', 'difficile', 'complique', 'demonstration']
        
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


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extracteur du manuel de mathematiques 6eme')
    parser.add_argument('--pdf', default='Cours maths college pdf/livre-prof-indigo-6eme.pdf', 
                       help='Chemin vers le PDF du manuel')
    parser.add_argument('--output', default='extracted_6eme', 
                       help='Dossier de sortie pour les resultats')
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
    extractor = Simple6emeExtractor()
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
    
    print(f"\nExtraction terminee avec succes!")


if __name__ == '__main__':
    main()

