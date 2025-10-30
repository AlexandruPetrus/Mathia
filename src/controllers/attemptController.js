const { Attempt, Exercise, User } = require('../models');
const { Op } = require('sequelize');

/**
 * POST /api/attempts - Enregistrer une réponse utilisateur et vérifier si elle est correcte
 */
const submitAttempt = async (req, res) => {
  try {
    const { exerciseId, userAnswer } = req.validatedBody;
    const userId = req.user.id;

    // Récupérer l'exercice
    const exercise = await Exercise.findByPk(exerciseId);

    if (!exercise) {
      return res.status(404).json({
        success: false,
        message: 'Exercice non trouvé'
      });
    }

    // Vérifier si la réponse est correcte (comparaison insensible à la casse)
    const isCorrect = userAnswer.trim().toLowerCase() === exercise.answer.trim().toLowerCase();

    // Créer la tentative dans la base de données
    const attempt = await Attempt.create({
      userId,
      exerciseId,
      userAnswer,
      isCorrect
    });

    // Réponse avec le résultat et l'explication si correct
    res.status(201).json({
      success: true,
      data: {
        attempt: {
          id: attempt.id,
          exerciseId: attempt.exerciseId,
          userAnswer: attempt.userAnswer,
          isCorrect: attempt.isCorrect,
          createdAt: attempt.createdAt
        },
        isCorrect,
        ...(isCorrect && { 
          explanation: exercise.explanation,
          correctAnswer: exercise.answer 
        })
      }
    });
  } catch (error) {
    console.error('Erreur lors de la soumission de la tentative:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la soumission de la tentative',
      error: error.message
    });
  }
};

/**
 * Récupérer les tentatives de l'utilisateur connecté
 */
const getMyAttempts = async (req, res) => {
  try {
    const userId = req.user.id;
    const { exerciseId, page = 1, limit = 20 } = req.query;

    const where = { userId };
    if (exerciseId) where.exerciseId = exerciseId;

    const offset = (page - 1) * limit;

    const { count, rows: attempts } = await Attempt.findAndCountAll({
      where,
      order: [['createdAt', 'DESC']],
      limit: parseInt(limit),
      offset: parseInt(offset),
      include: [
        {
          model: Exercise,
          as: 'exercise',
          attributes: ['id', 'type', 'difficulty'],
          include: [
            {
              model: require('../models/Course'),
              as: 'course',
              attributes: ['id', 'title', 'grade', 'chapter']
            }
          ]
        }
      ]
    });

    res.json({
      success: true,
      data: {
        attempts,
        pagination: {
          total: count,
          page: parseInt(page),
          totalPages: Math.ceil(count / limit),
          limit: parseInt(limit)
        }
      }
    });
  } catch (error) {
    console.error('Erreur lors de la récupération des tentatives:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la récupération des tentatives',
      error: error.message
    });
  }
};

/**
 * Récupérer les statistiques de l'utilisateur
 */
const getMyStats = async (req, res) => {
  try {
    const userId = req.user.id;

    // Statistiques globales
    const totalAttempts = await Attempt.count({ where: { userId } });
    const successfulAttempts = await Attempt.count({ 
      where: { userId, isCorrect: true } 
    });
    
    const successRate = totalAttempts > 0 
      ? Math.round((successfulAttempts / totalAttempts) * 100) 
      : 0;

    // Exercices uniques résolus
    const uniqueExercisesSolved = await Attempt.count({
      where: { userId, isCorrect: true },
      distinct: true,
      col: 'exerciseId'
    });

    // Tentatives récentes
    const recentAttempts = await Attempt.findAll({
      where: { userId },
      order: [['createdAt', 'DESC']],
      limit: 10,
      include: [
        {
          model: Exercise,
          as: 'exercise',
          attributes: ['id', 'title']
        }
      ]
    });

    // Statistiques par difficulté
    const statsByDifficulty = await Attempt.findAll({
      where: { userId },
      attributes: [
        [require('sequelize').fn('COUNT', require('sequelize').col('Attempt.id')), 'count'],
        [require('sequelize').fn('SUM', require('sequelize').literal('CASE WHEN "Attempt"."isCorrect" = true THEN 1 ELSE 0 END')), 'correct']
      ],
      include: [
        {
          model: Exercise,
          as: 'exercise',
          attributes: ['difficulty']
        }
      ],
      group: ['exercise.difficulty'],
      raw: true
    });

    res.json({
      success: true,
      data: {
        totalAttempts,
        successfulAttempts,
        successRate,
        uniqueExercisesSolved,
        recentAttempts,
        statsByDifficulty
      }
    });
  } catch (error) {
    console.error('Erreur lors de la récupération des statistiques:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la récupération des statistiques',
      error: error.message
    });
  }
};

/**
 * Récupérer toutes les tentatives (admin)
 */
const getAllAttempts = async (req, res) => {
  try {
    const { userId, exerciseId, page = 1, limit = 50 } = req.query;

    const where = {};
    if (userId) where.userId = userId;
    if (exerciseId) where.exerciseId = exerciseId;

    const offset = (page - 1) * limit;

    const { count, rows: attempts } = await Attempt.findAndCountAll({
      where,
      order: [['createdAt', 'DESC']],
      limit: parseInt(limit),
      offset: parseInt(offset),
      include: [
        {
          model: User,
          as: 'user',
          attributes: ['id', 'username', 'email', 'grade']
        },
        {
          model: Exercise,
          as: 'exercise',
          attributes: ['id', 'title', 'difficulty']
        }
      ]
    });

    res.json({
      success: true,
      data: {
        attempts,
        pagination: {
          total: count,
          page: parseInt(page),
          totalPages: Math.ceil(count / limit),
          limit: parseInt(limit)
        }
      }
    });
  } catch (error) {
    console.error('Erreur lors de la récupération des tentatives:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la récupération des tentatives',
      error: error.message
    });
  }
};

module.exports = {
  submitAttempt
};

