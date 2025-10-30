const express = require('express');
const router = express.Router();
const { validate, schemas } = require('../middleware/validation');
const authController = require('../controllers/authController');

/**
 * @route   POST /api/auth/signup
 * @desc    Inscription d'un nouvel utilisateur
 * @access  Public
 */
router.post('/signup', validate(schemas.signup), authController.signup);

/**
 * @route   POST /api/auth/login
 * @desc    Connexion d'un utilisateur
 * @access  Public
 */
router.post('/login', validate(schemas.login), authController.login);

module.exports = router;

