const User = require('./User');
const Course = require('./Course');
const Exercise = require('./Exercise');
const Attempt = require('./Attempt');

// Relations entre les modèles

// Un Course a plusieurs Exercises
Course.hasMany(Exercise, {
  foreignKey: 'courseId',
  as: 'exercises',
  onDelete: 'CASCADE'
});

Exercise.belongsTo(Course, {
  foreignKey: 'courseId',
  as: 'course'
});

// Un User a plusieurs Attempts
User.hasMany(Attempt, {
  foreignKey: 'userId',
  as: 'attempts',
  onDelete: 'CASCADE'
});

Attempt.belongsTo(User, {
  foreignKey: 'userId',
  as: 'user'
});

// Un Exercise a plusieurs Attempts
Exercise.hasMany(Attempt, {
  foreignKey: 'exerciseId',
  as: 'attempts',
  onDelete: 'CASCADE'
});

Attempt.belongsTo(Exercise, {
  foreignKey: 'exerciseId',
  as: 'exercise'
});

module.exports = {
  User,
  Course,
  Exercise,
  Attempt
};

