const express = require('express');
const router = express.Router();
const {
  getAllExercises,
  createExercise,
  updateExercise,
  deleteExercise,
  importExercises,
  getExerciseStats,
  upload
} = require('../controllers/adminExerciseController');
const { authenticateToken, requireAdmin } = require('../middleware/auth');

// Middleware d'authentification pour toutes les routes admin
router.use(authenticateToken);
router.use(requireAdmin);

// Créer le dossier uploads s'il n'existe pas
const fs = require('fs');
const path = require('path');
const uploadsDir = path.join(__dirname, '../../uploads/exercises');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

/**
 * @swagger
 * /api/admin/exercises:
 *   get:
 *     summary: Récupérer tous les exercices (Admin)
 *     tags: [Admin - Exercices]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *           default: 1
 *         description: Numéro de page
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *           default: 20
 *         description: Nombre d'éléments par page
 *       - in: query
 *         name: search
 *         schema:
 *           type: string
 *         description: Recherche dans le contenu des exercices
 *       - in: query
 *         name: courseId
 *         schema:
 *           type: integer
 *         description: Filtrer par cours
 *       - in: query
 *         name: difficulty
 *         schema:
 *           type: string
 *           enum: [facile, moyen, difficile]
 *         description: Filtrer par difficulté
 *       - in: query
 *         name: type
 *         schema:
 *           type: string
 *           enum: [qcm, libre, vrai-faux, calcul]
 *         description: Filtrer par type d'exercice
 *     responses:
 *       200:
 *         description: Liste des exercices avec pagination
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   type: object
 *                   properties:
 *                     exercises:
 *                       type: array
 *                       items:
 *                         $ref: '#/components/schemas/Exercise'
 *                     pagination:
 *                       type: object
 *                       properties:
 *                         currentPage:
 *                           type: integer
 *                         totalPages:
 *                           type: integer
 *                         totalItems:
 *                           type: integer
 *                         itemsPerPage:
 *                           type: integer
 */
router.get('/', getAllExercises);

/**
 * @swagger
 * /api/admin/exercises:
 *   post:
 *     summary: Créer un nouvel exercice (Admin)
 *     tags: [Admin - Exercices]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - courseId
 *               - type
 *               - body
 *               - answer
 *             properties:
 *               courseId:
 *                 type: integer
 *                 description: ID du cours
 *               type:
 *                 type: string
 *                 enum: [qcm, libre, vrai-faux, calcul]
 *                 description: Type d'exercice
 *               body:
 *                 type: string
 *                 description: Énoncé de l'exercice
 *               options:
 *                 type: string
 *                 description: Options JSON pour les QCM
 *               answer:
 *                 type: string
 *                 description: Réponse correcte
 *               explanation:
 *                 type: string
 *                 description: Explication de la solution
 *               difficulty:
 *                 type: string
 *                 enum: [facile, moyen, difficile]
 *                 default: moyen
 *               tags:
 *                 type: string
 *                 description: Tags JSON pour catégoriser
 *     responses:
 *       201:
 *         description: Exercice créé avec succès
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   type: object
 *                   properties:
 *                     exercise:
 *                       $ref: '#/components/schemas/Exercise'
 */
router.post('/', createExercise);

/**
 * @swagger
 * /api/admin/exercises/{id}:
 *   put:
 *     summary: Modifier un exercice (Admin)
 *     tags: [Admin - Exercices]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: ID de l'exercice
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               courseId:
 *                 type: integer
 *               type:
 *                 type: string
 *                 enum: [qcm, libre, vrai-faux, calcul]
 *               body:
 *                 type: string
 *               options:
 *                 type: string
 *               answer:
 *                 type: string
 *               explanation:
 *                 type: string
 *               difficulty:
 *                 type: string
 *                 enum: [facile, moyen, difficile]
 *               tags:
 *                 type: string
 *     responses:
 *       200:
 *         description: Exercice modifié avec succès
 *       404:
 *         description: Exercice non trouvé
 */
router.put('/:id', updateExercise);

/**
 * @swagger
 * /api/admin/exercises/{id}:
 *   delete:
 *     summary: Supprimer un exercice (Admin)
 *     tags: [Admin - Exercices]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: ID de l'exercice
 *     responses:
 *       200:
 *         description: Exercice supprimé avec succès
 *       404:
 *         description: Exercice non trouvé
 */
router.delete('/:id', deleteExercise);

/**
 * @swagger
 * /api/admin/exercises/import:
 *   post:
 *     summary: Importer des exercices depuis un fichier (Admin)
 *     tags: [Admin - Exercices]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         multipart/form-data:
 *           schema:
 *             type: object
 *             required:
 *               - file
 *               - courseId
 *             properties:
 *               file:
 *                 type: string
 *                 format: binary
 *                 description: Fichier PDF, JSON ou TXT
 *               courseId:
 *                 type: integer
 *                 description: ID du cours de destination
 *     responses:
 *       200:
 *         description: Import terminé avec succès
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 message:
 *                   type: string
 *                 data:
 *                   type: object
 *                   properties:
 *                     success:
 *                       type: integer
 *                     errors:
 *                       type: integer
 *                     details:
 *                       type: array
 */
router.post('/import', upload.single('file'), importExercises);

/**
 * @swagger
 * /api/admin/exercises/stats:
 *   get:
 *     summary: Statistiques des exercices (Admin)
 *     tags: [Admin - Exercices]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Statistiques des exercices
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   type: object
 *                   properties:
 *                     total:
 *                       type: integer
 *                     byType:
 *                       type: array
 *                       items:
 *                         type: object
 *                         properties:
 *                           type:
 *                             type: string
 *                           count:
 *                             type: integer
 *                     byDifficulty:
 *                       type: array
 *                       items:
 *                         type: object
 *                         properties:
 *                           difficulty:
 *                             type: string
 *                           count:
 *                             type: integer
 *                     byCourse:
 *                       type: array
 *                       items:
 *                         type: object
 *                         properties:
 *                           courseId:
 *                             type: integer
 *                           count:
 *                             type: integer
 *                           course:
 *                             type: object
 *                             properties:
 *                               title:
 *                                 type: string
 *                               grade:
 *                                 type: string
 *                               chapter:
 *                                 type: string
 */
router.get('/stats', getExerciseStats);

module.exports = router;

