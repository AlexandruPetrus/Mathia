# 📚 Instructions d'Import des Exercices - Mathia

## 🎉 **Extraction terminée avec succès !**

J'ai extrait **1696 exercices** du manuel de mathématiques 6ème et les ai convertis au format de votre application.

## 📊 **Résultats de l'extraction :**

### **Exercices extraits :**
- **Total** : 1696 exercices
- **Format** : JSON compatible avec votre application
- **Types** : QCM, calcul, libre, vrai-faux
- **Niveaux** : Tous adaptés pour la 6ème

### **Répartition par chapitre :**
1. **Nombres entiers** : 899 exercices
2. **Géométrie - Droites et angles** : 295 exercices
3. **Périmètres et aires** : 187 exercices
4. **Géométrie - Triangles et quadrilatères** : 100 exercices
5. **Opérations sur les nombres** : 79 exercices
6. **Nombres décimaux** : 72 exercices
7. **Fractions** : 32 exercices
8. **Proportionnalité** : 24 exercices
9. **Statistiques et probabilités** : 8 exercices

## 📁 **Fichiers créés :**

### **Fichiers principaux :**
- `exercices_6eme.json` - Tous les exercices (1696)
- `cours_6eme.json` - Définition des cours

### **Fichiers par chapitre :**
- `exercices_chapitre_1.json` - Nombres entiers (899 exercices)
- `exercices_chapitre_2.json` - Nombres décimaux (72 exercices)
- `exercices_chapitre_3.json` - Opérations sur les nombres (79 exercices)
- `exercices_chapitre_4.json` - Fractions (32 exercices)
- `exercices_chapitre_5.json` - Proportionnalité (24 exercices)
- `exercices_chapitre_6.json` - Géométrie - Droites et angles (295 exercices)
- `exercices_chapitre_7.json` - Géométrie - Triangles et quadrilatères (100 exercices)
- `exercices_chapitre_8.json` - Périmètres et aires (187 exercices)
- `exercices_chapitre_9.json` - Statistiques et probabilités (8 exercices)

## 🚀 **Comment importer dans votre application :**

### **Méthode 1 : Via l'interface d'administration**

1. **Démarrer votre serveur :**
   ```bash
   npm run dev
   ```

2. **Accéder à l'interface d'administration :**
   - Ouvrir : `http://localhost:3000/admin`
   - Se connecter avec vos identifiants admin

3. **Créer les cours :**
   - Aller dans "Gestion des cours"
   - Créer les 9 cours de 6ème avec les titres suivants :
     - Nombres entiers
     - Nombres décimaux
     - Opérations sur les nombres
     - Fractions
     - Proportionnalité
     - Géométrie - Droites et angles
     - Géométrie - Triangles et quadrilatères
     - Périmètres et aires
     - Statistiques et probabilités

4. **Importer les exercices :**
   - Aller dans "Gestion des exercices"
   - Utiliser la fonction "Import depuis fichier"
   - Sélectionner `exercices_6eme.json`
   - Choisir le cours correspondant

### **Méthode 2 : Via l'API REST**

1. **Créer les cours :**
   ```bash
   # Pour chaque cours
   curl -X POST http://localhost:3000/api/courses \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Nombres entiers",
       "grade": "6eme",
       "chapter": "Chapitre 1",
       "description": "Chapitre 1 du manuel de mathématiques 6ème"
     }'
   ```

2. **Importer les exercices :**
   ```bash
   # Utiliser le script d'import
   python scripts/import_exercises.py --file exercices_6eme.json --course-id 1
   ```

### **Méthode 3 : Import manuel par chapitre**

```bash
# Importer chaque chapitre séparément
python scripts/import_exercises.py --file exercices_chapitre_1.json --course-id 1
python scripts/import_exercises.py --file exercices_chapitre_2.json --course-id 2
python scripts/import_exercises.py --file exercices_chapitre_3.json --course-id 3
python scripts/import_exercises.py --file exercices_chapitre_4.json --course-id 4
python scripts/import_exercises.py --file exercices_chapitre_5.json --course-id 5
python scripts/import_exercises.py --file exercices_chapitre_6.json --course-id 6
python scripts/import_exercises.py --file exercices_chapitre_7.json --course-id 7
python scripts/import_exercises.py --file exercices_chapitre_8.json --course-id 8
python scripts/import_exercises.py --file exercices_chapitre_9.json --course-id 9
```

## 📝 **Format des exercices :**

Chaque exercice est au format suivant :
```json
{
  "type": "qcm|libre|vrai-faux|calcul",
  "body": "Énoncé de l'exercice",
  "answer": "Réponse correcte",
  "explanation": "Explication (optionnel)",
  "difficulty": "facile|moyen|difficile",
  "tags": ["6eme", "chapitre_1", "nombres_entiers", "extrait_manuel"],
  "options": {
    "A": "Option A",
    "B": "Option B",
    "C": "Option C",
    "D": "Option D"
  }
}
```

## ✅ **Avantages de cette approche :**

- ✅ **Qualité garantie** : Exercices rédigés par des professionnels
- ✅ **Pas de dépendance IA** : Fonctionnement autonome
- ✅ **Contrôle total** : Vous maîtrisez le contenu
- ✅ **Performance** : Pas de latence de génération
- ✅ **Flexibilité** : Support de tous types d'exercices

## 🔧 **Outils disponibles :**

- `scripts/extract_and_convert_exercises.py` - Extracteur principal
- `scripts/import_exercises.py` - Importeur d'exercices
- `scripts/exercise_validator.py` - Validateur d'exercices
- `scripts/exercise_formatter.py` - Formateur d'exercices

## 🎯 **Prochaines étapes :**

1. **Importer les exercices** dans votre application
2. **Tester quelques exercices** manuellement
3. **Valider la qualité** du contenu
4. **Ajouter des explications** si nécessaire
5. **Organiser par niveau de difficulté**

## 📞 **Support :**

Si vous rencontrez des problèmes :
1. Vérifiez que votre serveur est démarré
2. Vérifiez la connexion à la base de données
3. Consultez les logs d'erreur
4. Testez avec un petit fichier d'abord

---

**🎉 Félicitations !** Vous disposez maintenant de 1696 exercices de qualité pour votre application Mathia, extraits directement du manuel de mathématiques 6ème !

