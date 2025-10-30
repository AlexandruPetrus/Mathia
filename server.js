require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
const path = require('path');

const { connectDB } = require('./src/config/db');
const routes = require('./src/routes');
const { errorHandler, notFound } = require('./src/middleware/errorHandler');

// Initialiser l'application Express
const app = express();
const PORT = process.env.PORT || 3000;

// Charger la documentation Swagger
let swaggerDocument;
try {
  swaggerDocument = YAML.load(path.join(__dirname, 'docs', 'openapi.yaml'));
} catch (error) {
  console.log('⚠️  Documentation Swagger non trouvée');
}

// Middleware de sécurité
app.use(helmet());

// Configuration CORS
const corsOptions = {
  origin: process.env.CORS_ORIGIN || '*',
  credentials: true,
  optionsSuccessStatus: 200
};
app.use(cors(corsOptions));

// Rate limiting
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 15 * 60 * 1000, // 15 minutes
  max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 100,
  message: {
    success: false,
    message: 'Trop de requêtes, veuillez réessayer plus tard.'
  },
  standardHeaders: true,
  legacyHeaders: false
});

// Appliquer le rate limiting à toutes les routes
app.use('/api', limiter);

// Middleware pour parser le JSON
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logger des requêtes en mode développement
if (process.env.NODE_ENV === 'development') {
  app.use((req, res, next) => {
    console.log(`${req.method} ${req.path}`);
    next();
  });
}

// Route racine
app.get('/', (req, res) => {
  res.json({
    success: true,
    message: '🎓 Bienvenue sur l\'API Mathia',
    version: '1.0.0',
    documentation: '/api-docs',
    endpoints: {
      health: '/api/health',
      auth: '/api/auth',
      courses: '/api/courses',
      exercises: '/api/exercises',
      attempts: '/api/attempts',
      admin: '/api/admin'
    }
  });
});

// Documentation API avec Swagger
if (swaggerDocument) {
  app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument, {
    customCss: '.swagger-ui .topbar { display: none }',
    customSiteTitle: 'Mathia API Documentation'
  }));
}

// Monter les routes API
app.use('/api', routes);

// Gestion des routes non trouvées
app.use(notFound);

// Middleware de gestion des erreurs (doit être en dernier)
app.use(errorHandler);

// Démarrer le serveur
const startServer = async () => {
  try {
    // Connexion à la base de données
    await connectDB();

    // Démarrer le serveur
    app.listen(PORT, () => {
      console.log('');
      console.log('🚀 ========================================');
      console.log(`🎓 Serveur Mathia démarré avec succès`);
      console.log(`📍 URL: http://localhost:${PORT}`);
      console.log(`📚 Documentation: http://localhost:${PORT}/api-docs`);
      console.log(`🌍 Environnement: ${process.env.NODE_ENV || 'development'}`);
      console.log('🚀 ========================================');
      console.log('');
    });
  } catch (error) {
    console.error('❌ Erreur lors du démarrage du serveur:', error);
    process.exit(1);
  }
};

// Gestion de l'arrêt gracieux
process.on('SIGTERM', () => {
  console.log('👋 SIGTERM reçu, arrêt du serveur...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('👋 SIGINT reçu, arrêt du serveur...');
  process.exit(0);
});

// Démarrer le serveur
startServer();

module.exports = app;

