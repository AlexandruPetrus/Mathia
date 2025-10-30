# Instructions d'Import - Fichier Divisé

## Fichier Original
mathia_final_safe.sql (6.1 MB)

## Parties Créées
Le fichier a été divisé en 4 parties pour éviter l'erreur "Query is too large".

## Ordre d'Exécution dans Supabase SQL Editor

### Étape 1: Préparation
Assurez-vous que le schéma de base existe :
- Si c'est la première fois, exécutez d'abord: supabase/schema.sql
- Sinon, passez directement à l'étape 2

### Étape 2: Import des Parties
Exécutez les parties dans l'ordre suivant :

**1. mathia_final_safe_part_01.sql** (2.0 MB)
**2. mathia_final_safe_part_02.sql** (2.0 MB)
**3. mathia_final_safe_part_03.sql** (2.0 MB)
**4. mathia_final_safe_part_04.sql** (0.0 MB)

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
