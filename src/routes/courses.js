const express = require('express');
const router = express.Router();
const { authenticate } = require('../middleware/auth');
const courseController = require('../controllers/courseController');

/**
 * @route   GET /api/courses
 * @desc    Récupérer tous les cours
 * @access  Private (JWT requis)
 */
router.get('/', authenticate, courseController.getCourses);

/**
 * @route   GET /api/courses/:id
 * @desc    Récupérer un cours par ID
 * @access  Private (JWT requis)
 */
router.get('/:id', authenticate, courseController.getCourseById);

module.exports = router;

