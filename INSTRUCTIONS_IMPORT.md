# Instructions d'Import - Fichiers SQL Petits

## Fichiers Créés
Les exercices ont été organisés en fichiers séparés pour éviter les problèmes de taille.

## Ordre d'Exécution dans Supabase SQL Editor

### Étape 1: Schéma de Base
**01_schema.sql** - Exécutez ce fichier EN PREMIER
- Crée les types et tables nécessaires
- Gère les types existants automatiquement

### Étape 2: Cours
**02_courses.sql** - Crée les 9 cours de 6ème

### Étape 3: Exercices par Chapitre
Exécutez les fichiers dans l'ordre :

**03_chapitre_01.sql** (2.9 MB, 2595 exercices)
**03_chapitre_02.sql** (0.1 MB, 72 exercices)
**03_chapitre_03.sql** (0.4 MB, 79 exercices)
**03_chapitre_04.sql** (0.0 MB, 32 exercices)
**03_chapitre_05.sql** (0.0 MB, 24 exercices)
**03_chapitre_06.sql** (0.5 MB, 295 exercices)
**03_chapitre_07.sql** (0.1 MB, 100 exercices)
**03_chapitre_08.sql** (0.2 MB, 187 exercices)
**03_chapitre_09.sql** (0.0 MB, 8 exercices)

### Étape 4: Vérification
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

## Avantages de cette Méthode
- ✅ Fichiers petits (pas de problème de taille)
- ✅ Encodage UTF-8 correct
- ✅ Import par chapitre (plus de contrôle)
- ✅ Gestion des erreurs par fichier

## Résultat Attendu
- 9 cours (chapitres 6ème)
- 3 392 exercices importés
- Bibliothèque complète prête à utiliser
