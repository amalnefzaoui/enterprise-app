const express = require('express');
const router = express.Router();
const { Enrollment, Course } = require('../models');

// GET /api/enrollments?employeeId=
router.get('/', async (req, res) => {
  try {
    const where = {};
    if (req.query.employeeId) where.employeeId = req.query.employeeId;
    if (req.query.courseId) where.courseId = req.query.courseId;

    const enrollments = await Enrollment.findAll({
      where,
      include: [{ model: Course, attributes: ['title', 'category', 'durationHours'] }],
      order: [['createdAt', 'DESC']]
    });
    res.json(enrollments);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/enrollments - inscrire un employé à une formation
router.post('/', async (req, res) => {
  try {
    const { employeeId, courseId } = req.body;

    const course = await Course.findByPk(courseId);
    if (!course) return res.status(404).json({ error: 'Formation non trouvée' });

    const existing = await Enrollment.findOne({ where: { employeeId, courseId } });
    if (existing) return res.status(400).json({ error: 'Déjà inscrit à cette formation' });

    const enrollment = await Enrollment.create({ employeeId, courseId });
    res.status(201).json(enrollment);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// PATCH /api/enrollments/:id/progress - mettre à jour la progression
router.patch('/:id/progress', async (req, res) => {
  try {
    const { progressPercent, score } = req.body;
    const enrollment = await Enrollment.findByPk(req.params.id);
    if (!enrollment) return res.status(404).json({ error: 'Inscription non trouvée' });

    enrollment.progressPercent = progressPercent;
    if (score !== undefined) enrollment.score = score;

    if (progressPercent >= 100) {
      enrollment.completionStatus = 'terminé';
      enrollment.completionDate = new Date().toISOString().split('T')[0];
    } else if (progressPercent > 0) {
      enrollment.completionStatus = 'en_cours';
    }

    await enrollment.save();
    res.json(enrollment);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// GET /api/enrollments/employee/:employeeId/summary - résumé formations d'un employé
router.get('/employee/:employeeId/summary', async (req, res) => {
  try {
    const enrollments = await Enrollment.findAll({
      where: { employeeId: req.params.employeeId },
      include: [{ model: Course, attributes: ['title', 'category'] }]
    });

    const total = enrollments.length;
    const completed = enrollments.filter(e => e.completionStatus === 'terminé').length;

    res.json({
      employeeId: req.params.employeeId,
      totalCourses: total,
      completedCourses: completed,
      inProgress: enrollments.filter(e => e.completionStatus === 'en_cours').length,
      enrollments
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
