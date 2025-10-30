const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/db');

const Attempt = sequelize.define('Attempt', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  userId: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: 'users',
      key: 'id'
    },
    onDelete: 'CASCADE'
  },
  exerciseId: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: 'exercises',
      key: 'id'
    },
    onDelete: 'CASCADE'
  },
  userAnswer: {
    type: DataTypes.TEXT,
    allowNull: false
  },
  isCorrect: {
    type: DataTypes.BOOLEAN,
    allowNull: false
  },
  createdAt: {
    type: DataTypes.DATE,
    allowNull: false,
    defaultValue: DataTypes.NOW
  }
}, {
  tableName: 'attempts',
  timestamps: false,
  indexes: [
    {
      fields: ['userId']
    },
    {
      fields: ['exerciseId']
    },
    {
      fields: ['userId', 'exerciseId']
    }
  ]
});

module.exports = Attempt;

