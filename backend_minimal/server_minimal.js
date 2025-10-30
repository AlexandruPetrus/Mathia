require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

const app = express();
const PORT = process.env.PORT || 3000;

// ============================================
// MIDDLEWARE
// ============================================

app.use(helmet());
app.use(cors());
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 50, // limite réduite car API minimale
  message: { success: false, message: 'Trop de requêtes' }
});
app.use('/api', limiter);

// ============================================
// ROUTES
// ============================================

// Route racine
app.get('/', (req, res) => {
  res.json({
    success: true,
    message: '🎓 API Mathia Minimale - Génération IA uniquement',
    version: '2.0.0',
    info: 'Les opérations CRUD sont gérées directement par Supabase',
    endpoints: {
      health: '/api/health',
      generateExercises: 'POST /api/ai/generate-exercises',
      generateCourse: 'POST /api/ai/generate-course'
    }
  });
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    success: true,
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// ============================================
// ROUTES IA
// ============================================

const aiRoutes = require('./routes/ai');
app.use('/api/ai', aiRoutes);

// ============================================
// GESTION D'ERREURS
// ============================================

// 404 - Route non trouvée
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: 'Route non trouvée. Consultez / pour la liste des endpoints disponibles.'
  });
});

// Erreur globale
app.use((err, req, res, next) => {
  console.error('❌ Erreur:', err);
  res.status(err.status || 500).json({
    success: false,
    message: err.message || 'Erreur serveur interne',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
});

// ============================================
// DÉMARRAGE DU SERVEUR
// ============================================

app.listen(PORT, () => {
  console.log('');
  console.log('🚀 ========================================');
  console.log(`🎓 API Mathia Minimale démarrée`);
  console.log(`📍 URL: http://localhost:${PORT}`);
  console.log(`🤖 Génération IA: ACTIVÉE`);
  console.log(`🌍 Environnement: ${process.env.NODE_ENV || 'development'}`);
  console.log('');
  console.log('ℹ️  Les opérations CRUD sont gérées par Supabase');
  console.log('ℹ️  Ce serveur gère uniquement la génération IA');
  console.log('🚀 ========================================');
  console.log('');
});

// Gestion de l'arrêt gracieux
process.on('SIGTERM', () => {
  console.log('👋 SIGTERM reçu, arrêt du serveur...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('👋 SIGINT reçu, arrêt du serveur...');
  process.exit(0);
});

module.exports = app;




