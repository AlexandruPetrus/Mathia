#!/usr/bin/env python3
"""
Validateur d'exercices pour Mathia
Vérifie la qualité et la cohérence des exercices importés
"""

import json
import re
from typing import List, Dict, Any, Tuple, Optional


class ExerciseValidator:
    """Validateur d'exercices pour Mathia"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.validated_exercises = []
    
    def validate_exercise(self, exercise: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Valider un exercice individuel"""
        errors = []
        warnings = []
        
        # Vérifications obligatoires
        if not exercise.get('body'):
            errors.append("L'énoncé de l'exercice est requis")
        
        if not exercise.get('answer'):
            errors.append("La réponse est requise")
        
        if not exercise.get('type'):
            errors.append("Le type d'exercice est requis")
        elif exercise['type'] not in ['qcm', 'libre', 'vrai-faux', 'calcul']:
            errors.append(f"Type d'exercice invalide: {exercise['type']}")
        
        # Vérifications spécifiques par type
        exercise_type = exercise.get('type', '')
        
        if exercise_type == 'qcm':
            errors.extend(self._validate_qcm(exercise))
        elif exercise_type == 'vrai-faux':
            errors.extend(self._validate_true_false(exercise))
        elif exercise_type == 'calcul':
            errors.extend(self._validate_calculation(exercise))
        
        # Vérifications de qualité
        warnings.extend(self._validate_quality(exercise))
        
        return len(errors) == 0, errors, warnings
    
    def _validate_qcm(self, exercise: Dict[str, Any]) -> List[str]:
        """Valider un exercice QCM"""
        errors = []
        
        options = exercise.get('options')
        if not options:
            errors.append("Les options sont requises pour un QCM")
        elif not isinstance(options, dict):
            errors.append("Les options doivent être un objet JSON")
        else:
            # Vérifier les clés des options
            expected_keys = ['A', 'B', 'C', 'D']
            actual_keys = list(options.keys())
            
            if not all(key in actual_keys for key in expected_keys):
                errors.append(f"Options manquantes. Attendu: {expected_keys}, Reçu: {actual_keys}")
            
            # Vérifier que la réponse correspond à une option
            answer = exercise.get('answer', '').upper()
            if answer not in actual_keys:
                errors.append(f"La réponse '{answer}' ne correspond à aucune option")
            
            # Vérifier que les options ne sont pas vides
            for key, value in options.items():
                if not value or not value.strip():
                    errors.append(f"L'option {key} est vide")
        
        return errors
    
    def _validate_true_false(self, exercise: Dict[str, Any]) -> List[str]:
        """Valider un exercice vrai/faux"""
        errors = []
        
        answer = exercise.get('answer', '').lower()
        if answer not in ['vrai', 'faux', 'true', 'false']:
            errors.append("La réponse doit être 'Vrai' ou 'Faux'")
        
        return errors
    
    def _validate_calculation(self, exercise: Dict[str, Any]) -> List[str]:
        """Valider un exercice de calcul"""
        errors = []
        
        body = exercise.get('body', '')
        answer = exercise.get('answer', '')
        
        # Vérifier la présence de termes mathématiques
        math_terms = ['calculer', 'résoudre', 'trouver', 'déterminer', 'évaluer']
        if not any(term in body.lower() for term in math_terms):
            errors.append("L'énoncé d'un exercice de calcul doit contenir un verbe d'action mathématique")
        
        # Vérifier que la réponse contient des éléments mathématiques
        if not re.search(r'[\d\+\-\*/\=\(\)]', answer):
            errors.append("La réponse d'un exercice de calcul doit contenir des éléments mathématiques")
        
        return errors
    
    def _validate_quality(self, exercise: Dict[str, Any]) -> List[str]:
        """Valider la qualité générale de l'exercice"""
        warnings = []
        
        body = exercise.get('body', '')
        answer = exercise.get('answer', '')
        explanation = exercise.get('explanation', '')
        
        # Longueur de l'énoncé
        if len(body) < 10:
            warnings.append("L'énoncé semble trop court")
        elif len(body) > 500:
            warnings.append("L'énoncé semble très long")
        
        # Présence d'explication
        if not explanation:
            warnings.append("Aucune explication fournie")
        elif len(explanation) < 10:
            warnings.append("L'explication semble trop courte")
        
        # Difficulté
        difficulty = exercise.get('difficulty', '')
        if not difficulty:
            warnings.append("Aucune difficulté spécifiée")
        elif difficulty not in ['facile', 'moyen', 'difficile']:
            warnings.append(f"Difficulté non standard: {difficulty}")
        
        # Tags
        tags = exercise.get('tags', [])
        if not tags:
            warnings.append("Aucun tag fourni pour catégoriser l'exercice")
        
        # Cohérence réponse/énoncé
        if body and answer:
            # Vérifier si la réponse est trop similaire à l'énoncé
            if answer.lower() in body.lower() and len(answer) > 5:
                warnings.append("La réponse semble contenue dans l'énoncé")
        
        return warnings
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Valider un fichier d'exercices"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                exercises = json.load(f)
            
            if not isinstance(exercises, list):
                exercises = [exercises]
            
            return self.validate_exercises(exercises)
            
        except FileNotFoundError:
            return {
                'valid': False,
                'errors': [f"Fichier non trouvé: {file_path}"],
                'warnings': [],
                'statistics': {}
            }
        except json.JSONDecodeError as e:
            return {
                'valid': False,
                'errors': [f"Erreur de format JSON: {e}"],
                'warnings': [],
                'statistics': {}
            }
    
    def validate_exercises(self, exercises: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Valider une liste d'exercices"""
        self.errors = []
        self.warnings = []
        self.validated_exercises = []
        
        valid_count = 0
        invalid_count = 0
        
        for i, exercise in enumerate(exercises, 1):
            is_valid, errors, warnings = self.validate_exercise(exercise)
            
            if is_valid:
                valid_count += 1
                self.validated_exercises.append(exercise)
            else:
                invalid_count += 1
                self.errors.extend([f"Exercice {i}: {error}" for error in errors])
            
            self.warnings.extend([f"Exercice {i}: {warning}" for warning in warnings])
        
        # Générer des statistiques
        statistics = self._generate_statistics(exercises)
        
        return {
            'valid': invalid_count == 0,
            'valid_count': valid_count,
            'invalid_count': invalid_count,
            'total_count': len(exercises),
            'errors': self.errors,
            'warnings': self.warnings,
            'statistics': statistics,
            'validated_exercises': self.validated_exercises
        }
    
    def _generate_statistics(self, exercises: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Générer des statistiques sur les exercices"""
        stats = {
            'total': len(exercises),
            'by_type': {},
            'by_difficulty': {},
            'with_explanations': 0,
            'with_tags': 0,
            'average_body_length': 0,
            'average_explanation_length': 0
        }
        
        total_body_length = 0
        total_explanation_length = 0
        explanations_count = 0
        
        for exercise in exercises:
            # Par type
            ex_type = exercise.get('type', 'unknown')
            stats['by_type'][ex_type] = stats['by_type'].get(ex_type, 0) + 1
            
            # Par difficulté
            difficulty = exercise.get('difficulty', 'unknown')
            stats['by_difficulty'][difficulty] = stats['by_difficulty'].get(difficulty, 0) + 1
            
            # Avec explications
            if exercise.get('explanation'):
                stats['with_explanations'] += 1
                total_explanation_length += len(exercise['explanation'])
                explanations_count += 1
            
            # Avec tags
            if exercise.get('tags'):
                stats['with_tags'] += 1
            
            # Longueur moyenne
            body = exercise.get('body', '')
            total_body_length += len(body)
        
        # Calculer les moyennes
        if exercises:
            stats['average_body_length'] = round(total_body_length / len(exercises), 1)
        
        if explanations_count > 0:
            stats['average_explanation_length'] = round(total_explanation_length / explanations_count, 1)
        
        return stats
    
    def fix_common_issues(self, exercises: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Corriger automatiquement les problèmes courants"""
        fixed_exercises = []
        
        for exercise in exercises:
            fixed_exercise = exercise.copy()
            
            # Corriger la casse des types
            ex_type = fixed_exercise.get('type', '').lower()
            if ex_type in ['qcm', 'libre', 'vrai-faux', 'calcul']:
                fixed_exercise['type'] = ex_type
            
            # Corriger la casse des difficultés
            difficulty = fixed_exercise.get('difficulty', '').lower()
            if difficulty in ['facile', 'moyen', 'difficile']:
                fixed_exercise['difficulty'] = difficulty
            
            # Nettoyer les espaces
            for field in ['body', 'answer', 'explanation']:
                if field in fixed_exercise and fixed_exercise[field]:
                    fixed_exercise[field] = ' '.join(fixed_exercise[field].split())
            
            # Corriger les réponses vrai/faux
            if fixed_exercise.get('type') == 'vrai-faux':
                answer = fixed_exercise.get('answer', '').lower()
                if answer in ['true', '1', 'oui', 'o']:
                    fixed_exercise['answer'] = 'Vrai'
                elif answer in ['false', '0', 'non', 'n']:
                    fixed_exercise['answer'] = 'Faux'
            
            # Ajouter des tags par défaut si manquants
            if not fixed_exercise.get('tags'):
                fixed_exercise['tags'] = ['imported']
            
            # Ajouter une difficulté par défaut
            if not fixed_exercise.get('difficulty'):
                fixed_exercise['difficulty'] = 'moyen'
            
            fixed_exercises.append(fixed_exercise)
        
        return fixed_exercises
    
    def generate_report(self, validation_result: Dict[str, Any]) -> str:
        """Générer un rapport de validation"""
        report = []
        report.append("=" * 60)
        report.append("📊 RAPPORT DE VALIDATION DES EXERCICES")
        report.append("=" * 60)
        report.append("")
        
        # Résumé
        report.append("📋 RÉSUMÉ:")
        report.append(f"   Total d'exercices: {validation_result['total_count']}")
        report.append(f"   ✅ Valides: {validation_result['valid_count']}")
        report.append(f"   ❌ Invalides: {validation_result['invalid_count']}")
        report.append(f"   ⚠️  Avertissements: {len(validation_result['warnings'])}")
        report.append("")
        
        # Statistiques
        stats = validation_result['statistics']
        report.append("📈 STATISTIQUES:")
        report.append(f"   Par type: {stats['by_type']}")
        report.append(f"   Par difficulté: {stats['by_difficulty']}")
        report.append(f"   Avec explications: {stats['with_explanations']}/{stats['total']}")
        report.append(f"   Avec tags: {stats['with_tags']}/{stats['total']}")
        report.append(f"   Longueur moyenne énoncé: {stats['average_body_length']} caractères")
        if stats['average_explanation_length'] > 0:
            report.append(f"   Longueur moyenne explication: {stats['average_explanation_length']} caractères")
        report.append("")
        
        # Erreurs
        if validation_result['errors']:
            report.append("❌ ERREURS:")
            for error in validation_result['errors']:
                report.append(f"   • {error}")
            report.append("")
        
        # Avertissements
        if validation_result['warnings']:
            report.append("⚠️  AVERTISSEMENTS:")
            for warning in validation_result['warnings']:
                report.append(f"   • {warning}")
            report.append("")
        
        # Recommandations
        report.append("💡 RECOMMANDATIONS:")
        if validation_result['invalid_count'] > 0:
            report.append("   • Corriger les erreurs avant l'import")
        if len(validation_result['warnings']) > validation_result['total_count'] * 0.5:
            report.append("   • Améliorer la qualité générale des exercices")
        if stats['with_explanations'] < stats['total'] * 0.8:
            report.append("   • Ajouter des explications pour plus d'exercices")
        if stats['with_tags'] < stats['total'] * 0.5:
            report.append("   • Ajouter des tags pour mieux catégoriser")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    """Interface en ligne de commande"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validateur d\'exercices pour Mathia')
    parser.add_argument('--file', help='Fichier JSON à valider')
    parser.add_argument('--fix', action='store_true', help='Corriger automatiquement les problèmes courants')
    parser.add_argument('--output', help='Fichier de sortie pour les exercices corrigés')
    parser.add_argument('--report', help='Fichier de rapport de validation')
    
    args = parser.parse_args()
    
    if not args.file:
        print("❌ Veuillez spécifier un fichier avec --file")
        return
    
    validator = ExerciseValidator()
    
    # Valider le fichier
    print(f"🔍 Validation du fichier: {args.file}")
    result = validator.validate_file(args.file)
    
    # Afficher le rapport
    report = validator.generate_report(result)
    print(report)
    
    # Sauvegarder le rapport si demandé
    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📄 Rapport sauvegardé: {args.report}")
    
    # Corriger et sauvegarder si demandé
    if args.fix and result['validated_exercises']:
        print("\n🔧 Correction automatique des problèmes...")
        
        # Charger les exercices originaux
        with open(args.file, 'r', encoding='utf-8') as f:
            original_exercises = json.load(f)
        
        if not isinstance(original_exercises, list):
            original_exercises = [original_exercises]
        
        # Corriger
        fixed_exercises = validator.fix_common_issues(original_exercises)
        
        # Sauvegarder
        output_file = args.output or args.file.replace('.json', '_fixed.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fixed_exercises, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Exercices corrigés sauvegardés: {output_file}")
        
        # Re-valider les exercices corrigés
        print("\n🔍 Re-validation des exercices corrigés...")
        fixed_result = validator.validate_exercises(fixed_exercises)
        fixed_report = validator.generate_report(fixed_result)
        print(fixed_report)


if __name__ == '__main__':
    main()

