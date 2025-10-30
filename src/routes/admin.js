const express = require('express');
const router = express.Router();
const { authenticate } = require('../middleware/auth');
const { validate, schemas } = require('../middleware/validation');
const adminController = require('../controllers/adminController');

/**
 * @route   POST /api/admin/exercises
 * @desc    Ajouter un exercice manuellement
 * @access  Private (JWT requis)
 */
router.post(
  '/exercises',
  authenticate,
  validate(schemas.createExercise),
  adminController.createExercise
);

module.exports = router;
