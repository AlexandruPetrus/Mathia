#!/usr/bin/env python3
"""
Script de génération d'exercices de mathématiques via l'API OpenAI
Pour Mathia - Application de révision de mathématiques pour collégiens

Usage:
    python scripts/ai_generate_exercises.py --chapter "Les fractions" --grade "6ème" --difficulty "facile" --type "qcm" --count 10
"""

import os
import sys
import json
import argparse
from pathlib import Path

try:
    import openai
except ImportError:
    print("❌ Le module openai n'est pas installé.")
    print("📦 Installez-le avec: pip install openai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("⚠️  Le module python-dotenv n'est pas installé.")
    print("📦 Installez-le avec: pip install python-dotenv")
    load_dotenv = lambda: None

# Charger les variables d'environnement
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PROMPTS_FILE = 'docs/ai_prompts.json'
OUTPUT_FILE = 'backend/data/generated_exercises.json'


def load_prompt_template():
    """Charger le template de prompt depuis docs/ai_prompts.json"""
    try:
        with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
            prompts = json.load(f)
            return prompts['generate_exercises']
    except FileNotFoundError:
        print(f"❌ Fichier {PROMPTS_FILE} non trouvé")
        sys.exit(1)
    except KeyError:
        print(f"❌ Clé 'generate_exercises' non trouvée dans {PROMPTS_FILE}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de parsing JSON dans {PROMPTS_FILE}: {e}")
        sys.exit(1)


def build_prompt(template, count, chapter_title, grade, difficulty, exercise_type):
    """Construire le prompt à partir du template et des paramètres"""
    instruction = template['instruction']
    example = template['example_output']
    
    # Remplacer les variables dans le template
    instruction = instruction.replace('{{count}}', str(count))
    instruction = instruction.replace('{{chapter_title}}', chapter_title)
    instruction = instruction.replace('{{grade}}', grade)
    instruction = instruction.replace('{{difficulty}}', difficulty)
    instruction = instruction.replace('{{type}}', exercise_type)
    
    # Construire le prompt complet
    prompt = f"""{instruction}

Exemple de format attendu pour un exercice :
{json.dumps(example, indent=2, ensure_ascii=False)}

Génère exactement {count} exercices différents au format JSON.
Réponds UNIQUEMENT avec un tableau JSON valide (array d'objets), sans texte avant ou après.
Format : [{{"id": "...", "type": "...", ...}}, {{"id": "...", ...}}]
"""
    
    return prompt


def generate_exercises_with_openai(prompt, count):
    """Appeler l'API OpenAI pour générer les exercices"""
    
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY non configurée dans .env")
        print("💡 Ajoutez votre clé API OpenAI dans le fichier .env")
        sys.exit(1)
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    print(f"🤖 Appel de l'API OpenAI (modèle: gpt-4)...")
    print(f"📝 Génération de {count} exercices en cours...\n")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "Tu es un expert en pédagogie mathématique pour collégiens français. Tu génères des exercices au format JSON strict."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Nettoyer la réponse (retirer les balises markdown si présentes)
        if content.startswith('```json'):
            content = content[7:]
        elif content.startswith('```'):
            content = content[3:]
        
        if content.endswith('```'):
            content = content[:-3]
        
        content = content.strip()
        
        # Parser le JSON
        exercises = json.loads(content)
        
        # Vérifier que c'est bien un tableau
        if not isinstance(exercises, list):
            print("⚠️  La réponse n'est pas un tableau JSON, tentative d'encapsulation...")
            exercises = [exercises]
        
        print(f"✅ {len(exercises)} exercices générés avec succès\n")
        
        return exercises
        
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de parsing JSON: {e}")
        print(f"Réponse reçue:\n{content}")
        return None
    except Exception as e:
        print(f"❌ Erreur lors de l'appel à OpenAI: {e}")
        return None


def save_exercises(exercises, output_file):
    """Sauvegarder les exercices dans un fichier JSON"""
    
    # Créer le dossier si nécessaire
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(exercises, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Exercices sauvegardés dans: {output_file}")
        print(f"📊 Nombre total d'exercices: {len(exercises)}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False


def display_exercises_summary(exercises):
    """Afficher un résumé des exercices générés"""
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DES EXERCICES GÉNÉRÉS")
    print("="*60 + "\n")
    
    for i, exercise in enumerate(exercises, 1):
        print(f"Exercice {i}:")
        print(f"  • ID: {exercise.get('id', 'N/A')}")
        print(f"  • Type: {exercise.get('type', 'N/A')}")
        print(f"  • Difficulté: {exercise.get('difficulty', 'N/A')}")
        print(f"  • Question: {exercise.get('body', 'N/A')[:60]}...")
        print(f"  • Réponse: {exercise.get('answer', 'N/A')}")
        
        if exercise.get('tags'):
            print(f"  • Tags: {', '.join(exercise.get('tags', []))}")
        
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Générer des exercices de mathématiques avec OpenAI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:

  # Générer 10 exercices QCM sur les fractions (6ème, facile)
  python scripts/ai_generate_exercises.py --chapter "Les fractions" --grade "6ème" --difficulty "facile" --type "qcm" --count 10

  # Générer 5 exercices libres sur les équations (3ème, difficile)
  python scripts/ai_generate_exercises.py --chapter "Les équations" --grade "3ème" --difficulty "difficile" --type "libre" --count 5

  # Générer 15 exercices moyens sur la géométrie
  python scripts/ai_generate_exercises.py --chapter "Géométrie" --grade "4ème" --difficulty "moyen" --type "qcm" --count 15
        """
    )
    
    parser.add_argument(
        '--chapter',
        type=str,
        required=True,
        help='Titre du chapitre (ex: "Les fractions", "Les équations")'
    )
    
    parser.add_argument(
        '--grade',
        type=str,
        required=True,
        choices=['6ème', '5ème', '4ème', '3ème'],
        help='Niveau scolaire'
    )
    
    parser.add_argument(
        '--difficulty',
        type=str,
        required=True,
        choices=['facile', 'moyen', 'difficile'],
        help='Niveau de difficulté'
    )
    
    parser.add_argument(
        '--type',
        type=str,
        required=True,
        choices=['qcm', 'libre', 'vrai-faux', 'calcul'],
        help='Type d\'exercice'
    )
    
    parser.add_argument(
        '--count',
        type=int,
        default=10,
        help='Nombre d\'exercices à générer (défaut: 10)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=OUTPUT_FILE,
        help=f'Fichier de sortie (défaut: {OUTPUT_FILE})'
    )
    
    args = parser.parse_args()
    
    # Afficher les paramètres
    print('🤖 ' + '='*58)
    print('🎓 Générateur d\'exercices Mathia avec OpenAI')
    print('🤖 ' + '='*58)
    print(f"\n📚 Chapitre: {args.chapter}")
    print(f"🎯 Niveau: {args.grade}")
    print(f"📊 Difficulté: {args.difficulty}")
    print(f"📝 Type: {args.type}")
    print(f"🔢 Nombre: {args.count}")
    print(f"💾 Sortie: {args.output}\n")
    
    # Charger le template de prompt
    print("📖 Chargement du template de prompt...")
    template = load_prompt_template()
    print(f"✅ Template chargé depuis {PROMPTS_FILE}\n")
    
    # Construire le prompt
    prompt = build_prompt(
        template,
        args.count,
        args.chapter,
        args.grade,
        args.difficulty,
        args.type
    )
    
    # Générer les exercices avec OpenAI
    exercises = generate_exercises_with_openai(prompt, args.count)
    
    if not exercises:
        print("❌ Échec de la génération des exercices")
        sys.exit(1)
    
    # Afficher le résumé
    display_exercises_summary(exercises)
    
    # Sauvegarder les exercices
    if save_exercises(exercises, args.output):
        print(f"\n✅ Fichier JSON créé avec succès!")
        print(f"📁 Chemin: {os.path.abspath(args.output)}")
        
        # Afficher les prochaines étapes
        print("\n" + "="*60)
        print("📝 PROCHAINES ÉTAPES")
        print("="*60)
        print("\n1. Vérifiez le fichier généré:")
        print(f"   cat {args.output}")
        print("\n2. Pour importer ces exercices en base de données,")
        print("   utilisez l'endpoint POST /admin/exercises")
        print("\n3. Ou créez un script d'import personnalisé")
        print("\n" + "="*60)
        
    else:
        print("\n❌ Erreur lors de la sauvegarde")
        sys.exit(1)


if __name__ == '__main__':
    main()
