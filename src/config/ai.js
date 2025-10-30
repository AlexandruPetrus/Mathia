require('dotenv').config();

const aiConfig = {
  openaiApiKey: process.env.OPENAI_API_KEY,
  model: 'gpt-4',
  temperature: 0.7,
  maxTokens: 2000,
  
  // Configuration pour la génération d'exercices
  exerciseGeneration: {
    promptTemplate: `Tu es un professeur de mathématiques pour collégiens français.
Génère un exercice de mathématiques pour le niveau {grade} sur le thème "{topic}".

L'exercice doit inclure:
1. Un énoncé clair et pédagogique
2. Une question précise
3. La réponse correcte
4. Une explication détaillée de la solution
5. Le niveau de difficulté (facile, moyen, difficile)

Format JSON attendu:
{
  "title": "Titre de l'exercice",
  "description": "Énoncé complet",
  "question": "Question à résoudre",
  "answer": "Réponse correcte",
  "explanation": "Explication détaillée de la solution",
  "difficulty": "facile|moyen|difficile",
  "points": 10
}`,
    
    grades: ['6ème', '5ème', '4ème', '3ème'],
    topics: [
      'Arithmétique',
      'Algèbre',
      'Géométrie',
      'Fractions',
      'Équations',
      'Proportionnalité',
      'Probabilités',
      'Statistiques',
      'Fonctions',
      'Théorème de Pythagore'
    ],
    difficulties: ['facile', 'moyen', 'difficile']
  }
};

module.exports = aiConfig;


