const Joi = require('joi');

/**
 * Middleware pour valider les données des requêtes
 */
const validate = (schema) => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,
      stripUnknown: true
    });

    if (error) {
      const errors = error.details.map(detail => ({
        field: detail.path.join('.'),
        message: detail.message
      }));

      return res.status(400).json({
        success: false,
        message: 'Erreur de validation',
        errors
      });
    }

    req.validatedBody = value;
    next();
  };
};

// Schémas de validation
const schemas = {
  // Validation pour l'inscription
  signup: Joi.object({
    name: Joi.string().min(3).max(100).required(),
    email: Joi.string().email().required(),
    password: Joi.string().min(6).required()
  }),

  // Validation pour la connexion
  login: Joi.object({
    email: Joi.string().email().required(),
    password: Joi.string().required()
  }),

  // Validation pour créer un cours
  createCourse: Joi.object({
    title: Joi.string().max(200).required(),
    grade: Joi.string().max(10).required(),
    chapter: Joi.string().max(100).required(),
    description: Joi.string().optional()
  }),

  // Validation pour créer un exercice
  createExercise: Joi.object({
    courseId: Joi.number().integer().required(),
    type: Joi.string().max(50).required(),
    body: Joi.string().required(),
    options: Joi.object().optional().allow(null),
    answer: Joi.string().required(),
    explanation: Joi.string().optional().allow(null, ''),
    difficulty: Joi.string().max(20).optional().allow(null, ''),
    tags: Joi.alternatives().try(Joi.object(), Joi.array()).optional().allow(null)
  }),

  // Validation pour soumettre une tentative
  submitAttempt: Joi.object({
    exerciseId: Joi.number().integer().required(),
    userAnswer: Joi.string().required()
  }),

  // Validation pour mise à jour du profil
  updateProfile: Joi.object({
    name: Joi.string().max(100).optional(),
    email: Joi.string().email().optional()
  })
};

module.exports = {
  validate,
  schemas
};

