# Instructions d'Import - Fichier Divisé (Version Corrigée)

## Fichier Original
mathia_final_safe.sql (6.1 MB)

## Parties Créées
Le fichier a été divisé en 5 parties pour éviter l'erreur "Query is too large".

## Ordre d'Exécution dans Supabase SQL Editor

### Étape 1: Préparation
Assurez-vous que le schéma de base existe :
- Si c'est la première fois, exécutez d'abord: supabase/schema.sql
- Sinon, passez directement à l'étape 2

### Étape 2: Import des Parties
Exécutez les parties dans l'ordre suivant :

**1. mathia_final_safe_part_01.sql**
   - Copiez-collez le contenu dans le SQL Editor
   - Cliquez sur 'Run' pour exécuter
   - Attendez la fin avant de passer à la partie suivante

**2. mathia_final_safe_part_02.sql**
   - Copiez-collez le contenu dans le SQL Editor
   - Cliquez sur 'Run' pour exécuter
   - Attendez la fin avant de passer à la partie suivante

**3. mathia_final_safe_part_03.sql**
   - Copiez-collez le contenu dans le SQL Editor
   - Cliquez sur 'Run' pour exécuter
   - Attendez la fin avant de passer à la partie suivante

**4. mathia_final_safe_part_04.sql**
   - Copiez-collez le contenu dans le SQL Editor
   - Cliquez sur 'Run' pour exécuter
   - Attendez la fin avant de passer à la partie suivante

**5. mathia_final_safe_part_05.sql**
   - Copiez-collez le contenu dans le SQL Editor
   - Cliquez sur 'Run' pour exécuter
   - Attendez la fin avant de passer à la partie suivante

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
