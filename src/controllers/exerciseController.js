const { Exercise, Course, Attempt } = require('../models');
const { Op } = require('sequelize');

/**
 * GET tous les exercices avec filtrage optionnel par courseId et difficulty
 */
const getExercises = async (req, res) => {
  try {
    const { courseId, difficulty } = req.query;

    const where = {};

    // Filtrage par courseId
    if (courseId) {
      where.courseId = parseInt(courseId);
    }

    // Filtrage par difficulty
    if (difficulty) {
      where.difficulty = difficulty;
    }

    const exercises = await Exercise.findAll({
      where,
      order: [['createdAt', 'DESC']],
      include: [
        {
          model: Course,
          as: 'course',
          attributes: ['id', 'title', 'grade', 'chapter']
        }
      ]
    });

    res.json({
      success: true,
      data: {
        exercises
      }
    });
  } catch (error) {
    console.error('Erreur lors de la récupération des exercices:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la récupération des exercices',
      error: error.message
    });
  }
};

/**
 * Récupérer un exercice par ID
 */
const getExerciseById = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user?.id;

    const exercise = await Exercise.findOne({
      where: { id },
      include: [
        {
          model: Course,
          as: 'course',
          attributes: ['id', 'title', 'grade', 'chapter']
        }
      ]
    });

    if (!exercise) {
      return res.status(404).json({
        success: false,
        message: 'Exercice non trouvé'
      });
    }

    // Masquer la réponse pour les étudiants
    const exerciseData = exercise.toJSON();
    
    // Récupérer les tentatives de l'utilisateur pour cet exercice
    let userAttempts = [];
    if (userId) {
      userAttempts = await Attempt.findAll({
        where: { userId, exerciseId: id },
        order: [['createdAt', 'DESC']],
        limit: 5
      });
    }

    // Ne pas envoyer la réponse si l'utilisateur n'a pas encore réussi
    const hasSucceeded = userAttempts.some(a => a.isCorrect);
    if (!hasSucceeded) {
      delete exerciseData.answer;
    }

    res.json({
      success: true,
      data: {
        exercise: exerciseData,
        userAttempts: userAttempts.map(a => ({
          id: a.id,
          isCorrect: a.isCorrect,
          createdAt: a.createdAt
        }))
      }
    });
  } catch (error) {
    console.error('Erreur lors de la récupération de l\'exercice:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la récupération de l\'exercice',
      error: error.message
    });
  }
};

/**
 * Créer un nouvel exercice (admin/teacher)
 */
const createExercise = async (req, res) => {
  try {
    const exerciseData = req.validatedBody;

    // Vérifier que le cours existe
    const course = await Course.findByPk(exerciseData.courseId);
    if (!course) {
      return res.status(404).json({
        success: false,
        message: 'Cours non trouvé'
      });
    }

    const exercise = await Exercise.create(exerciseData);

    res.status(201).json({
      success: true,
      message: 'Exercice créé avec succès',
      data: { exercise }
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

/**
 * Mettre à jour un exercice (admin/teacher)
 */
const updateExercise = async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;

    const exercise = await Exercise.findByPk(id);

    if (!exercise) {
      return res.status(404).json({
        success: false,
        message: 'Exercice non trouvé'
      });
    }

    await exercise.update(updates);

    res.json({
      success: true,
      message: 'Exercice mis à jour avec succès',
      data: { exercise }
    });
  } catch (error) {
    console.error('Erreur lors de la mise à jour de l\'exercice:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la mise à jour de l\'exercice',
      error: error.message
    });
  }
};

/**
 * Supprimer un exercice (admin)
 */
const deleteExercise = async (req, res) => {
  try {
    const { id } = req.params;

    const exercise = await Exercise.findByPk(id);

    if (!exercise) {
      return res.status(404).json({
        success: false,
        message: 'Exercice non trouvé'
      });
    }

    await exercise.destroy();

    res.json({
      success: true,
      message: 'Exercice supprimé avec succès'
    });
  } catch (error) {
    console.error('Erreur lors de la suppression de l\'exercice:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la suppression de l\'exercice',
      error: error.message
    });
  }
};

module.exports = {
  getExercises
};

