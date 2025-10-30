const { Exercise, Course } = require('../models');
const { Op } = require('sequelize');
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;

// Configuration de multer pour l'upload de fichiers
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/exercises/');
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({
  storage: storage,
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB max
  },
  fileFilter: function (req, file, cb) {
    const allowedTypes = ['.pdf', '.json', '.txt'];
    const ext = path.extname(file.originalname).toLowerCase();
    
    if (allowedTypes.includes(ext)) {
      cb(null, true);
    } else {
      cb(new Error('Type de fichier non autorisé. Utilisez PDF, JSON ou TXT.'));
    }
  }
});

/**
 * GET /api/admin/exercises - Liste tous les exercices avec pagination
 */
const getAllExercises = async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const offset = (page - 1) * limit;
    
    const { search, courseId, difficulty, type } = req.query;
    
    // Construire les conditions de recherche
    const whereConditions = {};
    
    if (search) {
      whereConditions[Op.or] = [
        { body: { [Op.iLike]: `%${search}%` } },
        { answer: { [Op.iLike]: `%${search}%` } }
      ];
    }
    
    if (courseId) {
      whereConditions.courseId = courseId;
    }
    
    if (difficulty) {
      whereConditions.difficulty = difficulty;
    }
    
    if (type) {
      whereConditions.type = type;
    }
    
    const { count, rows: exercises } = await Exercise.findAndCountAll({
      where: whereConditions,
      include: [{
        model: Course,
        as: 'course',
        attributes: ['id', 'title', 'grade', 'chapter']
      }],
      order: [['createdAt', 'DESC']],
      limit,
      offset
    });
    
    res.json({
      success: true,
      data: {
        exercises,
        pagination: {
          currentPage: page,
          totalPages: Math.ceil(count / limit),
          totalItems: count,
          itemsPerPage: limit
        }
      }
    });
  } catch (error) {
    console.error('Erreur lors de la récupération des exercices:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la récupération des exercices',
      error: error.message
    });
  }
};

/**
 * POST /api/admin/exercises - Créer un nouvel exercice
 */
const createExercise = async (req, res) => {
  try {
    const { courseId, type, body, options, answer, explanation, difficulty, tags } = req.body;
    
    // Vérifier que le cours existe
    const course = await Course.findByPk(courseId);
    if (!course) {
      return res.status(404).json({
        success: false,
        message: 'Cours non trouvé'
      });
    }
    
    // Créer l'exercice
    const exercise = await Exercise.create({
      courseId,
      type,
      body,
      options: options ? JSON.parse(options) : null,
      answer,
      explanation,
      difficulty,
      tags: tags ? JSON.parse(tags) : null
    });
    
    // Récupérer l'exercice avec les informations du cours
    const exerciseWithCourse = await Exercise.findByPk(exercise.id, {
      include: [{
        model: Course,
        as: 'course',
        attributes: ['id', 'title', 'grade', 'chapter']
      }]
    });
    
    res.status(201).json({
      success: true,
      data: { exercise: exerciseWithCourse }
    });
  } catch (error) {
    console.error('Erreur lors de la création de l\'exercice:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la création de l\'exercice',
      error: error.message
    });
  }
};

/**
 * PUT /api/admin/exercises/:id - Modifier un exercice
 */
const updateExercise = async (req, res) => {
  try {
    const { id } = req.params;
    const { courseId, type, body, options, answer, explanation, difficulty, tags } = req.body;
    
    const exercise = await Exercise.findByPk(id);
    if (!exercise) {
      return res.status(404).json({
        success: false,
        message: 'Exercice non trouvé'
      });
    }
    
    // Vérifier que le cours existe si courseId est fourni
    if (courseId) {
      const course = await Course.findByPk(courseId);
      if (!course) {
        return res.status(404).json({
          success: false,
          message: 'Cours non trouvé'
        });
      }
    }
    
    // Mettre à jour l'exercice
    await exercise.update({
      courseId: courseId || exercise.courseId,
      type: type || exercise.type,
      body: body || exercise.body,
      options: options ? JSON.parse(options) : exercise.options,
      answer: answer || exercise.answer,
      explanation: explanation !== undefined ? explanation : exercise.explanation,
      difficulty: difficulty || exercise.difficulty,
      tags: tags ? JSON.parse(tags) : exercise.tags
    });
    
    // Récupérer l'exercice mis à jour avec les informations du cours
    const updatedExercise = await Exercise.findByPk(exercise.id, {
      include: [{
        model: Course,
        as: 'course',
        attributes: ['id', 'title', 'grade', 'chapter']
      }]
    });
    
    res.json({
      success: true,
      data: { exercise: updatedExercise }
    });
  } catch (error) {
    console.error('Erreur lors de la modification de l\'exercice:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la modification de l\'exercice',
      error: error.message
    });
  }
};

/**
 * DELETE /api/admin/exercises/:id - Supprimer un exercice
 */
const deleteExercise = async (req, res) => {
  try {
    const { id } = req.params;
    
    const exercise = await Exercise.findByPk(id);
    if (!exercise) {
      return res.status(404).json({
        success: false,
        message: 'Exercice non trouvé'
      });
    }
    
    await exercise.destroy();
    
    res.json({
      success: true,
      message: 'Exercice supprimé avec succès'
    });
  } catch (error) {
    console.error('Erreur lors de la suppression de l\'exercice:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la suppression de l\'exercice',
      error: error.message
    });
  }
};

/**
 * POST /api/admin/exercises/import - Importer des exercices depuis un fichier
 */
const importExercises = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: 'Aucun fichier fourni'
      });
    }
    
    const { courseId } = req.body;
    const filePath = req.file.path;
    const fileExtension = path.extname(req.file.originalname).toLowerCase();
    
    // Vérifier que le cours existe
    const course = await Course.findByPk(courseId);
    if (!course) {
      // Nettoyer le fichier uploadé
      await fs.unlink(filePath);
      return res.status(404).json({
        success: false,
        message: 'Cours non trouvé'
      });
    }
    
    let exercises = [];
    let importResults = { success: 0, errors: 0, details: [] };
    
    try {
      if (fileExtension === '.json') {
        // Import depuis JSON
        const fileContent = await fs.readFile(filePath, 'utf-8');
        exercises = JSON.parse(fileContent);
        
        if (!Array.isArray(exercises)) {
          exercises = [exercises];
        }
        
      } else if (fileExtension === '.pdf') {
        // Import depuis PDF (nécessite le script Python)
        const { spawn } = require('child_process');
        
        return new Promise((resolve) => {
          const pythonProcess = spawn('python', [
            'scripts/pdf_exercise_importer.py',
            '--pdf', filePath,
            '--course-id', courseId,
            '--auto-format'
          ]);
          
          let output = '';
          let errorOutput = '';
          
          pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
          });
          
          pythonProcess.stderr.on('data', (data) => {
            errorOutput += data.toString();
          });
          
          pythonProcess.on('close', async (code) => {
            // Nettoyer le fichier uploadé
            await fs.unlink(filePath);
            
            if (code === 0) {
              res.json({
                success: true,
                message: 'Import PDF terminé avec succès',
                data: { output }
              });
            } else {
              res.status(500).json({
                success: false,
                message: 'Erreur lors de l\'import PDF',
                error: errorOutput
              });
            }
            resolve();
          });
        });
        
      } else if (fileExtension === '.txt') {
        // Import depuis texte brut
        const fileContent = await fs.readFile(filePath, 'utf-8');
        // Utiliser le formateur d'exercices
        const { spawn } = require('child_process');
        
        return new Promise((resolve) => {
          const pythonProcess = spawn('python', [
            'scripts/exercise_formatter.py',
            '--input', filePath,
            '--output', filePath + '.json'
          ]);
          
          pythonProcess.on('close', async (code) => {
            if (code === 0) {
              // Lire le fichier JSON généré
              const jsonPath = filePath + '.json';
              const fileContent = await fs.readFile(jsonPath, 'utf-8');
              exercises = JSON.parse(fileContent);
              
              // Nettoyer les fichiers temporaires
              await fs.unlink(filePath);
              await fs.unlink(jsonPath);
            } else {
              // Nettoyer le fichier uploadé
              await fs.unlink(filePath);
              return res.status(500).json({
                success: false,
                message: 'Erreur lors du formatage du fichier texte'
              });
            }
            resolve();
          });
        });
      }
      
      // Importer les exercices JSON
      for (const exerciseData of exercises) {
        try {
          const exercise = await Exercise.create({
            courseId,
            type: exerciseData.type || 'libre',
            body: exerciseData.body || exerciseData.question || '',
            options: exerciseData.options || null,
            answer: exerciseData.answer || '',
            explanation: exerciseData.explanation || null,
            difficulty: exerciseData.difficulty || 'moyen',
            tags: exerciseData.tags || null
          });
          
          importResults.success++;
          importResults.details.push({
            status: 'success',
            exerciseId: exercise.id,
            body: exercise.body.substring(0, 50) + '...'
          });
          
        } catch (error) {
          importResults.errors++;
          importResults.details.push({
            status: 'error',
            error: error.message,
            data: exerciseData
          });
        }
      }
      
      // Nettoyer le fichier uploadé
      await fs.unlink(filePath);
      
      res.json({
        success: true,
        message: `Import terminé: ${importResults.success} succès, ${importResults.errors} erreurs`,
        data: importResults
      });
      
    } catch (error) {
      // Nettoyer le fichier uploadé en cas d'erreur
      await fs.unlink(filePath);
      throw error;
    }
    
  } catch (error) {
    console.error('Erreur lors de l\'import des exercices:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de l\'import des exercices',
      error: error.message
    });
  }
};

/**
 * GET /api/admin/exercises/stats - Statistiques des exercices
 */
const getExerciseStats = async (req, res) => {
  try {
    const totalExercises = await Exercise.count();
    
    const statsByType = await Exercise.findAll({
      attributes: [
        'type',
        [Exercise.sequelize.fn('COUNT', Exercise.sequelize.col('id')), 'count']
      ],
      group: ['type'],
      raw: true
    });
    
    const statsByDifficulty = await Exercise.findAll({
      attributes: [
        'difficulty',
        [Exercise.sequelize.fn('COUNT', Exercise.sequelize.col('id')), 'count']
      ],
      group: ['difficulty'],
      raw: true
    });
    
    const statsByCourse = await Exercise.findAll({
      attributes: [
        'courseId',
        [Exercise.sequelize.fn('COUNT', Exercise.sequelize.col('id')), 'count']
      ],
      include: [{
        model: Course,
        as: 'course',
        attributes: ['title', 'grade', 'chapter']
      }],
      group: ['courseId', 'course.id', 'course.title', 'course.grade', 'course.chapter'],
      raw: true
    });
    
    res.json({
      success: true,
      data: {
        total: totalExercises,
        byType: statsByType,
        byDifficulty: statsByDifficulty,
        byCourse: statsByCourse
      }
    });
  } catch (error) {
    console.error('Erreur lors de la récupération des statistiques:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la récupération des statistiques',
      error: error.message
    });
  }
};

module.exports = {
  getAllExercises,
  createExercise,
  updateExercise,
  deleteExercise,
  importExercises,
  getExerciseStats,
  upload
};

