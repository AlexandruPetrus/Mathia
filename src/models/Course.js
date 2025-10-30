const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/db');

const Course = sequelize.define('Course', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  title: {
    type: DataTypes.STRING(200),
    allowNull: false
  },
  grade: {
    type: DataTypes.STRING(10),
    allowNull: false,
    comment: '6ème, 5ème, 4ème, 3ème'
  },
  chapter: {
    type: DataTypes.STRING(100),
    allowNull: false,
    comment: 'Chapitre ou thème du cours'
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: true
  }
}, {
  tableName: 'courses',
  timestamps: true
});

module.exports = Course;

