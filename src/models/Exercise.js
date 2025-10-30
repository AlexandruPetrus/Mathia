const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/db');

const Exercise = sequelize.define('Exercise', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  courseId: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: 'courses',
      key: 'id'
    },
    onDelete: 'CASCADE'
  },
  type: {
    type: DataTypes.STRING(50),
    allowNull: false,
    comment: 'qcm, libre, vrai-faux, calcul, etc.'
  },
  body: {
    type: DataTypes.TEXT,
    allowNull: false,
    comment: 'Énoncé de l\'exercice'
  },
  options: {
    type: DataTypes.JSON,
    allowNull: true,
    comment: 'Options pour les QCM (format JSON)'
  },
  answer: {
    type: DataTypes.TEXT,
    allowNull: false,
    comment: 'Réponse correcte'
  },
  explanation: {
    type: DataTypes.TEXT,
    allowNull: true,
    comment: 'Explication de la solution'
  },
  difficulty: {
    type: DataTypes.STRING(20),
    allowNull: true,
    comment: 'facile, moyen, difficile'
  },
  tags: {
    type: DataTypes.JSON,
    allowNull: true,
    comment: 'Tags pour catégoriser l\'exercice'
  }
}, {
  tableName: 'exercises',
  timestamps: true,
  indexes: [
    {
      fields: ['courseId']
    },
    {
      fields: ['difficulty']
    }
  ]
});

module.exports = Exercise;

