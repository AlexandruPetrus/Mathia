#!/usr/bin/env python3
"""
Outil de formatage d'exercices pour Mathia
Permet de convertir des exercices bruts en format JSON structuré
"""

import json
import re
from typing import List, Dict, Any, Optional


class ExerciseFormatter:
    """Formateur d'exercices pour Mathia"""
    
    def __init__(self):
        self.exercises = []
    
    def add_exercise(self, 
                    body: str, 
                    answer: str, 
                    exercise_type: str = "libre",
                    options: Optional[Dict[str, str]] = None,
                    explanation: Optional[str] = None,
                    difficulty: str = "moyen",
                    tags: Optional[List[str]] = None):
        """Ajouter un exercice formaté"""
        
        exercise = {
            "type": exercise_type,
            "body": body.strip(),
            "answer": answer.strip(),
            "explanation": explanation.strip() if explanation else None,
            "difficulty": difficulty,
            "tags": tags or [],
            "options": options
        }
        
        self.exercises.append(exercise)
        return len(self.exercises)
    
    def add_qcm_exercise(self, 
                        question: str, 
                        correct_answer: str,
                        options: Dict[str, str],
                        explanation: Optional[str] = None,
                        difficulty: str = "moyen",
                        tags: Optional[List[str]] = None):
        """Ajouter un exercice QCM"""
        return self.add_exercise(
            body=question,
            answer=correct_answer,
            exercise_type="qcm",
            options=options,
            explanation=explanation,
            difficulty=difficulty,
            tags=tags
        )
    
    def add_calculation_exercise(self,
                                problem: str,
                                solution: str,
                                explanation: Optional[str] = None,
                                difficulty: str = "moyen",
                                tags: Optional[List[str]] = None):
        """Ajouter un exercice de calcul"""
        return self.add_exercise(
            body=problem,
            answer=solution,
            exercise_type="calcul",
            explanation=explanation,
            difficulty=difficulty,
            tags=tags
        )
    
    def add_true_false_exercise(self,
                               statement: str,
                               is_true: bool,
                               explanation: Optional[str] = None,
                               difficulty: str = "moyen",
                               tags: Optional[List[str]] = None):
        """Ajouter un exercice vrai/faux"""
        return self.add_exercise(
            body=statement,
            answer="Vrai" if is_true else "Faux",
            exercise_type="vrai-faux",
            explanation=explanation,
            difficulty=difficulty,
            tags=tags
        )
    
    def parse_from_text(self, text: str) -> int:
        """Parser des exercices depuis un texte brut"""
        # Diviser le texte en exercices potentiels
        exercises_text = self._split_exercises(text)
        
        for i, exercise_text in enumerate(exercises_text, 1):
            exercise = self._parse_single_exercise(exercise_text, i)
            if exercise:
                self.exercises.append(exercise)
        
        return len(self.exercises)
    
    def _split_exercises(self, text: str) -> List[str]:
        """Diviser le texte en exercices individuels"""
        # Patterns pour détecter le début d'un exercice
        patterns = [
            r'Exercice\s+\d+',
            r'\d+[\.\)]\s*',
            r'Question\s+\d+',
            r'Problème\s+\d+'
        ]
        
        exercises = []
        current_exercise = ""
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Vérifier si c'est le début d'un nouvel exercice
            is_new_exercise = any(re.match(pattern, line, re.IGNORECASE) for pattern in patterns)
            
            if is_new_exercise and current_exercise:
                exercises.append(current_exercise.strip())
                current_exercise = line
            else:
                current_exercise += " " + line if current_exercise else line
        
        # Ajouter le dernier exercice
        if current_exercise:
            exercises.append(current_exercise.strip())
        
        return exercises
    
    def _parse_single_exercise(self, text: str, number: int) -> Optional[Dict[str, Any]]:
        """Parser un exercice individuel"""
        # Nettoyer le texte
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Détecter le type d'exercice
        exercise_type = self._detect_type(text)
        
        # Extraire les composants
        if exercise_type == "qcm":
            return self._parse_qcm(text, number)
        elif exercise_type == "vrai-faux":
            return self._parse_true_false(text, number)
        else:
            return self._parse_general(text, number, exercise_type)
    
    def _detect_type(self, text: str) -> str:
        """Détecter le type d'exercice"""
        text_lower = text.lower()
        
        if any(pattern in text_lower for pattern in ['a)', 'b)', 'c)', 'd)', 'choisir', 'sélectionner']):
            return "qcm"
        elif any(pattern in text_lower for pattern in ['vrai', 'faux', 'correct', 'incorrect']):
            return "vrai-faux"
        elif any(pattern in text_lower for pattern in ['calculer', 'résoudre', 'trouver', 'déterminer']):
            return "calcul"
        else:
            return "libre"
    
    def _parse_qcm(self, text: str, number: int) -> Optional[Dict[str, Any]]:
        """Parser un exercice QCM"""
        # Extraire les options
        options = {}
        option_pattern = r'([A-D])\)\s*([^\n]+)'
        matches = re.findall(option_pattern, text)
        
        for letter, content in matches:
            options[letter] = content.strip()
        
        if not options:
            return None
        
        # Extraire la question (tout ce qui précède les options)
        question = text
        for match in re.finditer(option_pattern, text):
            question = text[:match.start()].strip()
            break
        
        # La réponse correcte doit être déterminée manuellement
        answer = "À déterminer"
        
        return {
            "type": "qcm",
            "body": question,
            "options": options,
            "answer": answer,
            "explanation": None,
            "difficulty": "moyen",
            "tags": ["imported", f"exercice_{number}"]
        }
    
    def _parse_true_false(self, text: str, number: int) -> Optional[Dict[str, Any]]:
        """Parser un exercice vrai/faux"""
        # Extraire l'énoncé
        statement = text
        answer = "À déterminer"
        
        return {
            "type": "vrai-faux",
            "body": statement,
            "answer": answer,
            "explanation": None,
            "difficulty": "moyen",
            "tags": ["imported", f"exercice_{number}"]
        }
    
    def _parse_general(self, text: str, number: int, exercise_type: str) -> Optional[Dict[str, Any]]:
        """Parser un exercice général"""
        # Extraire question et réponse si possible
        answer_patterns = [
            r'Réponse[:\s]+([^\n]+)',
            r'Solution[:\s]+([^\n]+)',
            r'Résultat[:\s]+([^\n]+)',
        ]
        
        answer = "À compléter"
        question = text
        
        for pattern in answer_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                answer = match.group(1).strip()
                question = text[:match.start()].strip()
                break
        
        return {
            "type": exercise_type,
            "body": question,
            "answer": answer,
            "explanation": None,
            "difficulty": "moyen",
            "tags": ["imported", f"exercice_{number}"]
        }
    
    def save_to_file(self, filename: str):
        """Sauvegarder les exercices dans un fichier JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.exercises, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {len(self.exercises)} exercices sauvegardés dans {filename}")
    
    def load_from_file(self, filename: str):
        """Charger des exercices depuis un fichier JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.exercises = json.load(f)
            print(f"✅ {len(self.exercises)} exercices chargés depuis {filename}")
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
    
    def preview(self, limit: int = 5):
        """Aperçu des exercices"""
        print(f"\n📋 Aperçu des exercices ({min(limit, len(self.exercises))}/{len(self.exercises)}):")
        print("=" * 60)
        
        for i, exercise in enumerate(self.exercises[:limit], 1):
            print(f"\n{i}. Type: {exercise['type']}")
            print(f"   Question: {exercise['body'][:80]}...")
            print(f"   Réponse: {exercise['answer']}")
            if exercise.get('options'):
                print(f"   Options: {list(exercise['options'].keys())}")
            print(f"   Tags: {exercise.get('tags', [])}")
    
    def get_statistics(self):
        """Obtenir des statistiques sur les exercices"""
        stats = {
            "total": len(self.exercises),
            "by_type": {},
            "by_difficulty": {},
            "with_explanations": 0,
            "with_options": 0
        }
        
        for exercise in self.exercises:
            # Par type
            ex_type = exercise.get('type', 'unknown')
            stats["by_type"][ex_type] = stats["by_type"].get(ex_type, 0) + 1
            
            # Par difficulté
            difficulty = exercise.get('difficulty', 'unknown')
            stats["by_difficulty"][difficulty] = stats["by_difficulty"].get(difficulty, 0) + 1
            
            # Avec explications
            if exercise.get('explanation'):
                stats["with_explanations"] += 1
            
            # Avec options (QCM)
            if exercise.get('options'):
                stats["with_options"] += 1
        
        return stats
    
    def print_statistics(self):
        """Afficher les statistiques"""
        stats = self.get_statistics()
        
        print("\n📊 Statistiques des exercices:")
        print("=" * 40)
        print(f"Total: {stats['total']} exercices")
        
        print("\nPar type:")
        for ex_type, count in stats["by_type"].items():
            print(f"  {ex_type}: {count}")
        
        print("\nPar difficulté:")
        for difficulty, count in stats["by_difficulty"].items():
            print(f"  {difficulty}: {count}")
        
        print(f"\nAvec explications: {stats['with_explanations']}")
        print(f"Avec options (QCM): {stats['with_options']}")


def main():
    """Interface en ligne de commande"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Formateur d\'exercices pour Mathia')
    parser.add_argument('--input', help='Fichier texte à parser')
    parser.add_argument('--output', help='Fichier JSON de sortie')
    parser.add_argument('--preview', action='store_true', help='Aperçu des exercices')
    parser.add_argument('--stats', action='store_true', help='Afficher les statistiques')
    
    args = parser.parse_args()
    
    formatter = ExerciseFormatter()
    
    if args.input:
        # Parser depuis un fichier
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
        
        count = formatter.parse_from_text(text)
        print(f"✅ {count} exercices parsés depuis {args.input}")
    
    if args.preview:
        formatter.preview()
    
    if args.stats:
        formatter.print_statistics()
    
    if args.output:
        formatter.save_to_file(args.output)
    
    # Mode interactif si aucun argument
    if not any([args.input, args.output, args.preview, args.stats]):
        print("🛠️  Mode interactif - Formateur d'exercices")
        print("=" * 50)
        
        while True:
            print("\nOptions disponibles:")
            print("1. Ajouter un exercice QCM")
            print("2. Ajouter un exercice de calcul")
            print("3. Ajouter un exercice vrai/faux")
            print("4. Parser depuis un texte")
            print("5. Aperçu des exercices")
            print("6. Statistiques")
            print("7. Sauvegarder")
            print("8. Quitter")
            
            choice = input("\nVotre choix (1-8): ").strip()
            
            if choice == "1":
                question = input("Question: ")
                correct = input("Réponse correcte (A/B/C/D): ").upper()
                options = {}
                for letter in ['A', 'B', 'C', 'D']:
                    option = input(f"Option {letter}: ")
                    options[letter] = option
                
                explanation = input("Explication (optionnel): ")
                formatter.add_qcm_exercise(question, correct, options, explanation or None)
                print("✅ Exercice QCM ajouté")
            
            elif choice == "2":
                problem = input("Problème: ")
                solution = input("Solution: ")
                explanation = input("Explication (optionnel): ")
                formatter.add_calculation_exercise(problem, solution, explanation or None)
                print("✅ Exercice de calcul ajouté")
            
            elif choice == "3":
                statement = input("Énoncé: ")
                is_true = input("Vrai ou Faux? (v/f): ").lower() == 'v'
                explanation = input("Explication (optionnel): ")
                formatter.add_true_false_exercise(statement, is_true, explanation or None)
                print("✅ Exercice vrai/faux ajouté")
            
            elif choice == "4":
                text = input("Collez le texte à parser: ")
                count = formatter.parse_from_text(text)
                print(f"✅ {count} exercices parsés")
            
            elif choice == "5":
                formatter.preview()
            
            elif choice == "6":
                formatter.print_statistics()
            
            elif choice == "7":
                filename = input("Nom du fichier: ")
                formatter.save_to_file(filename)
            
            elif choice == "8":
                break
            
            else:
                print("❌ Choix invalide")


if __name__ == '__main__':
    main()

