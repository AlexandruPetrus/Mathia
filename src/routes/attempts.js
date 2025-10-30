const express = require('express');
const router = express.Router();
const { authenticate } = require('../middleware/auth');
const { validate, schemas } = require('../middleware/validation');
const attemptController = require('../controllers/attemptController');

/**
 * @route   POST /api/attempts
 * @desc    Enregistrer une réponse utilisateur et vérifier si elle est correcte
 * @access  Private (JWT requis)
 */
router.post(
  '/',
  authenticate,
  validate(schemas.submitAttempt),
  attemptController.submitAttempt
);

module.exports = router;

