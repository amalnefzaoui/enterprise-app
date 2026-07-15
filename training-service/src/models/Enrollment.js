const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');
const Course = require('./Course');

// employeeId référence l'employé dans le service RH (Python API) —
// pas de FK inter-services, juste un identifiant partagé.
const Enrollment = sequelize.define('Enrollment', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  employeeId: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  courseId: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: { model: Course, key: 'id' }
  },
  enrollmentDate: {
    type: DataTypes.DATEONLY,
    defaultValue: DataTypes.NOW
  },
  completionStatus: {
    type: DataTypes.ENUM('non_commencé', 'en_cours', 'terminé'),
    defaultValue: 'non_commencé'
  },
  progressPercent: {
    type: DataTypes.INTEGER,
    defaultValue: 0
  },
  completionDate: {
    type: DataTypes.DATEONLY,
    allowNull: true
  },
  score: {
    type: DataTypes.FLOAT,
    allowNull: true
  }
}, {
  tableName: 'enrollments',
  timestamps: true
});

Enrollment.belongsTo(Course, { foreignKey: 'courseId' });
Course.hasMany(Enrollment, { foreignKey: 'courseId' });

module.exports = Enrollment;
