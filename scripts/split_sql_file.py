#!/usr/bin/env python3
"""
Script pour diviser le fichier SQL en parties plus petites
pour éviter l'erreur "Query is too large" dans Supabase
"""

import os
import sys

def split_sql_file(input_file: str, max_size_mb: float = 2.0):
    """Diviser un fichier SQL en parties plus petites"""
    
    if not os.path.exists(input_file):
        print(f"[ERROR] Fichier non trouve: {input_file}")
        return
    
    # Taille maximale en bytes (2 MB par défaut)
    max_size_bytes = int(max_size_mb * 1024 * 1024)
    
    print(f"[INFO] Division du fichier {input_file}")
    print(f"[INFO] Taille maximale par partie: {max_size_mb} MB")
    
    # Essayer différents encodages
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    content = None
    
    for encoding in encodings:
        try:
            with open(input_file, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"[INFO] Fichier lu avec l'encodage: {encoding}")
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        print(f"[ERROR] Impossible de lire le fichier avec les encodages testés")
        return
    
    total_size = len(content.encode('utf-8'))
    print(f"[INFO] Taille totale: {total_size / (1024*1024):.1f} MB")
    
    # Diviser le contenu en parties
    parts = []
    current_part = ""
    current_size = 0
    part_number = 1
    
    # Diviser par lignes pour éviter de couper au milieu d'une instruction SQL
    lines = content.split('\n')
    
    for line in lines:
        line_size = len(line.encode('utf-8'))
        
        # Si ajouter cette ligne dépasse la taille max, sauvegarder la partie actuelle
        if current_size + line_size > max_size_bytes and current_part:
            parts.append(current_part)
            current_part = ""
            current_size = 0
            part_number += 1
        
        current_part += line + '\n'
        current_size += line_size
    
    # Ajouter la dernière partie
    if current_part:
        parts.append(current_part)
    
    print(f"[INFO] Fichier divise en {len(parts)} parties")
    
    # Sauvegarder les parties
    base_name = os.path.splitext(input_file)[0]
    
    for i, part in enumerate(parts, 1):
        output_file = f"{base_name}_part_{i:02d}.sql"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(part)
        
        part_size = len(part.encode('utf-8'))
        print(f"[OK] Partie {i}: {output_file} ({part_size / (1024*1024):.1f} MB)")
    
    # Créer un fichier d'instructions
    instructions = f"""# Instructions d'Import - Fichier Divisé

## Fichier Original
{input_file} ({total_size / (1024*1024):.1f} MB)

## Parties Créées
Le fichier a été divisé en {len(parts)} parties pour éviter l'erreur "Query is too large".

## Ordre d'Exécution dans Supabase SQL Editor

### Étape 1: Préparation
Assurez-vous que le schéma de base existe :
- Si c'est la première fois, exécutez d'abord: supabase/schema.sql
- Sinon, passez directement à l'étape 2

### Étape 2: Import des Parties
Exécutez les parties dans l'ordre suivant :

"""
    
    for i in range(1, len(parts) + 1):
        part_file = f"{base_name}_part_{i:02d}.sql"
        part_size = len(parts[i-1].encode('utf-8'))
        instructions += f"**{i}. {part_file}** ({part_size / (1024*1024):.1f} MB)\n"
    
    instructions += f"""
### Étape 3: Vérification
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

## Résultat Attendu
- 9 cours (chapitres 6ème)
- 3 392 exercices importés
- Bibliothèque complète prête à utiliser
"""
    
    instructions_file = f"{base_name}_INSTRUCTIONS.md"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"[SUCCESS] Instructions creees: {instructions_file}")
    print(f"[INFO] Executez les parties dans l'ordre indique dans {instructions_file}")

def main():
    """Fonction principale"""
    print('=' * 60)
    print('DIVISEUR DE FICHIER SQL - MATHIA')
    print('=' * 60)
    print()
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        max_size = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    else:
        input_file = "mathia_final_safe.sql"
        max_size = 2.0
    
    split_sql_file(input_file, max_size)

if __name__ == '__main__':
    main()
