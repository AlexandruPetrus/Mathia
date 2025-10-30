const { Course, Exercise } = require('../models');
const { Op } = require('sequelize');

/**
 * GET tous les cours
 */
const getCourses = async (req, res) => {
  try {
    const courses = await Course.findAll({
      order: [['createdAt', 'DESC']],
      include: [
        {
          model: Exercise,
          as: 'exercises',
          attributes: ['id', 'type', 'difficulty']
        }
      ]
    });

    res.json({
      success: true,
      data: {
        courses
      }
    });
  } catch (error) {
    console.error('Erreur lors de la récupération des cours:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la récupération des cours',
      error: error.message
    });
  }
};

/**
 * GET un cours par ID avec tous ses exercices
 */
const getCourseById = async (req, res) => {
  try {
    const { id } = req.params;

    const course = await Course.findByPk(id, {
      include: [
        {
          model: Exercise,
          as: 'exercises'
        }
      ]
    });

    if (!course) {
      return res.status(404).json({
        success: false,
        message: 'Cours non trouvé'
      });
    }

    res.json({
      success: true,
      data: { course }
    });
  } catch (error) {
    console.error('Erreur lors de la récupération du cours:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la récupération du cours',
      error: error.message
    });
  }
};

/**
 * Créer un nouveau cours (admin/teacher)
 */
const createCourse = async (req, res) => {
  try {
    const courseData = req.validatedBody;

    const course = await Course.create(courseData);

    res.status(201).json({
      success: true,
      message: 'Cours créé avec succès',
      data: { course }
    });
  } catch (error) {
    console.error('Erreur lors de la création du cours:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la création du cours',
      error: error.message
    });
  }
};

/**
 * Mettre à jour un cours (admin/teacher)
 */
const updateCourse = async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;

    const course = await Course.findByPk(id);

    if (!course) {
      return res.status(404).json({
        success: false,
        message: 'Cours non trouvé'
      });
    }

    await course.update(updates);

    res.json({
      success: true,
      message: 'Cours mis à jour avec succès',
      data: { course }
    });
  } catch (error) {
    console.error('Erreur lors de la mise à jour du cours:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la mise à jour du cours',
      error: error.message
    });
  }
};

/**
 * Supprimer un cours (admin)
 */
const deleteCourse = async (req, res) => {
  try {
    const { id } = req.params;

    const course = await Course.findByPk(id);

    if (!course) {
      return res.status(404).json({
        success: false,
        message: 'Cours non trouvé'
      });
    }

    await course.destroy();

    res.json({
      success: true,
      message: 'Cours supprimé avec succès'
    });
  } catch (error) {
    console.error('Erreur lors de la suppression du cours:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la suppression du cours',
      error: error.message
    });
  }
};

/**
 * Récupérer les statistiques des cours
 */
const getCourseStats = async (req, res) => {
  try {
    const stats = await Course.findAll({
      attributes: [
        'grade',
        [require('sequelize').fn('COUNT', require('sequelize').col('id')), 'count']
      ],
      group: ['grade']
    });

    res.json({
      success: true,
      data: { stats }
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

module.exports = {
  getCourses,
  getCourseById
};

