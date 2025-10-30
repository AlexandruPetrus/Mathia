# 🤖 Guide de génération d'exercices avec IA

Ce guide explique comment générer automatiquement des exercices de mathématiques avec OpenAI.

## 📋 Prérequis

### 1. Clé API OpenAI

Obtenez une clé API sur https://platform.openai.com/api-keys

Ajoutez-la à votre fichier `.env` :
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. Dépendances Python

```bash
pip install openai python-dotenv psycopg2-binary
```

## 🚀 Génération d'exercices

### Commande de base

```bash
python scripts/ai_generate_exercises.py \
  --chapter "Les fractions" \
  --grade "6ème" \
  --difficulty "facile" \
  --type "qcm" \
  --count 10
```

### Paramètres

| Paramètre | Description | Valeurs possibles |
|-----------|-------------|-------------------|
| `--chapter` | Titre du chapitre | Texte libre |
| `--grade` | Niveau scolaire | 6ème, 5ème, 4ème, 3ème |
| `--difficulty` | Difficulté | facile, moyen, difficile |
| `--type` | Type d'exercice | qcm, libre, vrai-faux, calcul |
| `--count` | Nombre d'exercices | Nombre (défaut: 10) |
| `--output` | Fichier de sortie | Chemin (défaut: backend/data/generated_exercises.json) |

## 📝 Exemples d'utilisation

### Exercices QCM sur les fractions (6ème)

```bash
python scripts/ai_generate_exercises.py \
  --chapter "Les fractions" \
  --grade "6ème" \
  --difficulty "facile" \
  --type "qcm" \
  --count 10
```

### Exercices libres sur les équations (3ème)

```bash
python scripts/ai_generate_exercises.py \
  --chapter "Équations du premier degré" \
  --grade "3ème" \
  --difficulty "difficile" \
  --type "libre" \
  --count 5
```

### Exercices moyens sur la géométrie (4ème)

```bash
python scripts/ai_generate_exercises.py \
  --chapter "Théorème de Pythagore" \
  --grade "4ème" \
  --difficulty "moyen" \
  --type "calcul" \
  --count 8
```

### Vrai-Faux sur les probabilités (5ème)

```bash
python scripts/ai_generate_exercises.py \
  --chapter "Introduction aux probabilités" \
  --grade "5ème" \
  --difficulty "facile" \
  --type "vrai-faux" \
  --count 15
```

## 📂 Fichiers générés

Les exercices sont sauvegardés dans :
```
backend/data/generated_exercises.json
```

**Format :**
```json
[
  {
    "id": "ex-1",
    "type": "qcm",
    "body": "Quelle est la fraction équivalente à 2/3 ?",
    "options": ["3/4", "4/6", "5/6", "1/3"],
    "answer": "4/6",
    "explanation": "On multiplie numérateur et dénominateur par 2.",
    "difficulty": "facile",
    "tags": ["fractions", "équivalence"]
  },
  {
    "id": "ex-2",
    "type": "qcm",
    "body": "Quelle fraction est irréductible ?",
    "options": ["2/4", "3/9", "5/7", "6/8"],
    "answer": "5/7",
    "explanation": "5 et 7 n'ont pas de diviseur commun autre que 1.",
    "difficulty": "moyen",
    "tags": ["fractions", "simplification"]
  }
]
```

## 📥 Import dans la base de données

### Méthode 1 : Via le script d'import

```bash
python scripts/import_exercises.py \
  --file backend/data/generated_exercises.json \
  --course-id 1
```

Ce script :
1. ✅ Se connecte à PostgreSQL
2. ✅ Vérifie que le cours existe
3. ✅ Importe tous les exercices
4. ✅ Convertit les options en format JSON
5. ✅ Affiche un résumé

### Méthode 2 : Via l'API REST

```bash
# Pour chaque exercice du fichier JSON
curl -X POST http://localhost:3000/api/admin/exercises \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "courseId": 1,
    "type": "qcm",
    "body": "Quelle est la fraction équivalente à 2/3 ?",
    "options": {"A": "3/4", "B": "4/6", "C": "5/6", "D": "1/3"},
    "answer": "B",
    "explanation": "On multiplie numérateur et dénominateur par 2.",
    "difficulty": "facile",
    "tags": ["fractions", "équivalence"]
  }'
```

## 🎯 Workflow complet

### 1. Créer un cours (si nécessaire)

```sql
INSERT INTO courses (title, grade, chapter, description, "createdAt", "updatedAt")
VALUES ('Les fractions', '6ème', 'Arithmétique', 'Apprendre les fractions simples', NOW(), NOW())
RETURNING id;
```

Ou via SQL direct :
```bash
psql -U postgres -d mathia_db -c "INSERT INTO courses (title, grade, chapter, description, \"createdAt\", \"updatedAt\") VALUES ('Les fractions', '6ème', 'Arithmétique', 'Apprendre les fractions', NOW(), NOW()) RETURNING id;"
```

### 2. Générer les exercices avec IA

```bash
python scripts/ai_generate_exercises.py \
  --chapter "Les fractions" \
  --grade "6ème" \
  --difficulty "facile" \
  --type "qcm" \
  --count 10
```

### 3. Vérifier le fichier généré

```bash
cat backend/data/generated_exercises.json
```

### 4. Importer en base de données

```bash
python scripts/import_exercises.py \
  --file backend/data/generated_exercises.json \
  --course-id 1
```

### 5. Vérifier via l'API

```bash
curl http://localhost:3000/api/exercises?courseId=1 \
  -H "Authorization: Bearer $TOKEN"
```

## ⚙️ Configuration du prompt

Le template de prompt se trouve dans `docs/ai_prompts.json` :

```json
{
  "generate_exercises": {
    "instruction": "Tu es un générateur d'exercices...",
    "example_output": {
      "id": "uuid",
      "type": "qcm",
      "body": "...",
      "options": ["...", "..."],
      "answer": "...",
      "explanation": "...",
      "difficulty": "...",
      "tags": ["..."]
    }
  }
}
```

Vous pouvez modifier ce fichier pour personnaliser les instructions données à l'IA.

## 📊 Résumé des exercices générés

Le script affiche automatiquement un résumé :

```
============================================================
📋 RÉSUMÉ DES EXERCICES GÉNÉRÉS
============================================================

Exercice 1:
  • ID: ex-1
  • Type: qcm
  • Difficulté: facile
  • Question: Quelle est la fraction équivalente à 2/3 ?...
  • Réponse: 4/6
  • Tags: fractions, équivalence

Exercice 2:
  • ID: ex-2
  • Type: qcm
  • Difficulté: moyen
  • Question: Quelle fraction est irréductible ?...
  • Réponse: 5/7
  • Tags: fractions, simplification
```

## 💡 Conseils

### Qualité des exercices

- ✅ Utilisez des chapitres précis : "Les fractions" au lieu de "Maths"
- ✅ Spécifiez le niveau et la difficulté appropriés
- ✅ Générez plusieurs fois pour avoir de la diversité
- ✅ Vérifiez toujours les exercices générés avant import

### Optimisation des coûts

- 💰 Le modèle GPT-4 est plus cher mais génère de meilleurs exercices
- 💰 Générez par lots de 10-15 exercices maximum
- 💰 Réutilisez les exercices générés plutôt que de régénérer

### Personnalisation

Éditez `docs/ai_prompts.json` pour :
- Changer le style des exercices
- Ajouter des contraintes spécifiques
- Modifier le format de sortie

## 🐛 Dépannage

### "OPENAI_API_KEY non configurée"

Vérifiez votre fichier `.env` :
```bash
cat .env | grep OPENAI_API_KEY
```

### "Erreur de parsing JSON"

L'IA a retourné un format invalide. Réessayez ou ajustez le prompt.

### "Cours non trouvé" lors de l'import

Créez d'abord le cours ou vérifiez l'ID :
```sql
SELECT id, title FROM courses;
```

### Exercices de mauvaise qualité

- Ajustez la température (dans le script, ligne ~110)
- Modifiez le prompt dans `docs/ai_prompts.json`
- Essayez un autre modèle (gpt-3.5-turbo est plus rapide mais moins bon)

## 📚 Ressources

- **OpenAI API Docs** : https://platform.openai.com/docs
- **Pricing** : https://openai.com/pricing
- **Best Practices** : https://platform.openai.com/docs/guides/prompt-engineering

---

🎉 **Vous êtes prêt à générer des exercices avec l'IA !**









