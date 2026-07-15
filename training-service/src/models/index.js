const sequelize = require('../config/database');
const Course = require('./Course');
const Enrollment = require('./Enrollment');

module.exports = { sequelize, Course, Enrollment };
