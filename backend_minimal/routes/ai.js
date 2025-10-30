const express = require('express');
const router = express.Router();
const { createClient } = require('@supabase/supabase-js');
const OpenAI = require('openai');

// Initialiser Supabase (pour sauvegarder les résultats)
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY // Service key pour contourner RLS
);

// Initialiser OpenAI
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// ============================================
// GÉNÉRATION D'EXERCICES
// ============================================

router.post('/generate-exercises', async (req, res) => {
  try {
    const {
      courseId,
      grade,
      topic,
      difficulty = 'moyen',
      type = 'qcm',
      count = 1
    } = req.body;

    // Validation
    if (!courseId || !grade || !topic) {
      return res.status(400).json({
        success: false,
        message: 'courseId, grade et topic sont requis'
      });
    }

    // Créer le prompt pour OpenAI
    const prompt = `
Génère ${count} exercice(s) de mathématiques en français avec les caractéristiques suivantes :
- Niveau : ${grade}
- Thème : ${topic}
- Difficulté : ${difficulty}
- Type : ${type}

Pour chaque exercice, fournis :
1. Un titre court et clair
2. Une description (optionnelle)
3. La question détaillée
4. La réponse correcte
5. Une explication détaillée de la solution
6. 3 indices progressifs
${type === 'qcm' ? '7. 4 options de réponse (A, B, C, D) dont une seule correcte' : ''}

Formate ta réponse en JSON valide selon ce schéma :
{
  "exercises": [
    {
      "title": "string",
      "description": "string",
      "question": "string",
      "answer": "string",
      "explanation": "string",
      "hints": ["hint1", "hint2", "hint3"],
      ${type === 'qcm' ? '"options": {"A": "option1", "B": "option2", "C": "option3", "D": "option4"},' : ''}
      "points": number (entre 5 et 20)
    }
  ]
}
`;

    console.log('🤖 Génération d\'exercices avec OpenAI...');
    
    // Appel à OpenAI
    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'Tu es un professeur de mathématiques expert qui crée des exercices pédagogiques pour des collégiens français. Réponds uniquement en JSON valide.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.7,
      max_tokens: 2000
    });

    const content = completion.choices[0].message.content;
    const parsedData = JSON.parse(content);

    // Sauvegarder dans Supabase
    const exercisesToInsert = parsedData.exercises.map(ex => ({
      course_id: courseId,
      title: ex.title,
      description: ex.description || null,
      question: ex.question,
      answer: ex.answer,
      explanation: ex.explanation,
      difficulty: difficulty,
      points: ex.points || 10,
      type: type,
      hints: ex.hints || [],
      options: ex.options || null,
      ai_generated: true,
      is_published: false // À publier manuellement par un professeur
    }));

    const { data, error } = await supabase
      .from('exercises')
      .insert(exercisesToInsert)
      .select();

    if (error) {
      throw new Error(`Erreur Supabase: ${error.message}`);
    }

    console.log(`✅ ${data.length} exercice(s) généré(s) et sauvegardé(s)`);

    res.json({
      success: true,
      message: `${data.length} exercice(s) généré(s) avec succès`,
      count: data.length,
      exercises: data,
      usage: {
        tokens: completion.usage.total_tokens,
        cost: (completion.usage.total_tokens * 0.00003).toFixed(4) // Estimation GPT-4
      }
    });

  } catch (error) {
    console.error('❌ Erreur génération exercices:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la génération des exercices',
      error: error.message
    });
  }
});

// ============================================
// GÉNÉRATION DE CONTENU DE COURS
// ============================================

router.post('/generate-course-content', async (req, res) => {
  try {
    const {
      title,
      grade,
      topic,
      difficulty = 'moyen',
      duration = 30
    } = req.body;

    if (!title || !grade || !topic) {
      return res.status(400).json({
        success: false,
        message: 'title, grade et topic sont requis'
      });
    }

    const prompt = `
Crée un cours de mathématiques complet en français pour le niveau ${grade} sur le thème "${topic}" avec le titre "${title}".

Le cours doit durer environ ${duration} minutes et être de difficulté ${difficulty}.

Structure le cours avec :
1. Introduction (objectifs du cours)
2. Prérequis
3. Contenu principal (théorie, définitions, propriétés)
4. Exemples concrets
5. Méthodes et astuces
6. Pièges à éviter
7. Résumé

Formate ta réponse en JSON :
{
  "title": "string",
  "description": "string (2-3 phrases)",
  "content": "string (markdown formaté)",
  "prerequisites": ["string"],
  "learning_objectives": ["string"],
  "key_concepts": ["string"]
}
`;

    console.log('🤖 Génération de contenu de cours...');

    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'Tu es un professeur de mathématiques expert qui crée des cours pédagogiques structurés pour des collégiens français. Réponds en JSON valide.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.6,
      max_tokens: 3000
    });

    const content = completion.choices[0].message.content;
    const parsedData = JSON.parse(content);

    // Optionnel : sauvegarder directement le cours dans Supabase
    // Décommenter si vous voulez créer le cours automatiquement

    /*
    const { data, error } = await supabase
      .from('courses')
      .insert({
        title: parsedData.title,
        description: parsedData.description,
        content: parsedData.content,
        grade: grade,
        topic: topic,
        difficulty: difficulty,
        duration: duration,
        is_published: false
      })
      .select()
      .single();

    if (error) throw error;
    */

    console.log('✅ Contenu de cours généré');

    res.json({
      success: true,
      message: 'Contenu de cours généré avec succès',
      course: parsedData,
      usage: {
        tokens: completion.usage.total_tokens,
        cost: (completion.usage.total_tokens * 0.00003).toFixed(4)
      }
    });

  } catch (error) {
    console.error('❌ Erreur génération cours:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la génération du cours',
      error: error.message
    });
  }
});

// ============================================
// AMÉLIORATION D'UN EXERCICE EXISTANT
// ============================================

router.post('/improve-exercise', async (req, res) => {
  try {
    const { exerciseId } = req.body;

    if (!exerciseId) {
      return res.status(400).json({
        success: false,
        message: 'exerciseId est requis'
      });
    }

    // Récupérer l'exercice
    const { data: exercise, error } = await supabase
      .from('exercises')
      .select('*')
      .eq('id', exerciseId)
      .single();

    if (error || !exercise) {
      return res.status(404).json({
        success: false,
        message: 'Exercice non trouvé'
      });
    }

    const prompt = `
Améliore cet exercice de mathématiques :

Titre : ${exercise.title}
Question : ${exercise.question}
Réponse : ${exercise.answer}
Explication : ${exercise.explanation || 'Aucune'}

Suggestions d'amélioration :
1. Rendre la question plus claire
2. Ajouter des détails pertinents
3. Améliorer l'explication
4. Ajouter des indices utiles
5. Rendre l'exercice plus pédagogique

Retourne en JSON :
{
  "improved_question": "string",
  "improved_explanation": "string",
  "improved_hints": ["hint1", "hint2", "hint3"],
  "suggestions": ["suggestion1", "suggestion2"]
}
`;

    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'Tu es un expert en pédagogie des mathématiques. Améliore les exercices pour les rendre plus clairs et pédagogiques.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.5,
      max_tokens: 1500
    });

    const improvements = JSON.parse(completion.choices[0].message.content);

    res.json({
      success: true,
      message: 'Suggestions d\'amélioration générées',
      original: {
        question: exercise.question,
        explanation: exercise.explanation,
        hints: exercise.hints
      },
      improved: improvements,
      usage: {
        tokens: completion.usage.total_tokens
      }
    });

  } catch (error) {
    console.error('❌ Erreur amélioration exercice:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de l\'amélioration',
      error: error.message
    });
  }
});

// ============================================
// GÉNÉRATION DE FEEDBACK PERSONNALISÉ
// ============================================

router.post('/generate-feedback', async (req, res) => {
  try {
    const { exerciseId, userAnswer, isCorrect } = req.body;

    if (!exerciseId || !userAnswer) {
      return res.status(400).json({
        success: false,
        message: 'exerciseId et userAnswer sont requis'
      });
    }

    // Récupérer l'exercice
    const { data: exercise } = await supabase
      .from('exercises')
      .select('*')
      .eq('id', exerciseId)
      .single();

    if (!exercise) {
      return res.status(404).json({
        success: false,
        message: 'Exercice non trouvé'
      });
    }

    const prompt = `
Question : ${exercise.question}
Réponse correcte : ${exercise.answer}
Réponse de l'élève : ${userAnswer}
Résultat : ${isCorrect ? 'Correct' : 'Incorrect'}

Génère un feedback personnalisé et encourageant pour l'élève.
Si la réponse est incorrecte, explique l'erreur et guide vers la bonne solution sans donner la réponse directement.
Si la réponse est correcte, félicite et donne une astuce supplémentaire.

Réponds en JSON :
{
  "feedback": "string (2-3 phrases)",
  "encouragement": "string",
  "next_steps": "string"
}
`;

    const completion = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo', // GPT-3.5 suffit pour le feedback
      messages: [
        {
          role: 'system',
          content: 'Tu es un professeur bienveillant qui donne des feedbacks constructifs et encourageants.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.7,
      max_tokens: 300
    });

    const feedback = JSON.parse(completion.choices[0].message.content);

    res.json({
      success: true,
      feedback: feedback
    });

  } catch (error) {
    console.error('❌ Erreur génération feedback:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la génération du feedback',
      error: error.message
    });
  }
});

module.exports = router;




