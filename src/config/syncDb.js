const { sequelize } = require('./db');
const User = require('../models/User');
const Course = require('../models/Course');
const Exercise = require('../models/Exercise');
const Attempt = require('../models/Attempt');

const syncDatabase = async () => {
  try {
    console.log('🔄 Synchronisation de la base de données...');
    
    await sequelize.sync({ force: false, alter: true });
    
    console.log('✅ Base de données synchronisée avec succès');
    process.exit(0);
  } catch (error) {
    console.error('❌ Erreur lors de la synchronisation:', error);
    process.exit(1);
  }
};

syncDatabase();

