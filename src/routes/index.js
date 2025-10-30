const express = require('express');
const router = express.Router();

// Importer toutes les routes
const authRoutes = require('./auth');
const courseRoutes = require('./courses');
const exerciseRoutes = require('./exercises');
const attemptRoutes = require('./attempts');
const adminRoutes = require('./admin');

// Route de santé (sans authentification)
router.get('/health', (req, res) => {
  res.json({
    success: true,
    message: 'API Mathia fonctionnelle',
    timestamp: new Date().toISOString()
  });
});

// Monter les routes
// /auth : routes publiques (pas de JWT)
router.use('/auth', authRoutes);

// Toutes les autres routes nécessitent JWT (appliqué dans chaque router)
router.use('/courses', courseRoutes);
router.use('/exercises', exerciseRoutes);
router.use('/attempts', attemptRoutes);
router.use('/admin', adminRoutes);

module.exports = router;

