#!/usr/bin/env python3
"""
Script corrigé pour diviser le fichier SQL en parties plus petites
Gère correctement l'encodage UTF-8
"""

import os
import sys

def split_sql_file_fixed(input_file: str, max_size_mb: float = 1.5):
    """Diviser un fichier SQL en parties plus petites avec encodage correct"""
    
    if not os.path.exists(input_file):
        print(f"[ERROR] Fichier non trouvé: {input_file}")
        return
    
    # Taille maximale en bytes (1.5 MB par défaut pour être sûr)
    max_size_bytes = int(max_size_mb * 1024 * 1024)
    
    print(f"[INFO] Division du fichier {input_file}")
    print(f"[INFO] Taille maximale par partie: {max_size_mb} MB")
    
    # Lire le fichier avec encodage UTF-8
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Essayer avec latin-1 si UTF-8 échoue
        try:
            with open(input_file, 'r', encoding='latin-1') as f:
                content = f.read()
            print("[INFO] Fichier lu avec l'encodage latin-1")
        except Exception as e:
            print(f"[ERROR] Impossible de lire le fichier: {e}")
            return
    except Exception as e:
        print(f"[ERROR] Erreur lecture fichier: {e}")
        return
    
    total_size = len(content.encode('utf-8'))
    print(f"[INFO] Taille totale: {total_size / (1024*1024):.1f} MB")
    
    # Diviser le contenu en parties intelligentes
    parts = []
    current_part = ""
    current_size = 0
    part_number = 1
    
    # Diviser par lignes pour éviter de couper au milieu d'une instruction SQL
    lines = content.split('\n')
    
    for line in lines:
        line_with_newline = line + '\n'
        line_size = len(line_with_newline.encode('utf-8'))
        
        # Si ajouter cette ligne dépasse la taille max, sauvegarder la partie actuelle
        if current_size + line_size > max_size_bytes and current_part:
            parts.append(current_part)
            current_part = ""
            current_size = 0
            part_number += 1
        
        current_part += line_with_newline
        current_size += line_size
    
    # Ajouter la dernière partie
    if current_part:
        parts.append(current_part)
    
    print(f"[INFO] Fichier divisé en {len(parts)} parties")
    
    # Sauvegarder les parties avec encodage UTF-8
    base_name = os.path.splitext(input_file)[0]
    
    for i, part in enumerate(parts, 1):
        output_file = f"{base_name}_part_{i:02d}.sql"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(part)
            
            part_size = len(part.encode('utf-8'))
            print(f"[OK] Partie {i}: {output_file} ({part_size / (1024*1024):.1f} MB)")
        except Exception as e:
            print(f"[ERROR] Erreur sauvegarde partie {i}: {e}")
    
    # Créer un fichier d'instructions
    create_instructions(base_name, len(parts), total_size)

def create_instructions(base_name: str, num_parts: int, total_size: int):
    """Créer le fichier d'instructions"""
    instructions = f"""# Instructions d'Import - Fichier Divisé (Version Corrigée)

## Fichier Original
{base_name}.sql ({total_size / (1024*1024):.1f} MB)

## Parties Créées
Le fichier a été divisé en {num_parts} parties pour éviter l'erreur "Query is too large".

## Ordre d'Exécution dans Supabase SQL Editor

### Étape 1: Préparation
Assurez-vous que le schéma de base existe :
- Si c'est la première fois, exécutez d'abord: supabase/schema.sql
- Sinon, passez directement à l'étape 2

### Étape 2: Import des Parties
Exécutez les parties dans l'ordre suivant :

"""
    
    for i in range(1, num_parts + 1):
        part_file = f"{base_name}_part_{i:02d}.sql"
        instructions += f"**{i}. {part_file}**\n"
        instructions += f"   - Copiez-collez le contenu dans le SQL Editor\n"
        instructions += f"   - Cliquez sur 'Run' pour exécuter\n"
        instructions += f"   - Attendez la fin avant de passer à la partie suivante\n\n"
    
    instructions += f"""### Étape 3: Vérification
Après avoir exécuté toutes les parties, vérifiez l'import :

```sql
-- Vérifier le nombre total d'exercices
SELECT COUNT(*) as total_exercices FROM public.exercises;

-- Vérifier par chapitre
SELECT 
    c.title as chapitre,
    COUNT(e.id) as exercices
FROM public.courses c
LEFT JOIN public.exercises e ON c.id = e.course_id
GROUP BY c.id, c.title
ORDER BY c.order_num;
```

## Notes Importantes
- Exécutez les parties **dans l'ordre** (part_01, part_02, etc.)
- Chaque partie peut prendre quelques minutes à s'exécuter
- Ne pas interrompre l'exécution d'une partie
- Si une partie échoue, relancez-la avant de passer à la suivante
- Les fichiers sont maintenant en encodage UTF-8 correct

## Résultat Attendu
- 9 cours (chapitres 6ème)
- 3 392 exercices importés
- Bibliothèque complète prête à utiliser

## Dépannage
Si vous voyez encore des caractères "NUL" :
1. Fermez et rouvrez le fichier
2. Vérifiez que votre éditeur utilise l'encodage UTF-8
3. Utilisez l'alternative : scripts/import_via_api_safe.py
"""
    
    instructions_file = f"{base_name}_INSTRUCTIONS_FIXED.md"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"[SUCCESS] Instructions corrigées créées: {instructions_file}")

def main():
    """Fonction principale"""
    print('=' * 60)
    print('DIVISEUR DE FICHIER SQL CORRIGÉ - MATHIA')
    print('=' * 60)
    print()
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        max_size = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5
    else:
        input_file = "mathia_final_safe.sql"
        max_size = 1.5
    
    split_sql_file_fixed(input_file, max_size)

if __name__ == '__main__':
    main()


