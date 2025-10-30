const { Exercise, Course } = require('../models');

/**
 * POST /api/admin/exercises - Ajouter un exercice manuellement
 */
const createExercise = async (req, res) => {
  try {
    const { courseId, type, body, options, answer, explanation, difficulty, tags } = req.validatedBody;

    // Vérifier que le cours existe
    const course = await Course.findByPk(courseId);

    if (!course) {
      return res.status(404).json({
        success: false,
        message: 'Cours non trouvé'
      });
    }

    // Créer l'exercice
    const exercise = await Exercise.create({
      courseId,
      type,
      body,
      options: options || null,
      answer,
      explanation: explanation || null,
      difficulty: difficulty || null,
      tags: tags || null
    });

    res.status(201).json({
      success: true,
      message: 'Exercice créé avec succès',
      data: {
        exercise
      }
    });
  } catch (error) {
    console.error('Erreur lors de la création de l\'exercice:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la création de l\'exercice',
      error: error.message
    });
  }
};

module.exports = {
  createExercise
};
