const express = require('express');
const router = express.Router();
const { authenticate } = require('../middleware/auth');
const exerciseController = require('../controllers/exerciseController');

/**
 * @route   GET /api/exercises
 * @desc    Récupérer tous les exercices avec filtrage par courseId et difficulty
 * @access  Private (JWT requis)
 */
router.get('/', authenticate, exerciseController.getExercises);

module.exports = router;

